from celery import Celery
import os
import time

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379")
)

@celery_app.task(name="process_ai_prompt")
def process_ai_prompt(prompt: str):
    # Simulate AI Processing (Phase 2 will replace this with actual LLM calls)
    time.sleep(5) 
    return f"Processed AI Result for: {prompt}"
