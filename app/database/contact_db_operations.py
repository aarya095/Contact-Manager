from app.database.models import Contact

from app.exceptions import ContactNotFoundError

from sqlalchemy import select
from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)


def insert_contact(
        owner_id: int,
        contact_name: str, 
        encrypted_contact_number: bytes,
        db: Session
        ) -> Contact:
    """Create an entry in the database"""

    contact_data = Contact(
        contact_name = contact_name, 
        contact_number = encrypted_contact_number,
        user_id = owner_id
        )
    
    db.add(contact_data)
    db.commit()
    db.refresh(contact_data)
    
    return contact_data
    

def retrieve_contact_by_id(
                        owner_id: int,
                        contact_id: str, 
                        db: Session
                        ) -> Contact:
    """Retrieves one contact via SQLAlchemy"""

    contact_exists = check_contact_exists(
        owner_id = owner_id,
        contact_id = contact_id, 
        db = db
        )
    
    if not contact_exists:
        logger.exception(f"Contact doesn't exist")
        raise ContactNotFoundError()

    statement = (
        select(Contact)
        .where(Contact.user_id == owner_id)
        .where(Contact.contact_id == contact_id)
        )

    user_to_view = db.scalar(statement)

    return user_to_view
        
    
def retrieve_all_contacts(
        owner_id: int, 
        db: Session
        ) -> list[tuple[Contact]]:
    """Retrieves all the contacts via SQLAlchemy"""

    statement = select(Contact).where(Contact.user_id == owner_id)

    contacts_data = db.execute(statement).all()

    return contacts_data

        
def update_contact_by_id(
        owner_id: int, 
        contact_id: str, 
        db: Session,
        updated_name: str | None = None,
        updated_encrypted_contact_number: bytes | None = None
        ) -> Contact:

    contact_exists = check_contact_exists(
                        id_to_check = contact_id,
                        db = db
                        )
    
    if not contact_exists:
        logger.exception(f"Contact doesn't exist")
        return ContactNotFoundError

    statement = (
        select(Contact)
        .where(Contact.user_id == owner_id)
        .where(Contact.contact_id == contact_id)
        )

    user_to_update = db.scalar(statement)
    
    if user_to_update:
        
        if updated_encrypted_contact_number is not None \
            and updated_encrypted_contact_number != user_to_update.contact_number:
            user_to_update.contact_number = updated_encrypted_contact_number

        if updated_name is not None and \
            updated_name != user_to_update.contact_name:
            user_to_update.contact_name = updated_name

        if updated_name is None and \
            updated_encrypted_contact_number is None:
            raise ValueError(
                "No information is provided to be updated in the database"
                )
        db.commit()
        db.refresh(user_to_update)

    return user_to_update
    
    
def delete_contact_by_id(
        owner_id: int, 
        contact_id: str, 
        db: Session
        ) -> dict:
    """Create an entry in the database"""

    contact_exists = check_contact_exists(
                    owner_id = owner_id,
                    contact_id = contact_id,
                    db = db
                    )
    if not contact_exists:
        logger.exception(f"Contact doesn't exist")
        raise ContactNotFoundError()

    statement = (
        select(Contact)
        .where(Contact.user_id == owner_id)
        .where(Contact.contact_id == contact_id)
        )
    
    user_to_delete = db.scalar(statement = statement)

    deleted_contact_data = {
        "id": user_to_delete.contact_id,
        "contact_name": user_to_delete.contact_name
    }

    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()

    return deleted_contact_data
    

def check_contact_exists(
        owner_id: int, 
        contact_id: int, 
        db: Session
        ) -> bool:
    """Retrieves all the contact names via 
    SQLAlchemy and checks if the contact entry exists"""

    statement = (
        select(Contact)
        .where(Contact.user_id == owner_id)
        .where(Contact.contact_id == contact_id)
        )

    contact_to_find = db.execute(statement).first()

    if contact_to_find:
        logger.info(f"Contact found in the database: {contact_id}")
        return True
    return False
    
    
if __name__ == '__main__':

    #results = view_all_contacts()
    #rint(results)
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from dotenv import load_dotenv

    env_file_path = ".env.dev"
    load_dotenv(dotenv_path = env_file_path)

    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL, echo=True)

    SessionLocal = sessionmaker(
                                bind = engine,
                                autoflush = False,
                                autocommit = False
                                )
    db = SessionLocal()
    #result = check_contact_exists(id_to_check=2, db=db)
    #delete_contact_db(contact_name="aarya",db=db)
    
    result = insert_contact(
        1,
     "umeko",
     b'gAAAAABptliCAHsPyXXjDcQjqtQLoqwiEaIgZ1ZxiZykUGVk1so4Pr4c30AUM-uOIeJmkXURSzd_VQuaFgEhyzAXvAzTDWoxrg==',
     db)
    #result = retrieve_all_contacts(owner_id = 1, db=db)
    #result = retrieve_contact_by_id(owner_id = 1, contact_id=2, db=db)
    print(type(result))
    #logger.debug(f"{result}")
    #user = view_contact_by_name(contact_name="aarya",db=db)
    #name, contact_number = view_contact_by_name("vikas")
    #print(name, contact_number)
    #update_contact_entry("string","india")
    #pass