from app.database.models import Contact

from app.exceptions import ContactNotFoundError, UserAlreadyExistsError

from sqlalchemy import select, delete 
from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)


def insert_contact(
        contact_name: str, 
        encrypted_contact_number: bytes,
        db: Session
        ) -> Contact:
    """Create an entry in the database"""

    with db as session:
        contact_data = Contact(
            contact_name = contact_name, 
            contact_number = encrypted_contact_number
            )
        session.add(contact_data)
        session.commit()
        session.refresh(contact_data)
    
    return contact_data
    

def retrieve_contact_by_id(
                        contact_name: str, 
                        db: Session
                        ) -> Contact:
    """Retrieves one contact via SQLAlchemy"""

    contact_exists = check_contact_exists(name_to_check = contact_name, 
                                          db = db)
    
    if not contact_exists:
        logger.exception(f"User doesn't exist: {contact_name}")
        raise ContactNotFoundError()

    stmt = select(Contact).where(Contact.contact_name == contact_name)

    user_to_view = db.execute(stmt).first()
    user_to_view = user_to_view[0]

    return user_to_view
        
    
def retrieve_all_contacts(db: Session) -> list[tuple[Contact]]:
    """Retrieves all the contacts via SQLAlchemy"""

    stmt = select(Contact)

    contacts_data = db.execute(stmt).all()

    return contacts_data

        
def update_contact_by_id(
                    old_contact_name: str, 
                    db: Session,
                    updated_name: str | None = None,
                    updated_encrypted_contact_number: bytes | None = None
                ) -> Contact:

    contact_exists = check_contact_exists(
                        name_to_check = old_contact_name,
                        db = db
                        )
    
    if not contact_exists:
        logger.exception(f"User doesn't exist: {old_contact_name}")
        return ContactNotFoundError

    stmt = select(Contact).filter_by(
        contact_name = old_contact_name
        )
    user_to_update_tuple = db.execute(statement = stmt).one()
    user_to_update = user_to_update_tuple[0]
    
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
        contact_name: str, 
        db: Session
        ) -> dict:
    """Create an entry in the database"""

    contact_exists = check_contact_exists(
                    name_to_check = contact_name,
                    db = db
                    )
    if not contact_exists:
        logger.exception(f"User doesn't exist: {contact_name}")
        raise ContactNotFoundError()

    stmt = select(Contact).filter_by(
            contact_name = contact_name
                )
    user_to_delete_tuple = db.execute(statement = stmt).one()
    user_to_delete = user_to_delete_tuple[0]

    deleted_contact_data = {
        "id": user_to_delete.contact_id,
        "contact_name": user_to_delete.contact_name
    }

    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()

    return deleted_contact_data
    

def empty_database_tables(db: Session):

    logger.info("Starting to empty the database.")
    stmt = delete(Contact)

    db.execute(stmt.execution_options(synchronize_session="fetch"))

    db.commit()
    logger.info("Database has been emptied successfully.")


def check_contact_exists(id_to_check: int, db: Session):
    """Retrieves all the contact names via 
    SQLAlchemy and checks if the contact entry exists"""

    stmt = select(Contact).filter_by(contact_id = id_to_check)

    user_to_find = db.execute(stmt).first()

    if user_to_find:
        logger.info(f"User found in the database: {id_to_check}")
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
    #empty_database_tables(db=db)
    
    #insert_contact(
    # "umeko",
    # b'gAAAAABptliCAHsPyXXjDcQjqtQLoqwiEaIgZ1ZxiZykUGVk1so4Pr4c30AUM-uOIeJmkXURSzd_VQuaFgEhyzAXvAzTDWoxrg==',
    # db)
    #result = retrieve_all_contacts(db=db)
    #print(result)
    #logger.debug(f"{result}")
    #user = view_contact_by_name(contact_name="aarya",db=db)
    #name, contact_number = view_contact_by_name("vikas")
    #print(name, contact_number)
    #update_contact_entry("string","india")
    #pass