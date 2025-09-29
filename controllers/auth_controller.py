from fastapi import HTTPException, status, Depends
from datetime import timedelta
from sqlalchemy.orm import Session

from schemas import UserCreate, UserResponse, Token, UserLogin
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, verify_password
from helpers import success_response, error_response
from database import create_user, authenticate_user
from db_config import get_db

def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_response = create_user(db, user)
        return success_response(user_response, "User registered successfully")
    except ValueError as e:
        return error_response(str(e), status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return error_response("Registration failed", status.HTTP_500_INTERNAL_SERVER_ERROR)

def login(user_login: UserLogin, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, user_login.username, user_login.password)
        if not user:
            return error_response("Incorrect username or password", status.HTTP_401_UNAUTHORIZED)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(**user.__dict__)
        }
        
        return success_response(response_data, "Login successful")
    except Exception as e:
        return error_response("Login failed", status.HTTP_500_INTERNAL_SERVER_ERROR)