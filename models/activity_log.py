from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from .base import Base

class UserActivityLog(Base):
    """
    Model to store user activity logs for data engineering pipeline
    This table will capture all user interactions for analytics
    """
    __tablename__ = "user_activity_logs"
    
    # Primary key for each log entry
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to users table to track which user performed the action
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous actions
    
    # Type of activity (login, logout, register, api_call, etc.)
    activity_type = Column(String(50), nullable=False, index=True)
    
    # Detailed description of the activity
    activity_description = Column(Text)
    
    # IP address of the user for security and location analytics
    ip_address = Column(String(45))  # IPv6 compatible
    
    # User agent string for device/browser analytics
    user_agent = Column(Text)
    
    # HTTP method and endpoint for API analytics
    http_method = Column(String(10))
    endpoint = Column(String(255))
    
    # Response status code for error tracking
    status_code = Column(Integer)
    
    # Timestamp when the activity occurred (indexed for time-series queries)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Additional metadata as JSON string for flexible data storage
    event_metadata = Column(Text)  # Store JSON string for additional context
    
    @classmethod
    def create_log(cls, db, **kwargs):
        """
        Helper method to create a new activity log entry
        Used by the logging service to insert new records
        """
        log_entry = cls(**kwargs)
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
    
    @classmethod
    def get_user_activities(cls, db, user_id, limit=100):
        """
        Get recent activities for a specific user
        Used for user behavior analysis
        """
        return db.query(cls).filter(cls.user_id == user_id).order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_activities_by_type(cls, db, activity_type, limit=1000):
        """
        Get activities by type for analytics
        Used for tracking specific user behaviors
        """
        return db.query(cls).filter(cls.activity_type == activity_type).order_by(cls.timestamp.desc()).limit(limit).all()