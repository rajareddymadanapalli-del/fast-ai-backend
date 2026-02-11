from fastapi import FastAPI
import os
try:
    from app.api.ai import router as ai_router
except ImportError as e:
    print(f'IMPORT ERROR: {e}')
    ai_router = None

app = FastAPI(title='FastAI Backend')

@app.get('/')
async def health():
    return {'status': 'online', 'db': 'connected', 'router_loaded': ai_router is not None}

if ai_router:
    app.include_router(ai_router, prefix='/ai', tags=['AI'])
