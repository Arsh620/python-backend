import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db_config import SessionLocal
from models.user_model import User

class DataProcessor:
    def __init__(self):
        self.db = SessionLocal()
    
    def extract_user_data(self) -> pd.DataFrame:
        """Extract user data from database"""
        users = self.db.query(User).all()
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'full_name': user.full_name,
                'is_active': user.is_active,
                'created_at': user.created_at
            })
        return pd.DataFrame(data)
    
    def transform_user_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform and clean user data"""
        # Data cleaning
        df['email_domain'] = df['email'].str.split('@').str[1]
        df['account_age_days'] = (datetime.now() - pd.to_datetime(df['created_at'])).dt.days
        df['has_full_name'] = df['full_name'].notna()
        
        # Add analytics columns
        df['user_type'] = df['account_age_days'].apply(
            lambda x: 'new' if x <= 7 else 'regular' if x <= 30 else 'veteran'
        )
        
        return df
    
    def load_analytics_data(self, df: pd.DataFrame) -> dict:
        """Load processed data into analytics format"""
        analytics = {
            'total_users': len(df),
            'active_users': len(df[df['is_active'] == True]),
            'new_users_last_7_days': len(df[df['account_age_days'] <= 7]),
            'top_email_domains': df['email_domain'].value_counts().head(5).to_dict(),
            'user_type_distribution': df['user_type'].value_counts().to_dict(),
            'users_with_full_name': df['has_full_name'].sum()
        }
        return analytics
    
    def run_etl_pipeline(self) -> dict:
        """Complete ETL pipeline"""
        # Extract
        raw_data = self.extract_user_data()
        
        # Transform
        processed_data = self.transform_user_data(raw_data)
        
        # Load
        analytics = self.load_analytics_data(processed_data)
        
        return analytics
    
    def close(self):
        self.db.close()