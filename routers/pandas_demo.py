from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_config import get_db
from models.user_model import User
from models.activity_log import UserActivityLog
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

router = APIRouter(prefix="/pandas", tags=["pandas-demo"])

@router.get("/user-analytics")
def pandas_user_analytics(db: Session = Depends(get_db)):
    """Pandas-powered user analytics"""
    try:
        # Extract data using SQLAlchemy
        users = db.query(User).all()
        
        if not users:
            return {"message": "No users found"}
        
        # Convert to pandas DataFrame
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'full_name': user.full_name,
                'is_active': user.is_active,
                'created_at': user.created_at
            })
        
        df = pd.DataFrame(user_data)
        
        # Pandas transformations
        df['email_domain'] = df['email'].str.split('@').str[1]
        df['has_full_name'] = df['full_name'].notna()
        df['account_age_days'] = (datetime.now() - pd.to_datetime(df['created_at'])).dt.days
        
        # Analytics using pandas - convert numpy types to Python types
        analytics = {
            "total_users": int(len(df)),
            "active_users": int(df['is_active'].sum()),
            "users_with_full_name": int(df['has_full_name'].sum()),
            "avg_account_age": float(df['account_age_days'].mean()) if len(df) > 0 else 0,
            "email_domains": {k: int(v) for k, v in df['email_domain'].value_counts().to_dict().items()},
            "completion_rate": float((df['has_full_name'].sum() / len(df)) * 100)
        }
        
        return {
            "success": True,
            "pandas_analytics": analytics,
            "sample_data": df.head(3).to_dict('records')
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/activity-analytics")
def pandas_activity_analytics(db: Session = Depends(get_db)):
    """Pandas-powered activity analytics"""
    try:
        # Extract activity logs
        activities = db.query(UserActivityLog).all()
        
        if not activities:
            return {"message": "No activity logs found"}
        
        # Convert to pandas DataFrame
        activity_data = []
        for activity in activities:
            activity_data.append({
                'id': activity.id,
                'user_id': activity.user_id,
                'activity_type': activity.activity_type,
                'ip_address': activity.ip_address,
                'created_at': activity.created_at
            })
        
        df = pd.DataFrame(activity_data)
        
        # Pandas analytics - convert numpy types to Python types
        analytics = {
            "total_activities": int(len(df)),
            "activity_types": {k: int(v) for k, v in df['activity_type'].value_counts().to_dict().items()},
            "unique_users": int(df['user_id'].nunique()),
            "unique_ips": int(df['ip_address'].nunique()),
            "activities_last_hour": int(len(df[df['created_at'] > datetime.now() - timedelta(hours=1)]))
        }
        
        return {
            "success": True,
            "pandas_activity_analytics": analytics,
            "sample_data": df.head(3).to_dict('records')
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/etl-demo")
def pandas_etl_demo(db: Session = Depends(get_db)):
    """Complete ETL pipeline demo using Pandas"""
    try:
        # EXTRACT - Get data from database
        users = db.query(User).all()
        activities = db.query(UserActivityLog).all()
        
        if not users:
            return {"message": "No users found for ETL demo"}
        
        # Convert to DataFrames
        users_df = pd.DataFrame([{
            'user_id': u.id, 'email': u.email, 'username': u.username,
            'created_at': u.created_at, 'is_active': u.is_active
        } for u in users])
        
        activities_df = pd.DataFrame([{
            'user_id': a.user_id, 'activity_type': a.activity_type,
            'created_at': a.created_at
        } for a in activities]) if activities else pd.DataFrame()
        
        # TRANSFORM - Clean and merge data
        if not users_df.empty:
            # Add calculated columns
            users_df['email_domain'] = users_df['email'].str.split('@').str[1]
            users_df['user_type'] = users_df['is_active'].apply(
                lambda x: 'active' if x else 'inactive'
            )
            
            if not activities_df.empty:
                # Join users with their activities
                merged_df = pd.merge(users_df, activities_df, on='user_id', how='left')
                
                # LOAD - Generate insights
                insights = {
                    "user_activity_summary": {k: int(v) for k, v in merged_df.groupby('user_type')['activity_type'].count().to_dict().items()},
                    "domain_analysis": {k: int(v) for k, v in users_df['email_domain'].value_counts().head(5).to_dict().items()},
                    "activity_patterns": {k: int(v) for k, v in activities_df['activity_type'].value_counts().to_dict().items()}
                }
            else:
                insights = {
                    "user_summary": {k: int(v) for k, v in users_df['user_type'].value_counts().to_dict().items()},
                    "domain_analysis": {k: int(v) for k, v in users_df['email_domain'].value_counts().head(5).to_dict().items()},
                    "note": "No activity data available"
                }
        else:
            insights = {"message": "Insufficient data for ETL demo"}
        
        return {
            "success": True,
            "etl_results": insights,
            "process": "Extract → Transform → Load completed using Pandas"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}