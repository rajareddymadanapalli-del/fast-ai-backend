import pytest
from httpx import AsyncClient
from main import app  # Adjust if your entry file is named differently

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/db-status")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"

def test_pydantic_models():
    # Example: Ensure your Pydantic validation logic works
    from models import UserSchema # Adjust based on your actual model names
    data = {"email": "test@example.com", "password": "securepassword"}
    user = UserSchema(**data)
    assert user.email == "test@example.com"
