from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app

DATABASE_URL="sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args = {
        "check_same_thread": False
    },
    poolclass = StaticPool
)

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Contact Manager API"