from app.api import login
@app.get("/health")
def health_check():
    return {"status": "healthy", "revision": 13, "service": "fast-ai-backend"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "revision": 13, "service": "fast-ai-backend"}

app.include_router(login.router, tags=['auth'])
