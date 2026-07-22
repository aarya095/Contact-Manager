from cryptography.fernet import InvalidToken
import pytest

from app.services.encryption import encrypt, decrypt 

def test_encryption_decryption_process():

    contact_info = 989463872
    encrypted_contact_info = encrypt(contact_info)
    original_contact_info = decrypt(encrypted_contact_info)

    assert original_contact_info == contact_info

def test_encrypt_generates_different_ciphertexts():

    contact_number = 9876543210

    encrypted1 = encrypt(contact_number)
    encrypted2 = encrypt(contact_number)

    assert encrypted1 != encrypted2

def test_multiple_encryptions_decrypt_to_same_value():
    contact_number = 9876543210

    encrypted1 = encrypt(contact_number)
    encrypted2 = encrypt(contact_number)

    assert decrypt(encrypted1) == contact_number
    assert decrypt(encrypted2) == contact_number


def test_decrypt_invalid_ciphertext():

    with pytest.raises(InvalidToken):
        decrypt(b"this is not a valid fernet token")