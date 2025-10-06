import json
import time
from datetime import datetime
from typing import Dict, List
from threading import Thread
import queue

class StreamProcessor:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.processed_events = []
        self.is_running = False
    
    def publish_event(self, event_type: str, data: dict):
        """Publish event to stream"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        self.event_queue.put(event)
        print(f"Event published: {event_type}")
    
    def process_user_registration(self, user_data: dict):
        """Process user registration event"""
        processed = {
            'user_id': user_data.get('id'),
            'registration_time': datetime.now().isoformat(),
            'email_domain': user_data.get('email', '').split('@')[-1],
            'has_full_name': bool(user_data.get('full_name'))
        }
        return processed
    
    def process_user_login(self, user_data: dict):
        """Process user login event"""
        processed = {
            'user_id': user_data.get('id'),
            'login_time': datetime.now().isoformat(),
            'username': user_data.get('username')
        }
        return processed
    
    def stream_worker(self):
        """Background worker to process streaming events"""
        while self.is_running:
            try:
                # Get event from queue (timeout after 1 second)
                event = self.event_queue.get(timeout=1)
                
                # Process based on event type
                if event['event_type'] == 'user_registration':
                    processed = self.process_user_registration(event['data'])
                elif event['event_type'] == 'user_login':
                    processed = self.process_user_login(event['data'])
                else:
                    processed = event['data']
                
                # Store processed event
                processed_event = {
                    'original_timestamp': event['timestamp'],
                    'processed_timestamp': datetime.now().isoformat(),
                    'event_type': event['event_type'],
                    'processed_data': processed
                }
                
                self.processed_events.append(processed_event)
                
                # Keep only last 1000 events in memory
                if len(self.processed_events) > 1000:
                    self.processed_events = self.processed_events[-1000:]
                
                print(f"Processed event: {event['event_type']}")
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing event: {e}")
    
    def start_streaming(self):
        """Start the streaming processor"""
        self.is_running = True
        worker_thread = Thread(target=self.stream_worker)
        worker_thread.daemon = True
        worker_thread.start()
        print("Stream processor started")
    
    def stop_streaming(self):
        """Stop the streaming processor"""
        self.is_running = False
        print("Stream processor stopped")
    
    def get_real_time_stats(self) -> dict:
        """Get real-time streaming statistics"""
        recent_events = [e for e in self.processed_events 
                        if (datetime.now() - datetime.fromisoformat(e['processed_timestamp'])).seconds < 300]
        
        stats = {
            'total_events_processed': len(self.processed_events),
            'events_last_5_minutes': len(recent_events),
            'queue_size': self.event_queue.qsize(),
            'event_types': {}
        }
        
        # Count event types
        for event in recent_events:
            event_type = event['event_type']
            stats['event_types'][event_type] = stats['event_types'].get(event_type, 0) + 1
        
        return stats
    
    def get_recent_events(self, limit: int = 10) -> List[dict]:
        """Get recent processed events"""
        return self.processed_events[-limit:] if self.processed_events else []

# Global stream processor instance
stream_processor = StreamProcessor()