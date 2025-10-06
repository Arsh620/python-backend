from fastapi import HTTPException, status, Depends, Request
from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from schemas import UserCreate, UserResponse, Token, UserLogin
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, verify_password
from helpers import success_response, error_response
from db_config import get_db
from data_engineering.streaming.real_kafka import real_kafka_processor
from models.activity_log import UserActivityLog

def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    try:
        # Force database usage - no fallback
        from database import create_user
        user_response = create_user(db, user)
        
        # Log registration activity
        print(f"Logging registration for user {user_response.id}")
        activity_log = UserActivityLog(
            user_id=user_response.id,
            activity_type="register",
            activity_description="New user registration",
            ip_address=request.client.host if request.client else "127.0.0.1",
            user_agent=request.headers.get("user-agent", "unknown"),
            http_method=request.method,
            endpoint=str(request.url.path),
            status_code=201,
            event_metadata='{"registration_timestamp": "' + datetime.utcnow().isoformat() + '"}'
        )
        db.add(activity_log)
        db.commit()
        print(f"✅ Registration activity logged successfully for user {user_response.id}")
        
        # Publish to REAL Kafka
        kafka_event_data = {
            "user_id": user_response.id,
            "email": user_response.email,
            "username": user_response.username,
            "ip_address": request.client.host if request.client else "127.0.0.1",
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        
        kafka_success = real_kafka_processor.publish_event(
            event_type='user_registration',
            data=kafka_event_data,
            topic='user_events'
        )
        
        if kafka_success:
            print(f"✅ Registration event published to Kafka for user {user_response.id}")
        else:
            print(f"⚠️ Failed to publish registration event to Kafka for user {user_response.id}")
        
        return success_response(user_response, "User registered successfully")
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return error_response(f"Registration failed: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

def login(user_login: UserLogin, request: Request, db: Session = Depends(get_db)):
    try:
        # Force database usage - no fallback
        from database import authenticate_user
        user = authenticate_user(db, user_login.username, user_login.password)
        
        if not user:
            # Log failed login attempt
            print("Logging failed login attempt")
            activity_log = UserActivityLog(
                user_id=None,
                activity_type="login_failed",
                activity_description="Failed login attempt",
                ip_address=request.client.host if request.client else "127.0.0.1",
                user_agent=request.headers.get("user-agent", "unknown"),
                http_method=request.method,
                endpoint=str(request.url.path),
                status_code=401,
                event_metadata='{"login_success": false, "username": "' + user_login.username + '"}'
            )
            db.add(activity_log)
            db.commit()
            print("❌ Failed login attempt logged")
            
            # Publish failed login to Kafka
            real_kafka_processor.publish_event(
                event_type='login_failed',
                data={
                    "username": user_login.username,
                    "ip_address": request.client.host if request.client else "127.0.0.1",
                    "user_agent": request.headers.get("user-agent", "unknown")
                },
                topic='system_events'
            )
            
            return error_response("Incorrect username or password", status.HTTP_401_UNAUTHORIZED)
        
        # Log successful login
        print(f"Logging successful login for user {user.id}")
        activity_log = UserActivityLog(
            user_id=user.id,
            activity_type="login",
            activity_description="Successful user login",
            ip_address=request.client.host if request.client else "127.0.0.1",
            user_agent=request.headers.get("user-agent", "unknown"),
            http_method=request.method,
            endpoint=str(request.url.path),
            status_code=200,
            event_metadata='{"login_success": true}'
        )
        db.add(activity_log)
        db.commit()
        print(f"✅ Login activity logged successfully for user {user.id}")
        
        user_data = UserResponse(**user.__dict__)
        
        # Publish successful login to REAL Kafka
        kafka_event_data = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "ip_address": request.client.host if request.client else "127.0.0.1",
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        
        kafka_success = real_kafka_processor.publish_event(
            event_type='user_login',
            data=kafka_event_data,
            topic='user_events'
        )
        
        if kafka_success:
            print(f"✅ Login event published to Kafka for user {user.id}")
        else:
            print(f"⚠️ Failed to publish login event to Kafka for user {user.id}")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data.username}, expires_delta=access_token_expires
        )
        
        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }
        
        return success_response(response_data, "Login successful")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return error_response(f"Login failed: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)