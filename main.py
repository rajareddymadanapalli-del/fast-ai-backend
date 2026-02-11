from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os

app = FastAPI(title="FastAI Backend")

# 1. HEALTH CHECK (The one that made us 'Healthy')
@app.get("/")
async def health_check():
    return {"status": "online", "version": "1.2.0"}

# 2. LOGIN ROUTE (The one missing in the 404 error)
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "secret":
        # Simplified token for testing (In prod, use jose to sign a real JWT)
        return {"access_token": "test_token_123", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

# 3. DASHBOARD ROUTE
@app.get("/dashboard")
async def dashboard(token: str = Depends(lambda x: "test_token_123")):
    return {"message": "Welcome to the FastAI Dashboard!", "data": "Secure AI Stats"}

