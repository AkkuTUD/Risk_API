from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_get_risk():
    response = client.post("/risks", json={
        "title": "Test Risk",
        "description": "Test description",
        "category": "Test Category"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Risk"

    response = client.get("/risks")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_risk_id():
    response = client.get("/risks/9999")
    assert response.status_code == 404