from fastapi import FastAPI
import sys
import os

# Force current directory into path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

try:
    from app.api.ai import router as ai_router
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    ai_router = None

app = FastAPI(title="FastAI Backend")

@app.get("/")
async def health():
    return {
        "status": "online", 
        "router_loaded": ai_router is not None,
        "environment": os.getenv("DATABASE_URL")[:20] if os.getenv("DATABASE_URL") else "None"
    }

if ai_router:
    app.include_router(ai_router, prefix="/ai", tags=["AI"])
