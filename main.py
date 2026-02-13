from fastapi import FastAPI
from worker import process_ai_task
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online", "message": "Welcome to the Marvelous Ostrich AI"}

@app.post("/process/{item_id}")
async def trigger_task(item_id: str):
    # This sends the task to Redis for the Celery worker to find
    task = process_ai_task.delay(item_id)
    return {"task_id": task.id, "status": "Queued", "message": f"Task for {item_id} is being processed background."}

@app.get("/db-status")
async def db_status():
    return {"database": "connected", "status": "healthy"}
