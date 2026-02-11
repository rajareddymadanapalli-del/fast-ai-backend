from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.task import AITask
from app.worker.celery_app import process_ai_prompt
import uuid
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()

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
    new_task = AITask(task_id=task_id, prompt=prompt, status="queued")
    db.add(new_task)
    db.commit()
    process_ai_prompt.delay(prompt)
    return {"task_id": task_id, "status": "queued"}

@router.get("/status/{task_id}")
async def get_status(task_id: str, db: Session = Depends(get_db)):
    task = db.query(AITask).filter(AITask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "task_id": task.task_id,
        "status": task.status,
        "prompt": task.prompt,
        "result": task.result,
        "created_at": task.created_at
    }
