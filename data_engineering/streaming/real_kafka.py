import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import threading
import time

class RealKafkaProcessor:
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None
        self.is_running = False
        self.processed_events = []
        self.topics = ['user_events', 'system_events', 'analytics_events']
        
        # Initialize Kafka connections
        self._init_producer()
        self._init_consumer()
    
    def _init_producer(self):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',  # Wait for all replicas
                retries=3,
                batch_size=16384,
                linger_ms=10
            )
            print("✅ Kafka Producer initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Kafka Producer: {e}")
            self.producer = None
    
    def _init_consumer(self):
        """Initialize Kafka consumer"""
        try:
            self.consumer = KafkaConsumer(
                *self.topics,
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                group_id='analytics_group',
                auto_offset_reset='latest',
                enable_auto_commit=True
            )
            print("✅ Kafka Consumer initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Kafka Consumer: {e}")
            self.consumer = None
    
    def publish_event(self, event_type: str, data: dict, topic: str = 'user_events'):
        """Publish event to Kafka topic"""
        if not self.producer:
            print("❌ Kafka Producer not available")
            return False
        
        try:
            event = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'data': data
            }
            
            # Send to Kafka
            future = self.producer.send(
                topic=topic,
                key=event_type,
                value=event
            )
            
            # Wait for confirmation
            record_metadata = future.get(timeout=10)
            
            print(f"✅ Event published to Kafka: {event_type} -> {topic}")
            print(f"   Topic: {record_metadata.topic}")
            print(f"   Partition: {record_metadata.partition}")
            print(f"   Offset: {record_metadata.offset}")
            
            return True
            
        except KafkaError as e:
            print(f"❌ Kafka error publishing event: {e}")
            return False
        except Exception as e:
            print(f"❌ Error publishing event: {e}")
            return False
    
    def start_consuming(self):
        """Start consuming events from Kafka"""
        if not self.consumer:
            print("❌ Kafka Consumer not available")
            return
        
        self.is_running = True
        consumer_thread = threading.Thread(target=self._consume_events)
        consumer_thread.daemon = True
        consumer_thread.start()
        print("✅ Kafka Consumer started")
    
    def _consume_events(self):
        """Background thread to consume Kafka events"""
        while self.is_running:
            try:
                # Poll for messages
                message_batch = self.consumer.poll(timeout_ms=1000)
                
                for topic_partition, messages in message_batch.items():
                    for message in messages:
                        self._process_kafka_message(message)
                        
            except Exception as e:
                print(f"❌ Error consuming Kafka messages: {e}")
                time.sleep(5)  # Wait before retrying
    
    def _process_kafka_message(self, message):
        """Process individual Kafka message"""
        try:
            processed_event = {
                'topic': message.topic,
                'partition': message.partition,
                'offset': message.offset,
                'key': message.key,
                'value': message.value,
                'timestamp': message.timestamp,
                'processed_at': datetime.now().isoformat()
            }
            
            # Store processed event
            self.processed_events.append(processed_event)
            
            # Keep only last 1000 events
            if len(self.processed_events) > 1000:
                self.processed_events = self.processed_events[-1000:]
            
            print(f"✅ Processed Kafka message: {message.value.get('event_type', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Error processing Kafka message: {e}")
    
    def stop_consuming(self):
        """Stop consuming events"""
        self.is_running = False
        if self.consumer:
            self.consumer.close()
        print("🛑 Kafka Consumer stopped")
    
    def get_kafka_stats(self) -> dict:
        """Get Kafka statistics"""
        try:
            stats = {
                'kafka_status': 'connected' if self.producer and self.consumer else 'disconnected',
                'producer_status': 'active' if self.producer else 'inactive',
                'consumer_status': 'active' if self.consumer else 'inactive',
                'is_consuming': self.is_running,
                'total_processed_events': len(self.processed_events),
                'bootstrap_servers': self.bootstrap_servers,
                'topics': self.topics,
                'recent_events_count': len([e for e in self.processed_events 
                                          if (datetime.now() - datetime.fromisoformat(e['processed_at'])).seconds < 300])
            }
            
            # Get event types from recent events
            recent_events = [e for e in self.processed_events 
                           if (datetime.now() - datetime.fromisoformat(e['processed_at'])).seconds < 300]
            
            event_types = {}
            for event in recent_events:
                event_type = event['value'].get('event_type', 'unknown')
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            stats['recent_event_types'] = event_types
            
            return stats
            
        except Exception as e:
            return {
                'kafka_status': 'error',
                'error': str(e),
                'bootstrap_servers': self.bootstrap_servers
            }
    
    def get_recent_events(self, limit: int = 10) -> List[dict]:
        """Get recent Kafka events"""
        return self.processed_events[-limit:] if self.processed_events else []
    
    def health_check(self) -> dict:
        """Kafka health check"""
        try:
            # Try to get cluster metadata
            if self.producer:
                metadata = self.producer.bootstrap_connected()
                return {
                    'status': 'healthy' if metadata else 'unhealthy',
                    'producer_connected': bool(self.producer),
                    'consumer_connected': bool(self.consumer),
                    'consuming': self.is_running
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': 'Producer not initialized'
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Global Kafka processor instance
real_kafka_processor = RealKafkaProcessor()