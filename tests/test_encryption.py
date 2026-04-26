from cryptography.fernet import InvalidToken
import pytest
from app.services import encryption 

def test_encryption_decryption_process():
    """Tests the encryption and decryption process"""
    contact_info = 989463872
    encrypted_contact_info, key = encryption.encrypt(contact_info)
    original_contact_info = encryption.decrypt(encrypted_contact_info, key)

    assert original_contact_info == contact_info

def test_encryption_wrong_key():
    """Tests the encryption and decryption process"""
    contact_info_1 = 9894638723
    contact_info_2 = 1231231231
    encrypted_contact_info_1, key_1 = encryption.encrypt(contact_info_1)
    encrypted_contact_info_2, key_2 = encryption.encrypt(contact_info_2)

    with pytest.raises(InvalidToken):
        encryption.decrypt(encrypted_contact_info_1, key_2)

if __name__ == '__main__':
    test_encryption_decryption_process()