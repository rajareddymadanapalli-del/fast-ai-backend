from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.task import AITask
from app.worker.celery_app import process_ai_prompt
import uuid

router = APIRouter()

# Dependency to get DB session (simpler version for now)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/process")
async def create_task(prompt: str, db: Session = Depends(get_db)):
    task_id = str(uuid.uuid4())
    
    # 1. Record in Database (RDS)
    new_task = AITask(task_id=task_id, prompt=prompt, status="queued")
    db.add(new_task)
    db.commit()
    
    # 2. Push to Queue (Redis/Celery)
    process_ai_prompt.delay(prompt)
    
    return {"task_id": task_id, "status": "queued", "message": "AI is crunching the data!"}
