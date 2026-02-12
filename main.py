from fastapi import FastAPI
from pydantic import BaseModel
from celery import Celery
import os

app = FastAPI()

# Redis/Celery Setup
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("tasks", broker=CELERY_BROKER_URL)

class UserSchema(BaseModel):
    email: str
    password: str

@app.get("/")
async def root():
    return {"status": "online", "cloud": "verified", "db": "available"}

@celery_app.task
def background_notification(email: str):
    return f"Notification sent to {email}"
