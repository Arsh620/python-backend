from fastapi import APIRouter
from data_engineering.streaming.real_kafka import real_kafka_processor

router = APIRouter(prefix="/real-kafka", tags=["real-kafka"])

@router.get("/status")
def real_kafka_status():
    """Check real Kafka system status"""
    try:
        stats = real_kafka_processor.get_kafka_stats()
        return {
            "success": True,
            "real_kafka": stats
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/health")
def real_kafka_health():
    """Real Kafka health check"""
    try:
        health = real_kafka_processor.health_check()
        return {
            "success": True,
            "kafka_health": health
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/test-event")
def test_real_kafka_event():
    """Test event publishing to real Kafka"""
    try:
        test_data = {
            "test_id": 123,
            "message": "Real Kafka test event",
            "timestamp": "2024-01-01T12:00:00"
        }
        
        success = real_kafka_processor.publish_event("test_event", test_data, "system_events")
        
        return {
            "success": success,
            "message": "Test event published to real Kafka" if success else "Failed to publish to Kafka",
            "event_data": test_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/recent-events")
def get_real_kafka_events(limit: int = 10):
    """Get recent events from real Kafka"""
    try:
        events = real_kafka_processor.get_recent_events(limit)
        return {
            "success": True,
            "recent_events": events,
            "count": len(events),
            "note": "Events from real Apache Kafka"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/start-consumer")
def start_kafka_consumer():
    """Start Kafka consumer"""
    try:
        real_kafka_processor.start_consuming()
        return {
            "success": True,
            "message": "Kafka consumer started"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/stop-consumer")
def stop_kafka_consumer():
    """Stop Kafka consumer"""
    try:
        real_kafka_processor.stop_consuming()
        return {
            "success": True,
            "message": "Kafka consumer stopped"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }