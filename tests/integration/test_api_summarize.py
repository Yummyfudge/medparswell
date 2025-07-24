import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_summarize_endpoint_returns_summary():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/summarize", json={"content": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
    # Optionally check for a placeholder or expected content in summary
    assert "summary" in data["summary"].lower() or len(data["summary"]) > 0