@app.get("/health")
def health_check():
    return {"status": "healthy", "revision": 13, "service": "fast-ai-backend"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "revision": 13, "service": "fast-ai-backend"}
