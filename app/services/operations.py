import logging

from app.services.encryption import encrypt, decrypt
from app.services import file_operations as f_ops
from app.database import db_operations as db_ops
from app.schemas import ContactResponse

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def create_contact(
        contact_name: str, 
        contact_number: int,
        db: Session
        ) -> ContactResponse:
    """Encrypts the contact number, sends the key to the .env file, and 
    sends the contact data to the database"""

    logger.info(f"Creating the entry for {contact_name} in database.")

    # Normalizing the updated contact name
    contact_name = contact_name.lower()
    contact_name = contact_name.replace(" ", "")
    logger.info(f"Creating the contact entry for {contact_name}.\n")

    encrypted_contact_number, key = encrypt(contact_number)

    contact_data = db_ops.insert_contact(
                    contact_name = contact_name, 
                    encrypted_contact_number = encrypted_contact_number,
                    db = db)

    f_ops.stores_contact_num_key_in_env_file(key, contact_data.contact_id)
    
    logger.info(f"Successfully created the entry for {contact_name} in database.")

    return ContactResponse(
        contact_id = contact_data.contact_id,
        contact_name = contact_data.contact_name
    )


def get_contact(
                contact_id: str, 
                db: Session
                ) -> dict:
    """Retrieves the encrypted contact number from the Database, 
    decrypts it, and returns it"""

    logger.info(f"Retrieving the entry for {contact_id} from database.")

    contact_data = db_ops.retrieve_contact_by_id(
                                        contact_id = contact_id,
                                        db = db
                                        )

    key_for_contact_number = (
        f_ops.retrieve_contact_num_key_from_env_file(contact_data.contact_id)
        )

    original_contact_number = decrypt(
        encrypted_contact_number = contact_data.contact_number, 
        key = key_for_contact_number)
    
    contact_data_dict = {
        'contact_id': contact_data.contact_id,
        'contact_name': contact_data.contact_name,
        'contact_number': original_contact_number
    }
    
    logger.info(f"Contact number retrieved for {contact_id} successfully!")
    
    return contact_data_dict

    
def list_contacts(db: Session) -> dict:
    """Retrieves all the encrypted contact numbers from the Database, 
    decrypts them all, and returns them"""

    logger.info("Retrieving all contact entries from database.")

    contacts_data = db_ops.retrieve_all_contacts(db)
    decrypted_contacts_data = {}

    for contact_id, contact_data in contacts_data.items():

        contact_name = contact_data['Contact Name']
        encrypted_contact_number = contact_data['Contact Number']

        key_for_contact_number = (
            f_ops.retrieve_contact_num_key_from_env_file(contact_id)
            )
        original_contact_number = decrypt(
            encrypted_contact_number = encrypted_contact_number, 
            key = key_for_contact_number)
        
        decrypted_contacts_data[contact_id] = {
                             'Contact Name': contact_name,
                             'Contact Number': original_contact_number
                            }

    logger.info("Successfully retrieved all contact entries from database.")

    return decrypted_contacts_data


def update_contact(
        contact_id: int, 
        updated_contact_name: str | None, 
        updated_contact_number: int | None,
        db: Session
        ) -> ContactResponse:
    """Seeks out the old contact info to be updated,
    Encrypts the new contact number, sends the key to the .env file, 
    deletes the old key, and sends the contact data to the database"""

    logger.info(f"Updating the entry for {contact_id} in database.")

    # Normalizing the updated contact name
    updated_contact_name = updated_contact_name.lower()
    updated_contact_name = updated_contact_name.replace(" ", "")
    
    if updated_contact_name is not None:
        f_ops.deletes_contact_num_key_in_env_file(contact_id)

    updated_encrypted_contact_number, key = (
        encrypt(updated_contact_number)
        )
    f_ops.stores_contact_num_key_in_env_file(
        key = key, 
        contact_id = contact_id
        )
    user_to_update = db_ops.update_contact_by_id(
        contact_id = contact_id,
        updated_name = updated_contact_name,
        updated_encrypted_contact_number = updated_encrypted_contact_number,
        db = db
    )

    logger.info(f"Successfully updated the entry for {contact_id} in database.")

    return ContactResponse(
        contact_id = user_to_update.contact_id,
        contact_name = user_to_update.contact_name
    )

def delete_contact(
        contact_id: str,
        db: Session 
        ) -> dict:
    """Deletes the contact entry from the database, also the key in the .env file"""

    logger.info(f"Deleting the entry for {contact_id} from database.")

    deleted_contact_data = db_ops.delete_contact_by_id(
                    contact_id = contact_id, 
                    db = db
                    )
    f_ops.deletes_contact_num_key_in_env_file(contact_id)

    logger.info(f"Successfully deleted the entry for {contact_id} from database.")
    
    return deleted_contact_data

if __name__ == '__main__':
    #view_all_contacts()
    my_var = False
    if not my_var:
        print("Nice")