from fastapi.testclient import TestClient

from sqlalchemy import delete 

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.main import app
from app.services.operations import create_contact
from app.database.models import Contact, Base

import logging

logger = logging.getLogger(__name__)

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


def test_create_contact():
    """Tests the POST /contacts endpoint"""

    setup()
    contact_name = "Aarya"
    contact_number = 9876543210

    response = client.post(
        "/contacts/", json = {
            "contact_name": contact_name,
            "contact_number": contact_number
            }
    )

    assert response.status_code == 201
    data = response.json()

    
    assert data['Message'] == "Contact created successfully"
    assert data['contact']['contact_name'] == "aarya"
    assert 'contact_id' in data['contact']
    
    teardown()


def test_get_contact():
    """Tests the GET /contacts/{contact_name} endpoint"""

    setup()
    contact_id = 1

    response = client.get(f"/contacts/{contact_id}")    
    assert response.status_code == 200

    data = response.json()

    assert 'contact_id' in data
    assert data['contact_name'] == "aarya"
    assert data['contact_number'] == 9876543210

    teardown()

def test_list_contacts():
    """Tests the GET /contacts endpoint,
    which fetches all the existing contacts in the db"""

    setup_for_testing_list_contacts()

    response = client.get("/contacts")
    assert response.status_code == 200

    data = response.json()
    print(f"All Data: {data}")

    for contact_data in data:
        assert "contact_id" in contact_data
    
    assert data[0]["contact_name"] == 'aarya'
    assert data[0]["contact_number"] == 9876543210

    assert data[1]["contact_name"] == 'yash'
    assert data[1]["contact_number"] == 1234567890

    assert data[2]["contact_name"] == 'omkar'
    assert data[2]["contact_number"] == 5432167890

    teardown_for_testing_list_contacts()


def test_update_contact():
    """Tests the PUT /contacts/{contact_id} endpoint"""

    setup()

    contact_id = 1

    response = client.put(
        f"/contacts/{contact_id}",
        json = {
            "contact_name": "Omkar",
            "contact_number": 8575975683
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data['Message'] == "Contact updated successfully"
    assert data['contact']['contact_name'] == "omkar"
    assert data['contact']['contact_number'] == 8575975683
    assert 'contact_id' in data['contact']
    
    teardown()


def test_delete_contact():
    """Tests the DELETE /contacts/{contact_id} endpoint"""

    setup()

    contact_id = 1

    response = client.delete(f"/contacts/{contact_id}")

    assert response.status_code == 200
    data = response.json()

    assert data['Message'] == "Contact deleted successfully"
    assert data['contact']['contact_name'] == "aarya"
    assert 'contact_id' in data['contact']
    
    teardown()


def setup():
    
    logger.info("Creating tables for testing.")
    Base.metadata.create_all(engine)

    db = SessionLocal()
    
    logger.info("Inserting data into database")
    create_contact(contact_name="Aarya",
                   contact_number=9876543210,
                   db=db)
    
    
def setup_for_testing_list_contacts():

    logger.info("Creating tables for testing.")
    Base.metadata.create_all(engine)

    db = SessionLocal()

    logger.info("Inserting data into database")
    create_contact(contact_name="Aarya",
                   contact_number=9876543210,
                   db=db)
    create_contact(contact_name="Yash",
                   contact_number=1234567890,
                   db=db)
    create_contact(contact_name="Omkar",
                   contact_number=5432167890,
                   db=db)


def teardown():
    db = SessionLocal()
    stmt = delete(Contact)

    db.execute(stmt.execution_options(synchronize_session="fetch"))
    print(f"Cleared table: {Contact.__tablename__}")

    db.commit()
    db.close()

def teardown_for_testing_list_contacts():
    db = SessionLocal()
    stmt = delete(Contact)

    db.execute(stmt.execution_options(synchronize_session="fetch"))
    print(f"Cleared table: {Contact.__tablename__}")

    db.commit()
    db.close()

if __name__ == "__main__":
    test_delete_contact()