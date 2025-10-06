from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data_engineering.streaming.stream_processor import stream_processor
from dependencies import get_current_user
from schemas import UserResponse
from db_config import get_db
from models.user_model import User
import pandas as pd
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/batch-report")
def get_batch_analytics(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get batch processed analytics (requires authentication)"""
    try:
        users = db.query(User).all()
        
        if not users:
            return {
                "success": True, 
                "data": {
                    "total_users": 0,
                    "active_users": 0,
                    "message": "No users found"
                }
            }
        
        total_users = len(users)
        active_users = len([u for u in users if u.is_active])
        users_with_names = len([u for u in users if u.full_name])
        
        analytics = {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users,
            "users_with_full_name": users_with_names,
            "completion_rate": round((users_with_names / total_users) * 100, 2) if total_users > 0 else 0,
            "processed_at": datetime.now().isoformat()
        }
        
        return {"success": True, "data": analytics}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics processing failed: {str(e)}")

@router.get("/public-analytics")
def get_public_analytics(db: Session = Depends(get_db)):
    """Get analytics without authentication"""
    try:
        users = db.query(User).all()
        
        if not users:
            return {
                "success": True, 
                "data": {
                    "total_users": 0,
                    "active_users": 0,
                    "message": "No users found"
                }
            }
        
        total_users = len(users)
        active_users = len([u for u in users if u.is_active])
        users_with_names = len([u for u in users if u.full_name])
        
        analytics = {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users,
            "users_with_full_name": users_with_names,
            "completion_rate": round((users_with_names / total_users) * 100, 2) if total_users > 0 else 0,
            "processed_at": datetime.now().isoformat()
        }
        
        return {"success": True, "data": analytics}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/streaming-stats")
def get_streaming_stats(current_user: UserResponse = Depends(get_current_user)):
    """Get real-time streaming statistics"""
    try:
        stats = stream_processor.get_real_time_stats()
        return {"success": True, "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming stats failed: {str(e)}")

@router.get("/recent-events")
def get_recent_events(limit: int = 10, current_user: UserResponse = Depends(get_current_user)):
    """Get recent streaming events"""
    try:
        events = stream_processor.get_recent_events(limit)
        return {"success": True, "data": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recent events failed: {str(e)}")

@router.get("/simple-stats")
def get_simple_stats(db: Session = Depends(get_db)):
    """Get simple statistics without authentication for testing"""
    try:
        user_count = db.query(User).count()
        active_count = db.query(User).filter(User.is_active == True).count()
        
        return {
            "success": True,
            "data": {
                "total_users": user_count,
                "active_users": active_count,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}