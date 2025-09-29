from fastapi import APIRouter
from routers import auth, users

def register_routes(app):
    # Authentication routes
    app.include_router(auth.router)
    
    # User routes  
    app.include_router(users.router)