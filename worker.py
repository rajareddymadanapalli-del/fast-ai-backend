from celery import Celery
import os

# Get Redis URL from environment (provided by CDK/ECS)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(name="process_ai_task")
def process_ai_task(data):
    # Simulate heavy AI computation
    import time
    time.sleep(10) 
    return {"status": "Task Complete", "result": f"Processed {data}"}
