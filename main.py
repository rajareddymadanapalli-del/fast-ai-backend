from fastapi import FastAPI
from app.api import ai
import os

app = FastAPI(title="FastAI Backend")

@app.get("/")
async def health():
    return {"status": "online", "db": "connected"}

app.include_router(ai.router, prefix="/ai", tags=["AI"])
