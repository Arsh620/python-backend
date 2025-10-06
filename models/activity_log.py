from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from .base import Base

class UserActivityLog(Base):
    __tablename__ = "user_activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_type = Column(String, index=True)
    activity_description = Column(Text)
    ip_address = Column(String)
    user_agent = Column(String)
    http_method = Column(String)
    endpoint = Column(String)
    status_code = Column(Integer)
    event_metadata = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def create_log(cls, db, user_id: int = None, activity_type: str = "", activity_description: str = "", 
                   ip_address: str = None, user_agent: str = None, http_method: str = None, 
                   endpoint: str = None, status_code: int = None, event_metadata: str = None):
        activity = cls(
            user_id=user_id,
            activity_type=activity_type,
            activity_description=activity_description,
            ip_address=ip_address,
            user_agent=user_agent,
            http_method=http_method,
            endpoint=endpoint,
            status_code=status_code,
            event_metadata=event_metadata
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity