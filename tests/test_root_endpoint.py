from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint_returns_status_and_message():
    """
    Ensure the root endpoint returns a 200 status and the expected status/message JSON response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "medparswell API is running."
    }