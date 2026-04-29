from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.database.database import get_db
from app.database.models import Base, Contact

DATABASE_URL="sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args = {
        "check_same_thread": False
    },
    poolclass = StaticPool
)
TestingSessionLocal = sessionmaker(
                bind = engine,
                autoflush = False,
                autocommit = False
                )


def override_get_db():
    """Dependency to get the testing database session"""
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Contact Manager API"


def test_get_one_contact_entry():
    contact_name = "Aarya Sarfare"
    response = client.get(f"/contacts/{contact_name}")
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)


def setup():
    Base.metadata.create_all(bind=engine)

    #create test contact entry
    session = TestingSessionLocal()
    contact_data = Contact(
        contact_name = "Aarya Sarfare",
        contact_number = "0000000000"
    )
    session.add(contact_data)
    session.commit()
    session.close()


def teardown():
    Base.metadata.drop_all(bind=engine)