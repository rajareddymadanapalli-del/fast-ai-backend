import os
from celery import Celery

# These will be provided by AWS ECS Environment Variables
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery("worker", broker=BROKER_URL, backend=RESULT_BACKEND)

@celery_app.task(name="app.worker.heavy_lifting_task")
def heavy_lifting_task(data: str):
    return f"AWS Processed: {data}"
