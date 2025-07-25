from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"
    assert "medparswell" in response.json().get("message", "")
