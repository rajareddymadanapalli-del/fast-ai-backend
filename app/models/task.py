from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AITask(Base):
    __tablename__ = "ai_tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String, default="pending")
    prompt = Column(Text)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
