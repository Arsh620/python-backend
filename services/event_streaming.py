import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class UserEvent:
    """
    Data class representing a user event for streaming
    This standardizes event format for Kafka publishing
    """
    event_type: str  # login, register, api_call, etc.
    user_id: Optional[int]
    timestamp: str
    metadata: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class EventStreaming:
    """
    Event streaming service for real-time data processing
    This simulates Kafka functionality for learning purposes
    In production, this would use actual Kafka client
    """
    
    def __init__(self):
        # In-memory event queue (simulates Kafka topic)
        # In production, this would be replaced with actual Kafka producer
        self.event_queue = []
        self.consumers = []
    
    async def publish_event(self, event: UserEvent):
        """
        Publish event to streaming platform
        In production, this would send to Kafka topic
        """
        try:
            # Convert event to JSON format for streaming
            event_data = {
                "event_type": event.event_type,
                "user_id": event.user_id,
                "timestamp": event.timestamp,
                "metadata": event.metadata,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "published_at": datetime.utcnow().isoformat()
            }
            
            # Add to in-memory queue (simulates Kafka publish)
            self.event_queue.append(event_data)
            
            # Notify consumers (simulates Kafka consumer notification)
            await self._notify_consumers(event_data)
            
            print(f"Event published: {event.event_type} for user {event.user_id}")
            
        except Exception as e:
            print(f"Failed to publish event: {str(e)}")
    
    async def _notify_consumers(self, event_data: Dict[str, Any]):
        """
        Notify all registered consumers about new event
        This simulates Kafka consumer group functionality
        """
        for consumer in self.consumers:
            try:
                await consumer(event_data)
            except Exception as e:
                print(f"Consumer error: {str(e)}")
    
    def register_consumer(self, consumer_func):
        """
        Register a consumer function to process events
        This simulates Kafka consumer registration
        """
        self.consumers.append(consumer_func)
    
    def get_recent_events(self, limit: int = 100) -> list:
        """
        Get recent events from the queue
        This is for monitoring and debugging purposes
        """
        return self.event_queue[-limit:] if self.event_queue else []

# Global event streaming instance
event_streamer = EventStreaming()

# Example consumer functions for different event types
async def login_event_consumer(event_data: Dict[str, Any]):
    """
    Consumer for login events
    This processes login events for real-time analytics
    """
    if event_data["event_type"] == "login":
        print(f"Processing login event for user {event_data['user_id']}")
        # Here you could:
        # - Update real-time dashboard
        # - Send welcome notification
        # - Update user session tracking
        # - Trigger personalization engine

async def security_event_consumer(event_data: Dict[str, Any]):
    """
    Consumer for security-related events
    This processes security events for threat detection
    """
    if event_data["event_type"] in ["login_failed", "register_failed"]:
        print(f"Processing security event: {event_data['event_type']}")
        # Here you could:
        # - Check for brute force attacks
        # - Update security metrics
        # - Send alerts to security team
        # - Block suspicious IPs

async def analytics_event_consumer(event_data: Dict[str, Any]):
    """
    Consumer for analytics events
    This processes all events for business intelligence
    """
    print(f"Processing analytics event: {event_data['event_type']}")
    # Here you could:
    # - Update real-time metrics
    # - Feed machine learning models
    # - Update recommendation systems
    # - Generate business insights

# Register consumers with the event streamer
event_streamer.register_consumer(login_event_consumer)
event_streamer.register_consumer(security_event_consumer)
event_streamer.register_consumer(analytics_event_consumer)

class EventPublisher:
    """
    Helper class to publish events from different parts of the application
    This provides a clean interface for event publishing
    """
    
    @staticmethod
    async def publish_login_event(user_id: int, ip_address: str = None, user_agent: str = None, success: bool = True):
        """
        Publish login event to streaming platform
        """
        event = UserEvent(
            event_type="login" if success else "login_failed",
            user_id=user_id if success else None,
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                "success": success,
                "login_method": "password"
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        await event_streamer.publish_event(event)
    
    @staticmethod
    async def publish_registration_event(user_id: int, ip_address: str = None, user_agent: str = None):
        """
        Publish registration event to streaming platform
        """
        event = UserEvent(
            event_type="register",
            user_id=user_id,
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                "registration_method": "email",
                "user_source": "direct"
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        await event_streamer.publish_event(event)
    
    @staticmethod
    async def publish_api_event(endpoint: str, method: str, user_id: int = None, status_code: int = 200):
        """
        Publish API call event to streaming platform
        """
        event = UserEvent(
            event_type="api_call",
            user_id=user_id,
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code
            }
        )
        await event_streamer.publish_event(event)