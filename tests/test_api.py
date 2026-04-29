from fastapi.testclient import TestClient

from app.main import app

# Set up test client 
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Contact Manager API"
