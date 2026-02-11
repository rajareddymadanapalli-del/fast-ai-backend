from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.task import AITask
from app.core.storage import upload_file_to_s3
import os
import time

# Setup Celery
celery_app = Celery("worker", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))

# Setup DB Session
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

@celery_app.task(name="process_ai_prompt")
def process_ai_prompt(prompt: str, task_id: str):
    db = SessionLocal()
    try:
        # 1. Simulate AI Work
        time.sleep(10)
        result_text = f"AI Analysis for '{prompt}': Completed successfully."
        
        # 2. Save Result to a Local Temp File and Upload to S3
        file_path = f"{task_id}.txt"
        with open(file_path, "w") as f:
            f.write(result_text)
        
        s3_url = upload_file_to_s3(file_path, f"reports/{task_id}.txt")
        os.remove(file_path) # Clean up local container storage

        # 3. Update RDS Database
        task = db.query(AITask).filter(AITask.task_id == task_id).first()
        if task:
            task.status = "completed"
            task.result = f"Report saved at: {s3_url}"
            db.commit()
            
    except Exception as e:
        print(f"Worker Error: {e}")
    finally:
        db.close()
