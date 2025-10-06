from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes import register_routes
from db_config import init_db
from data_engineering.streaming.real_kafka import real_kafka_processor

app = FastAPI(title="User Management API with Real Kafka", version="1.0.0")

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
    # Start real Kafka consumer
    try:
        real_kafka_processor.start_consuming()
        print("✅ Real Kafka consumer started")
    except Exception as e:
        print(f"⚠️ Failed to start Kafka consumer: {e}")

@app.on_event("shutdown")
def shutdown_event():
    # Stop real Kafka consumer
    try:
        real_kafka_processor.stop_consuming()
        print("🛑 Real Kafka consumer stopped")
    except Exception as e:
        print(f"⚠️ Error stopping Kafka consumer: {e}")

register_routes(app)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "User Management API with Real Apache Kafka is running!"}