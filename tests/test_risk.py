from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_risk():
    response = client.get("/api/v1/get_risk")
    assert response.status_code == 200
    data = response.json()
    assert "system_risk" in data
    assert "status" in data
