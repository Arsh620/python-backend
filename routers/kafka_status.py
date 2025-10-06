from fastapi import APIRouter
from data_engineering.streaming.stream_processor import stream_processor
import json

router = APIRouter(prefix="/kafka", tags=["kafka-monitoring"])

@router.get("/status")
def kafka_status():
    """Check Kafka-like streaming system status"""
    try:
        stats = stream_processor.get_real_time_stats()
        
        return {
            "success": True,
            "kafka_simulation": {
                "status": "active" if stream_processor.is_running else "inactive",
                "type": "in-memory queue simulation",
                "total_events_processed": stats.get("total_events_processed", 0),
                "queue_size": stats.get("queue_size", 0),
                "events_last_5_minutes": stats.get("events_last_5_minutes", 0),
                "event_types": stats.get("event_types", {}),
                "note": "This is a Kafka-like simulation, not real Kafka"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/test-event")
def test_kafka_event():
    """Test event publishing to Kafka simulation"""
    try:
        # Publish test event
        test_data = {
            "test_id": 123,
            "message": "Kafka test event",
            "timestamp": "2024-01-01T12:00:00"
        }
        
        stream_processor.publish_event("test_event", test_data)
        
        return {
            "success": True,
            "message": "Test event published to Kafka simulation",
            "event_data": test_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/recent-events")
def get_recent_kafka_events(limit: int = 10):
    """Get recent events from Kafka simulation"""
    try:
        events = stream_processor.get_recent_events(limit)
        
        return {
            "success": True,
            "recent_events": events,
            "count": len(events),
            "note": "Events from in-memory Kafka simulation"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/health")
def kafka_health_check():
    """Kafka system health check"""
    try:
        is_running = stream_processor.is_running
        stats = stream_processor.get_real_time_stats()
        
        health_status = "healthy" if is_running else "unhealthy"
        
        return {
            "success": True,
            "kafka_health": {
                "status": health_status,
                "streaming_active": is_running,
                "queue_size": stats.get("queue_size", 0),
                "total_processed": stats.get("total_events_processed", 0),
                "system_type": "Kafka Simulation (In-Memory Queue)",
                "recommendations": [
                    "System is working as Kafka-like event streaming",
                    "For production, consider real Apache Kafka",
                    "Current system handles events in memory"
                ]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }