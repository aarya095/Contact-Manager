from cryptography.fernet import Fernet
import subprocess
from dotenv import dotenv_values
import modules.database as db

def encrypt(contact_info):
    """Encrypts the contact number using fernet a symmmetric cipher"""

    key = Fernet.generate_key()
    f= Fernet(key)
    encrypted_contact_info = f.encrypt(contact_info)

    return encrypted_contact_info, key

def decrypt(encrypted_contact_info, key):
    """Decrypts the contact number using fernet a symmmetric cipher"""
    f = Fernet(key)
    original_contact_number = f.decrypt(encrypted_contact_info)

    return original_contact_number

def stores_encrypted_contact_num_in_db(encrypted_contact_info, name):
    """Stores the encrypted_contact_info in the sqlite3 db"""

    conn = db.connect_db()
    cur = conn.cursor()
    cur.execute("update contacts set contact_number = ? where name = ?", (encrypted_contact_info, name))
    conn.commit()
    conn.close()

def stores_encrypted_email_in_db(encrypted_contact_info, name):
    """Stores the encrypted_contact_info in the sqlite3 db"""

    conn = db.connect_db()
    cur = conn.cursor()
    cur.execute("update contacts set email = ? where name = ?", (encrypted_contact_info, name))
    conn.commit()
    conn.close()

def stores_contact_num_key_in_env_file(key, name):
    """Stores the Contact Number key in the .env file"""
    name_of_key = f"KEY_OF_{name.upper()}"
    
    # decoding the key as would store along with the 'b' as prefix in the database
    key_str = key.decode('utf-8') 
    command = f"dotenv set {name_of_key} {key_str}"
    res = subprocess.run(command, shell=True, capture_output=True)

def stores_email_key_in_env_file(key, name):
    """Stores the Email key in the .env file"""
    name_of_key = f"KEY_OF_EMAIL_{name.upper()}"
    
    # decoding the key as would store along with the 'b' as prefix in the database
    key_str = key.decode('utf-8') 
    command = f"dotenv set {name_of_key} {key_str}"
    res = subprocess.run(command, shell=True, capture_output=True)

def retrieve_encrypted_number_from_db(name):
    """Retrieves the encrypted_contact_number from the sqlite3 db"""
    conn = db.connect_db()
    cur = conn.cursor()

    cur.execute("select contact_number from contacts where name = ?", (name,))
    encrypted_contact_number = cur.fetchone()
    conn.commit()
    conn.close()

    return encrypted_contact_number

def retrieve_encrypted_email_from_db(name):
    """Retrieves the encrypted_email from the sqlite3 db"""
    conn = db.connect_db()
    cur = conn.cursor()

    cur.execute("select email from contacts where name = ?", (name,))
    encrypted_email = cur.fetchone()
    conn.commit()
    conn.close()

    return encrypted_email

def retrieve_contact_num_key_from_env_file(name):
    """Retrieves the Contact Number key from the .env file"""
    name_of_key = f"KEY_OF_{name.upper()}"
    dict_of_keys = dotenv_values(".env")

    for key,value in dict_of_keys.items():
        
        if key == name_of_key:
            key_for_contact_number = value
            break
    # encoding the key as decrypt() function expects a bytes object
    key_for_contact_number = key_for_contact_number.encode('utf-8')
    return key_for_contact_number

def retrieve_email_key_from_env_file(name):
    """Retrieves th Email key from the .env file"""
    name_of_key = f"KEY_OF_EMAIL_{name.upper()}"
    dict_of_keys = dotenv_values(".env")

    for key,value in dict_of_keys.items():
        
        if key == name_of_key:
            key_for_email = value
            break
    # encoding the key as decrypt() function expects a bytes object
    key_for_email = key_for_email.encode('utf-8')
    return key_for_email

if __name__ == '__main__':
    pass