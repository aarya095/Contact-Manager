from app.database.database import engine
from app.database.models import Contact
from app.exceptions import ContactNotFoundError, UserAlreadyExistsError

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select, delete

def create_contact_db(
        contact_name: str, 
        encrypted_contact_number: bytes
        ):
    """Create an entry in the database"""

    contact_exists = check_contact_exists(
                    name_to_check = contact_name
                    )

    if not contact_exists:
        with Session(engine) as session:
            contact_data = Contact(
                contact_name = contact_name, 
                contact_number = encrypted_contact_number
                )
            session.add(contact_data)
            session.commit()

    if contact_exists:
        raise UserAlreadyExistsError()

def check_contact_exists(name_to_check: str):
    """Retrieves all the contact names via 
    SQLAlchemy and checks if the contact entry exists"""

    Session = sessionmaker(bind=engine)
    session = Session()
    stmt = select(Contact)

    results = session.execute(stmt).all()
    print(f"Result is as follows = {results}\n")
    list_of_contact_names = []

    for row in results:
        # row is a Row object, you can access the User object directly
        contact_entry = row[0]
        list_of_contact_names.append(contact_entry.contact_name)

    session.close()

    if name_to_check in list_of_contact_names:
        return True
    if name_to_check not in list_of_contact_names:
        return False
    
def view_all_contacts() -> dict:
    """Retrieves all the contacts via SQLAlchemy"""

    Session = sessionmaker(bind=engine)
    session = Session()
    stmt = select(Contact)

    results = session.execute(stmt).all()

    session.close()

    contacts_data = {}
    # Cleaning the data
    for row in results:
        contact_data = row[0]
        contacts_data[contact_data.contact_id] = {
                        'Contact Name': contact_data.contact_name,
                        'Contact Number': contact_data.contact_number
                         }
    return contacts_data

def view_contact_by_name(name: str):
    """Retrieves one contact via SQLAlchemy"""

    contact_exists = check_contact_exists(name_to_check = name)

    if contact_exists:

        Session = sessionmaker(bind=engine)
        session = Session()
        stmt = select(Contact)

        results = session.execute(stmt).all()
        print(f"Result is as follows = {results}\n")

        for row in results:
            contact_entry = row[0]
            if contact_entry.contact_name == name:
                return contact_entry.contact_number

        session.close()

    if not contact_exists:
        raise ContactNotFoundError()
    
def update_contact_entry(
        old_contact_name: str, 
        updated_name: str | None = None,
        updated_encrypted_contact_number: bytes | None = None
    ):

    contact_exists = check_contact_exists(
                        name_to_check = old_contact_name
                        )

    if contact_exists:

        with Session(engine) as session:

            user_to_update = session.query(Contact).filter_by(contact_name = old_contact_name)

            if user_to_update:
                
                if updated_encrypted_contact_number is not None:
                    user_to_update.contact_number = updated_encrypted_contact_number

                if updated_name is not None:
                    user_to_update.contact_name = updated_name

                if updated_name is None and \
                    updated_encrypted_contact_number is None:
                    raise ValueError("No information is provided " \
                    "to be updated in the database")

    if not contact_exists:
        return ContactNotFoundError

def empty_database_tables():

    Session = sessionmaker(bind=engine)
    session = Session() 
    stmt = delete(Contact)

    session.execute(stmt.execution_options(synchronize_session="fetch"))
    print(f"Cleared table: {Contact.__tablename__}")

    session.commit()
    
if __name__ == '__main__':
    #create_contact_db(
    # "aarya",
    # b'gAAAAABptliCAHsPyXXjDcQjqtQLoqwiEaIgZ1ZxiZykUGVk1so4Pr4c30AUM-uOIeJmkXURSzd_VQuaFgEhyzAXvAzTDWoxrg==')
    results = view_all_contacts()
    print(results)
    empty_database_tables()
    #view_all_contacts()
    #name, contact_number = view_contact_by_name("vikas")
    #print(name, contact_number)
    #update_contact_entry("india")
    #pass