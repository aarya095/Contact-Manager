# Built-in Modules
import logging

# User-Defined Modules
from app.services.encryption import encrypt, decrypt
from app.database import contact_db_operations as db_ops
from app.schemas import ContactResponse

# External Modules
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


def create_contact(
        owner_id: int,
        contact_name: str, 
        contact_number: int,
        db: Session
        ) -> ContactResponse:
    """
    Encrypts the contact number, sends the key to the .env file, and 
    sends the contact data to the database
    """

    logger.info(f"Creating the entry for {contact_name} in database.")

    # Normalizing the updated contact name
    contact_name = contact_name.lower()
    contact_name = contact_name.replace(" ", "")
    logger.info(f"Creating the contact entry for {contact_name}.\n")

    encrypted_contact_number = encrypt(contact_number)

    contact_data = db_ops.insert_contact(
        owner_id = owner_id,
        contact_name = contact_name, 
        encrypted_contact_number = encrypted_contact_number,
        db = db
        )
    
    logger.info(f"Successfully created the entry for {contact_name} in database.")

    return ContactResponse(
        contact_id = contact_data.contact_id,
        contact_name = contact_data.contact_name,
        contact_number = contact_number,
    )


def get_contact(
        owner_id: int,
        contact_id: str, 
        db: Session
        ) -> ContactResponse:
    """
    Retrieves the encrypted contact number from the Database, 
    decrypts it, and returns it
    """

    logger.info(f"Retrieving the entry for {contact_id} from database.")

    contact_data = db_ops.retrieve_contact_by_id(
        owner_id = owner_id,
        contact_id = contact_id,
        db = db
    )

    original_contact_number = decrypt(
        encrypted_contact_number = contact_data.contact_number
        )

    logger.info(f"Contact number retrieved for {contact_id} successfully!")
    
    return ContactResponse(
        contact_id = contact_data.contact_id,
        contact_name = contact_data.contact_name,
        contact_number = original_contact_number,
    )

    
def list_contacts(owner_id: int, db: Session) -> dict:
    """
    Retrieves all the encrypted contact numbers from the Database, 
    decrypts them all, and returns them
    """

    logger.info("Retrieving all contact entries from database.")

    contacts_data = db_ops.retrieve_all_contacts(owner_id, db)
    decrypted_contacts_data = []

    for contact_data in contacts_data:

        original_contact_number = decrypt(
            encrypted_contact_number = contact_data.contact_number 
        )        
        
        current_contact_data_dictionary = {
                            'contact_id' : contact_data.contact_id,
                            'contact_name': contact_data.contact_name,
                            'contact_number': original_contact_number
                            }
        decrypted_contacts_data.append(current_contact_data_dictionary)

    logger.info("Successfully retrieved all contact entries from database.")

    return decrypted_contacts_data


def update_contact(
        owner_id: int,
        contact_id: int, 
        updated_contact_name: str, 
        updated_contact_number: int,
        db: Session
        ) -> ContactResponse:
    """
    Seeks out the old contact info to be updated,
    Encrypts the new contact number, sends the key to the .env file, 
    deletes the old key, and sends the contact data to the database
    """

    logger.info(f"Updating the entry for {contact_id} in database.")

    # Normalizing the updated contact name
    updated_contact_name = updated_contact_name.lower()
    updated_contact_name = updated_contact_name.replace(" ", "")

    updated_encrypted_contact_number = (
        encrypt(updated_contact_number)
        )
    
    user_to_update = db_ops.update_contact_by_id(
        owner_id = owner_id,
        contact_id = contact_id,
        updated_name = updated_contact_name,
        updated_encrypted_contact_number = updated_encrypted_contact_number,
        db = db
    )

    logger.info(f"Successfully updated the entry for {contact_id} in database.")

    return ContactResponse(
        contact_id = user_to_update.contact_id, 
        contact_name = user_to_update.contact_name, 
        contact_number = updated_contact_number
        )


def delete_contact(
        owner_id: int,
        contact_id: str,
        db: Session 
        ) -> dict:
    """
    Deletes the contact entry from the database, also the key in the .env file
    """

    logger.info(f"Deleting the entry for {contact_id} from database.")

    deleted_contact_data = db_ops.delete_contact_by_id(
        owner_id = owner_id,
        contact_id = contact_id, 
        db = db
        )

    logger.info(f"Successfully deleted the entry for {contact_id} from database.")
    
    return deleted_contact_data

if __name__ == '__main__':
    #view_all_contacts()
    pass