from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.activity_log import UserActivityLog
from models.user_model import User
from typing import Dict, List, Any
import json

class AnalyticsETL:
    """
    ETL (Extract, Transform, Load) service for processing user activity data
    This service transforms raw activity logs into meaningful analytics
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def extract_daily_login_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Extract daily login statistics for the last N days
        This is used for user engagement analytics dashboard
        """
        # Calculate date range for analysis
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)
        
        # Query successful logins grouped by date
        login_stats = self.db.query(
            func.date(UserActivityLog.timestamp).label('date'),
            func.count(UserActivityLog.id).label('total_logins'),
            func.count(func.distinct(UserActivityLog.user_id)).label('unique_users')
        ).filter(
            and_(
                UserActivityLog.activity_type == 'login',
                func.date(UserActivityLog.timestamp) >= start_date,
                func.date(UserActivityLog.timestamp) <= end_date
            )
        ).group_by(func.date(UserActivityLog.timestamp)).all()
        
        # Transform data into analytics format
        result = []
        for stat in login_stats:
            result.append({
                'date': stat.date.isoformat(),
                'total_logins': stat.total_logins,
                'unique_users': stat.unique_users,
                'avg_logins_per_user': round(stat.total_logins / stat.unique_users, 2) if stat.unique_users > 0 else 0
            })
        
        return result
    
    def extract_user_behavior_patterns(self, user_id: int) -> Dict[str, Any]:
        """
        Extract behavior patterns for a specific user
        This helps in personalization and user experience optimization
        """
        # Get user's activity history
        activities = self.db.query(UserActivityLog).filter(
            UserActivityLog.user_id == user_id
        ).order_by(UserActivityLog.timestamp.desc()).limit(100).all()
        
        if not activities:
            return {"user_id": user_id, "message": "No activity data found"}
        
        # Transform activities into behavior patterns
        activity_counts = {}
        hourly_activity = {}
        device_info = {}
        
        for activity in activities:
            # Count activity types
            activity_type = activity.activity_type
            activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1
            
            # Analyze hourly patterns
            hour = activity.timestamp.hour
            hourly_activity[hour] = hourly_activity.get(hour, 0) + 1
            
            # Extract device information from user agent
            if activity.user_agent:
                # Simple device detection (can be enhanced with proper parsing)
                if 'Mobile' in activity.user_agent:
                    device_type = 'mobile'
                elif 'Tablet' in activity.user_agent:
                    device_type = 'tablet'
                else:
                    device_type = 'desktop'
                device_info[device_type] = device_info.get(device_type, 0) + 1
        
        # Calculate most active hour
        most_active_hour = max(hourly_activity, key=hourly_activity.get) if hourly_activity else None
        
        return {
            'user_id': user_id,
            'total_activities': len(activities),
            'activity_breakdown': activity_counts,
            'most_active_hour': most_active_hour,
            'hourly_distribution': hourly_activity,
            'device_usage': device_info,
            'last_activity': activities[0].timestamp.isoformat() if activities else None
        }
    
    def extract_security_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Extract security-related events for monitoring
        This helps identify suspicious activities and potential threats
        """
        # Calculate time range for security analysis
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Query failed login attempts
        failed_logins = self.db.query(UserActivityLog).filter(
            and_(
                UserActivityLog.activity_type == 'login_failed',
                UserActivityLog.timestamp >= start_time
            )
        ).all()
        
        # Group failed attempts by IP address
        ip_attempts = {}
        username_attempts = {}
        
        for attempt in failed_logins:
            # Count attempts per IP
            ip = attempt.ip_address or 'unknown'
            ip_attempts[ip] = ip_attempts.get(ip, 0) + 1
            
            # Count attempts per username
            if attempt.event_metadata:
                try:
                    metadata = json.loads(attempt.event_metadata)
                    username = metadata.get('username_attempted', 'unknown')
                    username_attempts[username] = username_attempts.get(username, 0) + 1
                except:
                    pass
        
        # Identify potential security threats
        alerts = []
        
        # Alert for multiple failed attempts from same IP
        for ip, count in ip_attempts.items():
            if count >= 5:  # Threshold for suspicious activity
                alerts.append({
                    'type': 'multiple_failed_logins_ip',
                    'severity': 'high' if count >= 10 else 'medium',
                    'ip_address': ip,
                    'attempt_count': count,
                    'description': f'{count} failed login attempts from IP {ip}'
                })
        
        # Alert for multiple attempts on same username
        for username, count in username_attempts.items():
            if count >= 3:
                alerts.append({
                    'type': 'multiple_failed_logins_user',
                    'severity': 'medium',
                    'username': username,
                    'attempt_count': count,
                    'description': f'{count} failed login attempts for user {username}'
                })
        
        return alerts
    
    def extract_api_usage_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Extract API usage statistics for performance monitoring
        This helps optimize API performance and identify popular endpoints
        """
        # Calculate date range
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query API calls
        api_calls = self.db.query(UserActivityLog).filter(
            and_(
                UserActivityLog.activity_type == 'api_call',
                UserActivityLog.timestamp >= start_date
            )
        ).all()
        
        # Transform data for analytics
        endpoint_stats = {}
        method_stats = {}
        status_code_stats = {}
        hourly_distribution = {}
        
        for call in api_calls:
            # Count by endpoint
            endpoint = call.endpoint or 'unknown'
            endpoint_stats[endpoint] = endpoint_stats.get(endpoint, 0) + 1
            
            # Count by HTTP method
            method = call.http_method or 'unknown'
            method_stats[method] = method_stats.get(method, 0) + 1
            
            # Count by status code
            status = call.status_code or 0
            status_code_stats[status] = status_code_stats.get(status, 0) + 1
            
            # Count by hour
            hour = call.timestamp.hour
            hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
        
        # Calculate success rate
        success_calls = sum(count for status, count in status_code_stats.items() if 200 <= status < 300)
        total_calls = len(api_calls)
        success_rate = (success_calls / total_calls * 100) if total_calls > 0 else 0
        
        return {
            'total_api_calls': total_calls,
            'success_rate': round(success_rate, 2),
            'most_popular_endpoints': dict(sorted(endpoint_stats.items(), key=lambda x: x[1], reverse=True)[:10]),
            'http_method_distribution': method_stats,
            'status_code_distribution': status_code_stats,
            'hourly_distribution': hourly_distribution,
            'analysis_period_days': days
        }
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive daily analytics report
        This combines multiple analytics for executive dashboard
        """
        return {
            'report_date': datetime.utcnow().date().isoformat(),
            'login_stats': self.extract_daily_login_stats(1),  # Today's stats
            'security_alerts': self.extract_security_alerts(24),  # Last 24 hours
            'api_usage': self.extract_api_usage_stats(1),  # Today's API usage
            'generated_at': datetime.utcnow().isoformat()
        }