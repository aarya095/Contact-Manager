from cryptography.fernet import InvalidToken
import pytest
from app.services import encryption 

def test_encryption_decryption_process():

    contact_info = 989463872
    encrypted_contact_info = encryption.encrypt(contact_info)
    original_contact_info = encryption.decrypt(encrypted_contact_info)

    assert original_contact_info == contact_info

def test_encrypt_generates_different_ciphertexts():
    
    contact_number = 9876543210

    encrypted1 = encryption.encrypt(contact_number)
    encrypted2 = encryption.encrypt(contact_number)

    assert encrypted1 != encrypted2