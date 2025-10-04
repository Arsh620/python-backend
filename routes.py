from fastapi import APIRouter
from routers import auth, users, analytics, events

def register_routes(app):
    # Authentication routes
    app.include_router(auth.router)
    
    # User routes  
    app.include_router(users.router)
    
    # Analytics routes for data engineering features
    app.include_router(analytics.router)
    
    # Event streaming routes (Kafka simulation)
    app.include_router(events.router)