from app.database.models import Contact

from app.exceptions import ContactNotFoundError, UserAlreadyExistsError

from sqlalchemy import select, delete 
from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)


def create_contact_db(
        contact_name: str, 
        encrypted_contact_number: bytes,
        db: Session
        ):
    """Create an entry in the database"""

    contact_exists = check_contact_exists(
                    name_to_check = contact_name,
                    db = db
                    )

    if not contact_exists:
        with db as session:
            contact_data = Contact(
                contact_name = contact_name, 
                contact_number = encrypted_contact_number
                )
            session.add(contact_data)
            session.commit()

    if contact_exists:
        logger.exception(f"User already exists: {contact_name}")
        raise UserAlreadyExistsError()
    
    
def view_all_contacts(db: Session) -> dict:
    """Retrieves all the contacts via SQLAlchemy"""

    stmt = select(Contact)

    results = db.execute(stmt).all()

    contacts_data = {}
    # Cleaning the data
    for row in results:
        contact_data = row[0]
        contacts_data[contact_data.contact_id] = {
                        'Contact Name': contact_data.contact_name,
                        'Contact Number': contact_data.contact_number
                         }
        
    return contacts_data


def view_contact_by_name(
                        contact_name: str, 
                        db: Session
                        ):
    """Retrieves one contact via SQLAlchemy"""

    contact_exists = check_contact_exists(name_to_check = contact_name, 
                                          db = db)

    if contact_exists:

        stmt = select(Contact)

        results = db.execute(stmt).all()

        for row in results:
            contact_entry = row[0]
            if contact_entry.contact_name == contact_name:
                logger.info(f"Successfully retrieved the entry for {contact_name} from database.")
                return contact_entry.contact_number

    if not contact_exists:
        logger.exception(f"User doesn't exist: {contact_name}")
        raise ContactNotFoundError()
    
    
def update_contact_entry(
                    old_contact_name: str, 
                    db: Session,
                    updated_name: str | None = None,
                    updated_encrypted_contact_number: bytes | None = None
                ):

    contact_exists = check_contact_exists(
                        name_to_check = old_contact_name,
                        db = db
                        )

    if contact_exists:

        stmt = db.query(Contact).filter_by(
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

    if not contact_exists:
        logger.exception(f"User doesn't exist: {old_contact_name}")
        return ContactNotFoundError
    
    
def delete_contact_db(
        contact_name: str, 
        db: Session
        ):
    """Create an entry in the database"""

    contact_exists = check_contact_exists(
                    name_to_check = contact_name,
                    db = db
                    )

    if contact_exists:

        stmt = db.query(Contact).filter_by(
        contact_name = contact_name
            )
        user_to_delete_tuple = db.execute(statement = stmt).one()
        user_to_delete = user_to_delete_tuple[0]

        if user_to_delete:
            db.delete(user_to_delete)
            db.commit()

    if not contact_exists:
        logger.exception(f"User doesn't exist: {contact_name}")
        raise ContactNotFoundError()
    

def empty_database_tables(db: Session):

    logger.info("Starting to empty the database.")
    stmt = delete(Contact)

    db.execute(stmt.execution_options(synchronize_session="fetch"))
    print(f"Cleared table: {Contact.__tablename__}")

    db.commit()
    logger.info("Database has been emptied successfully.")


def check_contact_exists(name_to_check: str, db: Session):
    """Retrieves all the contact names via 
    SQLAlchemy and checks if the contact entry exists"""

    stmt = select(Contact)

    results = db.execute(stmt).all()
    list_of_contact_names = []

    for row in results:
        # row is a Row object, you can access the User object directly
        contact_entry = row[0]
        list_of_contact_names.append(contact_entry.contact_name)

    if name_to_check in list_of_contact_names:
        logger.info(f"User found in the database: {name_to_check}")
        return True
    if name_to_check not in list_of_contact_names:
        logger.info(f"Uesr not found in the database: {name_to_check}")
        return False
    
    
if __name__ == '__main__':
    #create_contact_db(
    # "aarya",
    # b'gAAAAABptliCAHsPyXXjDcQjqtQLoqwiEaIgZ1ZxiZykUGVk1so4Pr4c30AUM-uOIeJmkXURSzd_VQuaFgEhyzAXvAzTDWoxrg==')
    #results = view_all_contacts()
    #rint(results)
    empty_database_tables()
    #view_all_contacts()
    #name, contact_number = view_contact_by_name("vikas")
    #print(name, contact_number)
    #update_contact_entry("string","india")
    #pass