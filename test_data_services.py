#!/usr/bin/env python3
"""
Test script to verify data engineering services
Run this to check if activity logging is working
"""

from db_config import get_db
from models.activity_log import UserActivityLog
from models.user_model import User
from services.analytics_etl import AnalyticsETL

def test_activity_logs():
    """Check if activity logs are being created"""
    db = next(get_db())
    
    print("=== TESTING ACTIVITY LOGS ===")
    
    # Get recent activity logs
    recent_logs = db.query(UserActivityLog).order_by(UserActivityLog.timestamp.desc()).limit(10).all()
    
    if recent_logs:
        print(f"✅ Found {len(recent_logs)} recent activity logs:")
        for log in recent_logs:
            print(f"  - {log.activity_type} | User: {log.user_id} | Time: {log.timestamp}")
    else:
        print("❌ No activity logs found. Try registering/logging in first.")
    
    db.close()

def test_analytics_etl():
    """Test ETL analytics processing"""
    db = next(get_db())
    
    print("\n=== TESTING ANALYTICS ETL ===")
    
    etl = AnalyticsETL(db)
    
    # Test login stats
    login_stats = etl.extract_daily_login_stats(7)
    print(f"✅ Login stats for last 7 days: {len(login_stats)} days with data")
    
    # Test security alerts
    alerts = etl.extract_security_alerts(24)
    print(f"✅ Security alerts in last 24h: {len(alerts)} alerts")
    
    # Test API usage
    api_stats = etl.extract_api_usage_stats(7)
    print(f"✅ API usage stats: {api_stats['total_api_calls']} total calls")
    
    db.close()

def test_user_behavior():
    """Test user behavior analysis"""
    db = next(get_db())
    
    print("\n=== TESTING USER BEHAVIOR ANALYSIS ===")
    
    # Get first user
    user = db.query(User).first()
    if user:
        etl = AnalyticsETL(db)
        behavior = etl.extract_user_behavior_patterns(user.id)
        print(f"✅ User {user.username} behavior analysis:")
        print(f"  - Total activities: {behavior.get('total_activities', 0)}")
        print(f"  - Activity types: {list(behavior.get('activity_breakdown', {}).keys())}")
    else:
        print("❌ No users found. Register a user first.")
    
    db.close()

def show_database_tables():
    """Show what's in the database"""
    db = next(get_db())
    
    print("\n=== DATABASE CONTENTS ===")
    
    # Count users
    user_count = db.query(User).count()
    print(f"👥 Users: {user_count}")
    
    # Count activity logs
    log_count = db.query(UserActivityLog).count()
    print(f"📊 Activity logs: {log_count}")
    
    # Show activity types
    activity_types = db.query(UserActivityLog.activity_type).distinct().all()
    types = [t[0] for t in activity_types]
    print(f"🔍 Activity types: {types}")
    
    db.close()

if __name__ == "__main__":
    print("🚀 Testing Data Engineering Services\n")
    
    show_database_tables()
    test_activity_logs()
    test_analytics_etl()
    test_user_behavior()
    
    print("\n✨ Test completed!")
    print("\n📝 To generate more test data:")
    print("1. Register more users via POST /auth/register")
    print("2. Login with users via POST /auth/login")
    print("3. Call analytics APIs via GET /analytics/*")