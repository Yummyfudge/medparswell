import pytest
import httpx

@pytest.mark.asyncio
async def test_summarize_endpoint_returns_summary():
    # Integration test: expects FastAPI server running at localhost:8000
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/summarize", json={"content": "What is the capital of France?"})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert isinstance(data["summary"], str)
        assert "summary" in data["summary"].lower() or len(data["summary"]) > 0