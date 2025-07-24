import pytest
import httpx

@pytest.mark.asyncio
async def test_summarize_endpoint_returns_summary():
    base_url = "http://localhost:8000"
    try:
        async with httpx.AsyncClient(base_url=base_url, timeout=2.0) as client:
            response = await client.post("/summarize", json={"content": "What is the capital of France?"})
    except httpx.ConnectError:
        pytest.skip("FastAPI server not running at localhost:8000")

    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
    assert len(data["summary"]) > 0