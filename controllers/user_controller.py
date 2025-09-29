from fastapi import HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from schemas import UserUpdate, UserResponse
from database import get_user_by_id, get_all_users, update_user, delete_user
from dependencies import get_current_user
from db_config import get_db

def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user

def get_users(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    users = get_all_users(db)
    return [UserResponse(**user.__dict__) for user in users]

def get_user(user_id: int, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.__dict__)

def update_user_info(user_id: int, user_update: UserUpdate, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    user = update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.__dict__)

def delete_user_account(user_id: int, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}