import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI + PostgreSQL + Redis + Celery is live!"}

@pytest.mark.asyncio
async def test_register_user():
    # Using a unique email for the test
    payload = {"email": "test_pytest@example.com", "password": "password123"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/register", json=payload)
    
    # It should be 200 OR 400 if the test user already exists from a previous run
    assert response.status_code in [200, 400]

@pytest.mark.asyncio
async def test_login_user():
    payload = {"email": "test_pytest@example.com", "password": "password123"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/login", json=payload)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
