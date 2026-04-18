from app.services.encryption import encrypt, decrypt
from app.services import file_operations as f_ops
from app.database import db_operations as db_ops

def create_contact(
        contact_name: str, 
        contact_number: int
        ):
    """Encrypts the contact number, sends the key to the .env file, and 
    sends the contact data to the database"""

    # Normalizing the updated contact name
    contact_name = contact_name.lower()
    contact_name = contact_name.replace(" ", "")

    encrypted_contact_number, key = encrypt(contact_number)
    db_ops.create_contact_db(contact_name, encrypted_contact_number)
    f_ops.stores_contact_num_key_in_env_file(key, contact_name)

    return contact_name

def view_one_contact_entry(contact_name: str) -> str | int:
    """Retrieves the encrypted contact number from the Database, 
    decrypts it, and returns it"""

    encrypted_contact_number = db_ops.view_contact_by_name(
                                        name = contact_name.lower())

    key_for_contact_number = (
        f_ops.retrieve_contact_num_key_from_env_file(contact_name)
        )
    original_contact_number = decrypt(
        encrypted_contact_number = encrypted_contact_number, 
        key = key_for_contact_number)
    
    return original_contact_number
    
def view_all_contacts() -> dict:
    """Retrieves all the encrypted contact numbers from the Database, 
    decrypts them all, and returns them"""

    contacts_data = db_ops.view_all_contacts()
    decrypted_contacts_data = {}

    for contact_id, contact_data in contacts_data.items():

        contact_name = contact_data['Contact Name']
        encrypted_contact_number = contact_data['Contact Number']

        key_for_contact_number = (
            f_ops.retrieve_contact_num_key_from_env_file(contact_name)
            )
        original_contact_number = decrypt(
            encrypted_contact_number = encrypted_contact_number, 
            key = key_for_contact_number)
        
        decrypted_contacts_data[contact_id] = {
                             'Contact Name': contact_name,
                             'Contact Number': original_contact_number
                            }

    return decrypted_contacts_data

def update_contact_entry(
        old_contact_name: str, 
        updated_contact_name: str | None, 
        updated_contact_number: int | None
        ):
    """Seeks out the old contact info to be updated,
    Encrypts the new contact number, sends the key to the .env file, 
    deletes the old key, and sends the contact data to the database"""

    # Normalizing the updated contact name
    updated_contact_name = updated_contact_name.lower()
    updated_contact_name = updated_contact_name.replace(" ", "")
    
    if updated_contact_name is not None:
        f_ops.deletes_contact_num_key_in_env_file(old_contact_name)

    updated_encrypted_contact_number, key = (
        encrypt(updated_contact_number)
        )
    f_ops.stores_contact_num_key_in_env_file(
        key = key, 
        name = updated_contact_name
        )
    db_ops.update_contact_entry(
        old_contact_name = old_contact_name,
        updated_name = updated_contact_name,
        updated_encrypted_contact_number = updated_encrypted_contact_number
    )

    return updated_contact_name

def delete_contact(
        contact_name: str, 
        ):
    """Deletes the contact entry from the database, also the key in the .env file"""

    # Normalizing the updated contact name
    contact_name = contact_name.lower()
    contact_name = contact_name.replace(" ", "")

    db_ops.delete_contact_db(contact_name)
    f_ops.deletes_contact_num_key_in_env_file(contact_name)
    
    return contact_name

if __name__ == '__main__':
    #view_all_contacts()
    my_var = False
    if not my_var:
        print("Nice")