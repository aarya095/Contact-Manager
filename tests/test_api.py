from fastapi.testclient import TestClient
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import select, delete 

from app.database.models import Contact, Base

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.main import app
from app.services.operations import create_contact

# Set up test client 
client = TestClient(app)

# Set up test db
env_file_path = ".env.test"
load_dotenv(dotenv_path = env_file_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
                            bind = engine,
                            autoflush = False,
                            autocommit = False
                            )

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Contact Manager API"


def test_get_one_contact_entry():
    setup()
    contact_name = "Aarya"
    response = client.get(f"/contacts/{contact_name}")    
    assert response.status_code == 200
    data = response.json()
    assert data['contact_name'] == "Aarya"
    assert data['contact_number'] == 5635634634
    print(data)
    teardown()


def setup():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    create_contact(contact_name="Aarya",
                   contact_number=5635634634,
                   db=db)


def teardown():
    db = SessionLocal()
    stmt = delete(Contact)

    db.execute(stmt.execution_options(synchronize_session="fetch"))
    print(f"Cleared table: {Contact.__tablename__}")

    db.commit()
    db.close()

if __name__ == "__main__":
    test_get_one_contact_entry()