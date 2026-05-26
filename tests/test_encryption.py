from cryptography.fernet import InvalidToken
import pytest
from app.services import encryption 

def test_encryption_decryption_process():
    """Tests the encryption and decryption process"""
    contact_info = 989463872
    encrypted_contact_info = encryption.encrypt(contact_info)
    original_contact_info = encryption.decrypt(encrypted_contact_info)

    assert original_contact_info == contact_info

if __name__ == '__main__':
    test_encryption_decryption_process()