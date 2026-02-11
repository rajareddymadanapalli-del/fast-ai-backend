import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.worker import celery_app

app = FastAPI(title="FastAI AWS Ready")

class TaskRequest(BaseModel):
    data: str

@app.get("/health")
async def health():
    # AWS Load Balancers need a health check endpoint
    return {"status": "healthy"}

@app.post("/run-task")
async def run_task(payload: TaskRequest):
    try:
        task = celery_app.send_task("app.worker.heavy_lifting_task", args=[payload.data])
        return {"task_id": task.id, "status": "dispatched"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
