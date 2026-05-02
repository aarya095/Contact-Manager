from fastapi.testclient import TestClient

from sqlalchemy import delete 

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.main import app
from app.services.operations import create_contact
from app.services.file_operations import deletes_contact_num_key_in_env_file
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

    #teardown()
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

    logger.debug(data)
    
    assert data['Message'] == "Contact created successfully"
    assert data['contact']['contact_name'] == "aarya"
    assert 'contact_id' in data['contact']
    
    teardown()


def test_get_one_contact_entry():
    """Tests the GET /contacts/{contact_name} endpoint"""

    #teardown()
    setup()
    contact_name = "Aarya"
    response = client.get(f"/contacts/{contact_name}")    
    assert response.status_code == 200
    data = response.json()
    assert data['contact_name'] == "Aarya"
    assert data['contact_number'] == 9876543210
    print(data)
    teardown()


def setup():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    create_contact(contact_name="Aarya",
                   contact_number=9876543210,
                   db=db)
    
def setup_for_testing_get_all_contact_entries():
    Base.metadata.create_all(engine)
    db = SessionLocal()
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

    deletes_contact_num_key_in_env_file(name="aarya")

if __name__ == "__main__":
    test_create_contact()