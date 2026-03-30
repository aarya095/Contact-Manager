from app.services.encryption import encrypt, decrypt
from app.services import file_operations as f_ops
from app.database import db_operations as db_ops

def create_contact(contact_name: str, contact_number: int):
    """Encrypts the contact number, sends the key to the .env file, and sends the contact data to the database"""

    contact_name = contact_name.lower() # Normalizing the contact name
    contact_exists = db_ops.check_contact_exists(contact_name)

    if contact_exists == False:
        encrypted_contact_number, key = encrypt(contact_number)
        f_ops.stores_contact_num_key_in_env_file(key, contact_name)
        db_ops.create_contact_db(contact_name, encrypted_contact_number)
        return contact_name

    elif contact_exists == True:
        return "Null"

def view_one_contact_entry(contact_name: str) -> str | int:
    """Retrieves the encrypted contact number from the Database, decrypts it, and returns it"""

    encrypted_contact_number = db_ops.view_contact_by_name(name = contact_name.lower())

    if encrypted_contact_number != "Null":
        key_for_contact_number = f_ops.retrieve_contact_num_key_from_env_file(contact_name)
        original_contact_number = decrypt(
            encrypted_contact_number = encrypted_contact_number, 
            key = key_for_contact_number)
        
        return original_contact_number
    
    elif encrypted_contact_number == "Null":
        return "Null"
    
def view_all_contacts():
    """Retrieves all the encrypted contact numbers from the Database, decrypts them all, and returns them"""

    contacts_data = db_ops.view_all_contacts()
    decrypted_contacts_data = {}

    for contact_id, contact_data in contacts_data.items():

        contact_name = contact_data['Contact Name']
        encrypted_contact_number = contact_data['Contact Number']

        key_for_contact_number = f_ops.retrieve_contact_num_key_from_env_file(contact_name)
        original_contact_number = decrypt(
            encrypted_contact_number = encrypted_contact_number, 
            key = key_for_contact_number)
        
        decrypted_contacts_data[contact_id] = {
                             'Contact Name': contact_name,
                             'Contact Number': original_contact_number
                            }

    print(decrypted_contacts_data)
    return decrypted_contacts_data

if __name__ == '__main__':
    view_all_contacts()