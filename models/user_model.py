from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def create(cls, db, **kwargs):
        instance = cls(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    
    @classmethod
    def get_by_id(cls, db, user_id):
        return db.query(cls).filter(cls.id == user_id).first()
    
    @classmethod
    def get_by_username(cls, db, username):
        return db.query(cls).filter(cls.username == username).first()
    
    @classmethod
    def get_by_email(cls, db, email):
        return db.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()
    
    def update(self, db, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db):
        db.delete(self)
        db.commit()
        return True