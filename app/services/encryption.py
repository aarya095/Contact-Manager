# Built-in Modules
import subprocess

# Third Party Modules
from cryptography.fernet import Fernet

# User-defined modules
import app.database.database as db

def encrypt(contact_info: int | str):
    """Encrypts the contact number using fernet a symmmetric cipher"""

    if type(contact_info) == int:
        contact_info = contact_info.to_bytes(8,'big')
    else:
        contact_info = contact_info.encode('utf-8')
        
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_contact_info = f.encrypt(contact_info)

    return encrypted_contact_info, key

def decrypt(encrypted_contact_data: bytes, key: bytes):
    """Decrypts the contact number using fernet a symmmetric cipher"""

    f = Fernet(key)
    original_contact_data = f.decrypt(encrypted_contact_data)

    return original_contact_data

if __name__ == '__main__':
    pass