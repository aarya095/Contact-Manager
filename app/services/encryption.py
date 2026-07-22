# User-Defined Modules
from config.config import config

# External Modules
from cryptography.fernet import Fernet

def encrypt(contact_number: int) -> bytes:
    """
    Encrypts the contact number using fernet a symmmetric cipher
    """

    contact_number = contact_number.to_bytes(8,'big')   
    
    f = Fernet(config.MASTER_KEY)
    encrypted_contact_number = f.encrypt(contact_number)

    return encrypted_contact_number

def decrypt(encrypted_contact_number: bytes) -> int:
    """
    Decrypts the contact number using fernet a symmmetric cipher
    """

    f = Fernet(config.MASTER_KEY)
    original_contact_number_bytes = f.decrypt(encrypted_contact_number)
    original_contact_number = (
        int.from_bytes(original_contact_number_bytes, 'big')
        )

    return original_contact_number