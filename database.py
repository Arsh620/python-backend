from sqlalchemy.orm import Session
from models.user_model import User
from schemas import UserCreate, UserUpdate, UserResponse
from auth import get_password_hash, verify_password

def create_user(db: Session, user: UserCreate) -> UserResponse:
    if User.get_by_username(db, user.username):
        raise ValueError("Username already exists")
    if User.get_by_email(db, user.email):
        raise ValueError("Email already exists")
    
    db_user = User.create(
        db=db,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password)
    )
    return UserResponse(**db_user.__dict__)

def get_user_by_id(db: Session, user_id: int):
    return User.get_by_id(db, user_id)

def get_user_by_username(db: Session, username: str):
    return User.get_by_username(db, username)

def get_all_users(db: Session):
    return User.get_all(db)

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = User.get_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    return db_user.update(db, **update_data)

def delete_user(db: Session, user_id: int):
    db_user = User.get_by_id(db, user_id)
    if not db_user:
        return False
    return db_user.delete(db)

def authenticate_user(db: Session, username: str, password: str):
    user = User.get_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user