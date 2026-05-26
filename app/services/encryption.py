# Third Party Modules
from cryptography.fernet import Fernet
from dotenv import load_dotenv

def encrypt(contact_number: int, key = MASTER_KEY) -> bytes:
    """Encrypts the contact number using fernet a symmmetric cipher"""

    contact_number = contact_number.to_bytes(8,'big')   
    
    f = Fernet(key)
    encrypted_contact_number = f.encrypt(contact_number)

    return encrypted_contact_number, key

def decrypt(encrypted_contact_number: bytes, key: bytes = MASTER_KEY) -> int:
    """Decrypts the contact number using fernet a symmmetric cipher"""

    f = Fernet(key)
    original_contact_number_bytes = f.decrypt(encrypted_contact_number)
    original_contact_number = (
        int.from_bytes(original_contact_number_bytes, 'big')
        )

    return original_contact_number

if __name__ == '__main__':
    pass