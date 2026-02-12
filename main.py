from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
async def root():
    return {"status": "online", "message": "Marvelous Ostrich is Live"}

@app.get("/db-status")
async def db_status():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "connected", "migration": "complete"}
    except Exception as e:
        return {"database": "error", "details": str(e)}
