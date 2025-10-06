from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_config import get_db
from models.user_model import User
from models.activity_log import UserActivityLog
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

router = APIRouter(prefix="/advanced", tags=["advanced-analytics"])

@router.get("/user-segmentation")
def user_segmentation(db: Session = Depends(get_db)):
    """Advanced user segmentation - impossible with simple SQL"""
    try:
        users = db.query(User).all()
        activities = db.query(UserActivityLog).all()
        
        if not users:
            return {"message": "No data for segmentation"}
        
        # Create DataFrames
        users_df = pd.DataFrame([{
            'user_id': u.id, 'email': u.email, 'created_at': u.created_at,
            'is_active': u.is_active, 'full_name': u.full_name
        } for u in users])
        
        activities_df = pd.DataFrame([{
            'user_id': a.user_id, 'activity_type': a.activity_type,
            'created_at': a.created_at
        } for a in activities]) if activities else pd.DataFrame()
        
        # Advanced transformations
        users_df['account_age_days'] = (datetime.now() - pd.to_datetime(users_df['created_at'])).dt.days
        users_df['email_domain'] = users_df['email'].str.split('@').str[1]
        users_df['profile_completeness'] = users_df['full_name'].notna().astype(int)
        
        if not activities_df.empty:
            # Calculate user engagement metrics
            user_activity_stats = activities_df.groupby('user_id').agg({
                'activity_type': 'count',
                'created_at': ['min', 'max']
            }).reset_index()
            
            user_activity_stats.columns = ['user_id', 'total_activities', 'first_activity', 'last_activity']
            
            # Merge with users
            merged_df = pd.merge(users_df, user_activity_stats, on='user_id', how='left')
            merged_df['total_activities'] = merged_df['total_activities'].fillna(0)
            
            # Advanced segmentation using percentiles
            merged_df['activity_percentile'] = pd.qcut(merged_df['total_activities'], 
                                                     q=4, labels=['Low', 'Medium', 'High', 'Power'])
            
            # RFM-like analysis
            merged_df['recency_days'] = (datetime.now() - pd.to_datetime(merged_df['last_activity'])).dt.days
            merged_df['recency_score'] = pd.cut(merged_df['recency_days'], 
                                              bins=[0, 1, 7, 30, float('inf')], 
                                              labels=['Today', 'Week', 'Month', 'Inactive'])
        else:
            merged_df = users_df
            merged_df['activity_percentile'] = 'No Activity'
            merged_df['recency_score'] = 'No Activity'
        
        # User segments
        segments = merged_df.groupby(['activity_percentile', 'recency_score']).size().to_dict()
        
        # Cohort analysis by email domain
        domain_analysis = merged_df.groupby('email_domain').agg({
            'user_id': 'count',
            'profile_completeness': 'mean',
            'account_age_days': 'mean'
        }).to_dict('index')
        
        return {
            "success": True,
            "user_segments": {str(k): int(v) for k, v in segments.items()},
            "domain_insights": {k: {
                'user_count': int(v['user_id']),
                'completion_rate': float(v['profile_completeness'] * 100),
                'avg_age_days': float(v['account_age_days'])
            } for k, v in domain_analysis.items()},
            "total_segments": len(segments)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/predictive-insights")
def predictive_insights(db: Session = Depends(get_db)):
    """Predictive analytics - ML ready data"""
    try:
        users = db.query(User).all()
        activities = db.query(UserActivityLog).all()
        
        if len(users) < 5:
            return {"message": "Need more data for predictions"}
        
        # Create feature matrix
        users_df = pd.DataFrame([{
            'user_id': u.id, 'created_at': u.created_at,
            'is_active': u.is_active, 'has_full_name': bool(u.full_name)
        } for u in users])
        
        # Feature engineering
        users_df['account_age_days'] = (datetime.now() - pd.to_datetime(users_df['created_at'])).dt.days
        users_df['registration_hour'] = pd.to_datetime(users_df['created_at']).dt.hour
        users_df['registration_day'] = pd.to_datetime(users_df['created_at']).dt.dayofweek
        
        if activities:
            activity_features = pd.DataFrame([{
                'user_id': a.user_id, 'activity_count': 1
            } for a in activities]).groupby('user_id').sum().reset_index()
            
            users_df = pd.merge(users_df, activity_features, on='user_id', how='left')
            users_df['activity_count'] = users_df['activity_count'].fillna(0)
        else:
            users_df['activity_count'] = 0
        
        # Churn prediction features
        users_df['churn_risk_score'] = (
            (users_df['account_age_days'] > 30).astype(int) * 0.3 +
            (users_df['activity_count'] == 0).astype(int) * 0.4 +
            (~users_df['has_full_name']).astype(int) * 0.3
        )
        
        # Engagement prediction
        users_df['engagement_score'] = (
            (users_df['activity_count'] / (users_df['account_age_days'] + 1)) * 100
        ).round(2)
        
        # Risk segments
        users_df['risk_category'] = pd.cut(users_df['churn_risk_score'], 
                                         bins=[0, 0.3, 0.6, 1.0], 
                                         labels=['Low Risk', 'Medium Risk', 'High Risk'])
        
        insights = {
            "churn_analysis": users_df['risk_category'].value_counts().to_dict(),
            "avg_engagement_by_risk": users_df.groupby('risk_category')['engagement_score'].mean().to_dict(),
            "high_risk_users": int(users_df[users_df['churn_risk_score'] > 0.6].shape[0]),
            "feature_importance": {
                "account_age": "30%",
                "activity_level": "40%", 
                "profile_completion": "30%"
            }
        }
        
        return {
            "success": True,
            "predictive_insights": insights,
            "ml_ready": "Features engineered for machine learning models"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/time-series-analysis")
def time_series_analysis(db: Session = Depends(get_db)):
    """Time series analysis - trends and patterns"""
    try:
        activities = db.query(UserActivityLog).all()
        
        if not activities:
            return {"message": "No activity data for time series"}
        
        # Create time series DataFrame
        ts_df = pd.DataFrame([{
            'timestamp': a.created_at,
            'activity_type': a.activity_type,
            'user_id': a.user_id
        } for a in activities])
        
        ts_df['timestamp'] = pd.to_datetime(ts_df['timestamp'])
        ts_df['date'] = ts_df['timestamp'].dt.date
        ts_df['hour'] = ts_df['timestamp'].dt.hour
        ts_df['day_of_week'] = ts_df['timestamp'].dt.day_name()
        
        # Time-based analytics
        daily_activity = ts_df.groupby('date').size()
        hourly_pattern = ts_df.groupby('hour').size()
        weekly_pattern = ts_df.groupby('day_of_week').size()
        
        # Trend analysis
        if len(daily_activity) > 1:
            trend = "increasing" if daily_activity.iloc[-1] > daily_activity.iloc[0] else "decreasing"
        else:
            trend = "insufficient_data"
        
        # Peak hours
        peak_hour = hourly_pattern.idxmax() if not hourly_pattern.empty else None
        peak_day = weekly_pattern.idxmax() if not weekly_pattern.empty else None
        
        return {
            "success": True,
            "time_series_insights": {
                "daily_activity": {str(k): int(v) for k, v in daily_activity.to_dict().items()},
                "hourly_pattern": {str(k): int(v) for k, v in hourly_pattern.to_dict().items()},
                "weekly_pattern": {str(k): int(v) for k, v in weekly_pattern.to_dict().items()},
                "trend": trend,
                "peak_hour": int(peak_hour) if peak_hour is not None else None,
                "peak_day": peak_day,
                "total_data_points": len(ts_df)
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}