from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from db_config import get_db
from services.analytics_etl import AnalyticsETL
from dependencies import get_current_user
from schemas import UserResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard")
def get_dashboard_stats(
    days: int = Query(7, description="Number of days to analyze"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get dashboard analytics for admin users
    This endpoint provides key metrics for business intelligence
    """
    etl = AnalyticsETL(db)
    
    return {
        "login_trends": etl.extract_daily_login_stats(days),
        "security_alerts": etl.extract_security_alerts(24),
        "api_usage": etl.extract_api_usage_stats(days),
        "analysis_period": f"Last {days} days"
    }

@router.get("/user-behavior/{user_id}")
def get_user_behavior(
    user_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get behavior analysis for a specific user
    This helps in user experience optimization and personalization
    """
    etl = AnalyticsETL(db)
    return etl.extract_user_behavior_patterns(user_id)

@router.get("/security-alerts")
def get_security_alerts(
    hours: int = Query(24, description="Hours to look back for alerts"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get security alerts for monitoring suspicious activities
    This endpoint is used by security teams for threat detection
    """
    etl = AnalyticsETL(db)
    return etl.extract_security_alerts(hours)

@router.get("/daily-report")
def get_daily_report(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive daily analytics report
    This provides executive summary of platform usage
    """
    etl = AnalyticsETL(db)
    return etl.generate_daily_report()

@router.get("/my-activity")
def get_my_activity(
    user_id: int = Query(..., description="User ID to get activity for"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current user's activity patterns
    This allows users to see their own usage analytics
    """
    etl = AnalyticsETL(db)
    return etl.extract_user_behavior_patterns(user_id)