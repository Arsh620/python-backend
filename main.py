from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes import register_routes
from db_config import init_db, get_db
from services.activity_logger import ActivityLogger
from services.event_streaming import EventPublisher
import time
import asyncio

app = FastAPI(title="User Management API", version="1.0.0")

@app.middleware("http")
async def log_api_requests(request: Request, call_next):
    """
    Middleware to log all API requests for analytics
    This captures API usage patterns for data engineering pipeline
    """
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log API call (skip static files and docs)
    if not request.url.path.startswith(("/static", "/docs", "/openapi.json")):
        try:
            db = next(get_db())
            ActivityLogger.log_api_call(
                db=db,
                request=request,
                status_code=response.status_code
            )
            
            # Publish API call event to Kafka simulation
            asyncio.create_task(EventPublisher.publish_api_event(
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code
            ))
            
            db.close()
        except Exception as e:
            print(f"API logging error: {e}")
    
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"][1:])  # Skip 'body'
        errors.append(f"{field}: {error['msg']}")
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": errors,
            "required_fields": "email, username, password" if "register" in str(request.url) else "username, password"
        }
    )

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

register_routes(app)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "User Management API is running!"}