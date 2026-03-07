from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_report_incident():
    payload = {"service": "api-gateway", "signal_type": "latency", "value": 450}
    response = client.post("/api/v1/report_incident", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "api-gateway"
    assert 0 <= data["reliability"] <= 1
