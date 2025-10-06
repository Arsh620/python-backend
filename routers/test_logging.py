from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db_config import get_db
from models.activity_log import UserActivityLog
from datetime import datetime

router = APIRouter(prefix="/test", tags=["testing"])

@router.post("/log-test")
def test_logging(request: Request, db: Session = Depends(get_db)):
    try:
        # Create a simple test log
        activity_log = UserActivityLog(
            user_id=1,
            activity_type="test",
            activity_description="Test log entry",
            ip_address="127.0.0.1",
            user_agent="test-agent",
            http_method="POST",
            endpoint="/test/log-test",
            status_code=200,
            event_metadata='{"test": true}'
        )
        
        db.add(activity_log)
        db.commit()
        db.refresh(activity_log)
        
        return {
            "success": True,
            "message": "Log created successfully",
            "log_id": activity_log.id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    try:
        logs = db.query(UserActivityLog).all()
        return {
            "success": True,
            "count": len(logs),
            "logs": [
                {
                    "id": log.id,
                    "user_id": log.user_id,
                    "activity_type": log.activity_type,
                    "description": log.activity_description,
                    "created_at": log.created_at.isoformat() if log.created_at else None
                }
                for log in logs
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }