from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_simulate_intent():
    payload = {"action": "restart_service", "target": "api-gateway"}
    response = client.post("/api/v1/simulate_intent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert data["recommendation"] in ["safe_to_execute", "requires_approval", "blocked"]
