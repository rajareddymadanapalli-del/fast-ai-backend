from fastapi import FastAPI
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from app.api.ai import router as ai_router
except Exception as e:
    ai_router = None
app = FastAPI()
@app.get('/')
async def root():
    return {'status': 'online', 'v': 'v08-29', 'router': ai_router is not None}
if ai_router:
    app.include_router(ai_router, prefix='/ai')
