from fastapi import FastAPI
import sys
import os

# Diagnostic: List files to see what actually exists in the container
files_in_root = os.listdir('.')
app_exists = os.path.exists('app')
api_exists = os.path.exists('app/api')

try:
    from app.api.ai import router as ai_router
    import_error = None
except Exception as e:
    import_error = str(e)
    ai_router = None

app = FastAPI(title="FastAI Backend")

@app.get("/")
async def health():
    return {
        "status": "online", 
        "router_loaded": ai_router is not None,
        "import_error": import_error,
        "files_found": files_in_root,
        "app_folder_detected": app_exists,
        "api_folder_detected": api_exists
    }

if ai_router:
    app.include_router(ai_router, prefix="/ai", tags=["AI"])

# Cache-breaker: 20260211215416
