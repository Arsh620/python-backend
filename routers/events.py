from fastapi import APIRouter
from services.event_streaming import event_streamer
from typing import List, Dict, Any

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/recent")
def get_recent_events(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get recent events from Kafka simulation queue
    This shows real-time events being processed
    """
    return event_streamer.get_recent_events(limit)

@router.get("/stats")
def get_event_stats() -> Dict[str, Any]:
    """
    Get statistics about event streaming
    This shows Kafka-like metrics
    """
    events = event_streamer.get_recent_events(1000)
    
    event_types = {}
    for event in events:
        event_type = event.get("event_type", "unknown")
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    return {
        "total_events": len(events),
        "event_types": event_types,
        "consumers_registered": len(event_streamer.consumers),
        "queue_size": len(event_streamer.event_queue)
    }