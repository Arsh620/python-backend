import json
from datetime import datetime
from sqlalchemy.orm import Session
from models.activity_log import UserActivityLog
from fastapi import Request
from typing import Optional, Dict, Any

class ActivityLogger:
    """
    Service class for logging user activities
    This is the core component of our data ingestion pipeline
    """
    
    @staticmethod
    def log_activity(
        db: Session,
        activity_type: str,
        user_id: Optional[int] = None,
        request: Optional[Request] = None,
        description: str = "",
        status_code: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Main method to log user activities
        This method captures all necessary data for analytics
        
        Args:
            db: Database session
            activity_type: Type of activity (login, register, api_call, etc.)
            user_id: ID of the user performing the action
            request: FastAPI request object to extract IP, user-agent, etc.
            description: Human-readable description of the activity
            status_code: HTTP status code of the response
            metadata: Additional data to store as JSON
        """
        try:
            # Extract request information if available
            ip_address = None
            user_agent = None
            http_method = None
            endpoint = None
            
            if request:
                # Get client IP address (handles proxy headers)
                ip_address = request.client.host if request.client else None
                
                # Get user agent for device/browser analytics
                user_agent = request.headers.get("user-agent")
                
                # Get HTTP method and endpoint for API analytics
                http_method = request.method
                endpoint = str(request.url.path)
            
            # Convert metadata to JSON string for storage
            metadata_json = json.dumps(metadata) if metadata else None
            
            # Create the log entry in database
            UserActivityLog.create_log(
                db=db,
                user_id=user_id,
                activity_type=activity_type,
                activity_description=description,
                ip_address=ip_address,
                user_agent=user_agent,
                http_method=http_method,
                endpoint=endpoint,
                status_code=status_code,
                event_metadata=metadata_json
            )
            
        except Exception as e:
            # Don't let logging errors break the main application
            print(f"Activity logging error: {str(e)}")
    
    @staticmethod
    def log_login(db: Session, user_id: int, request: Request, success: bool = True):
        """
        Specialized method for logging login attempts
        This creates structured data for login analytics
        """
        status = "successful" if success else "failed"
        ActivityLogger.log_activity(
            db=db,
            activity_type="login",
            user_id=user_id if success else None,
            request=request,
            description=f"User login {status}",
            status_code=200 if success else 401,
            metadata={"login_success": success}
        )
    
    @staticmethod
    def log_registration(db: Session, user_id: int, request: Request):
        """
        Specialized method for logging user registrations
        This tracks new user acquisition for business analytics
        """
        ActivityLogger.log_activity(
            db=db,
            activity_type="register",
            user_id=user_id,
            request=request,
            description="New user registration",
            status_code=201,
            metadata={"registration_timestamp": datetime.utcnow().isoformat()}
        )
    
    @staticmethod
    def log_api_call(db: Session, request: Request, user_id: Optional[int] = None, status_code: int = 200):
        """
        Specialized method for logging API calls
        This tracks API usage patterns for performance analytics
        """
        ActivityLogger.log_activity(
            db=db,
            activity_type="api_call",
            user_id=user_id,
            request=request,
            description=f"{request.method} {request.url.path}",
            status_code=status_code,
            metadata={
                "query_params": dict(request.query_params),
                "path_params": dict(request.path_params) if hasattr(request, 'path_params') else {}
            }
        )