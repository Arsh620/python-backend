from fastapi import APIRouter
from routers import auth, users, analytics, test_logging, fix_table, pandas_demo, advanced_analytics, kafka_status, real_kafka_status

def register_routes(app):
    # Authentication routes
    app.include_router(auth.router)
    
    # User routes  
    app.include_router(users.router)
    
    # Analytics routes
    app.include_router(analytics.router)
    
    # Test routes
    app.include_router(test_logging.router)
    
    # Fix routes
    app.include_router(fix_table.router)
    
    # Pandas demo routes
    app.include_router(pandas_demo.router)
    
    # Advanced analytics routes
    app.include_router(advanced_analytics.router)
    
    # Kafka simulation monitoring routes
    app.include_router(kafka_status.router)
    
    # Real Kafka monitoring routes
    app.include_router(real_kafka_status.router)