from fastapi import HTTPException, status, Depends, Request
from datetime import timedelta
from sqlalchemy.orm import Session

from schemas import UserCreate, UserResponse, Token, UserLogin
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, verify_password
from helpers import success_response, error_response
from database import create_user, authenticate_user
from db_config import get_db
from services.activity_logger import ActivityLogger
from services.event_streaming import EventPublisher
import asyncio

def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    try:
        user_response = create_user(db, user)
        
        # Re-enable activity logging for registration
        try:
            ActivityLogger.log_registration(db=db, user_id=user_response.id, request=request)
            
            # Publish registration event to Kafka simulation
            asyncio.create_task(EventPublisher.publish_registration_event(
                user_id=user_response.id,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            ))
        except Exception as log_error:
            print(f"Activity logging error: {log_error}")
        
        return success_response(user_response, "User registered successfully")
    except ValueError as e:
        return error_response(str(e), status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Registration error: {str(e)}")  # Debug print
        return error_response("Registration failed", status.HTTP_500_INTERNAL_SERVER_ERROR)

def login(user_login: UserLogin, request: Request, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, user_login.username, user_login.password)
        if not user:
            # Log failed login attempt
            try:
                ActivityLogger.log_activity(
                    db=db,
                    activity_type="login_failed",
                    request=request,
                    description=f"Failed login for username: {user_login.username}",
                    status_code=401
                )
                
                # Publish failed login event to Kafka simulation
                asyncio.create_task(EventPublisher.publish_login_event(
                    user_id=None,
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    success=False
                ))
            except Exception as log_error:
                print(f"Activity logging error: {log_error}")
            return error_response("Incorrect username or password", status.HTTP_401_UNAUTHORIZED)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # Re-enable activity logging for successful login
        try:
            ActivityLogger.log_login(db=db, user_id=user.id, request=request, success=True)
            
            # Publish login event to Kafka simulation
            asyncio.create_task(EventPublisher.publish_login_event(
                user_id=user.id,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                success=True
            ))
        except Exception as log_error:
            print(f"Activity logging error: {log_error}")
        
        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat()
            }
        }
        
        return success_response(response_data, "Login successful")
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug print
        return error_response("Login failed", status.HTTP_500_INTERNAL_SERVER_ERROR)