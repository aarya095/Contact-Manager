from app.services.auth import (
    verify_password, get_password_hash,
)


def test_verify_correct_password():

    password = "my_password"

    hashed = get_password_hash(password)

    assert verify_password(password, hashed)


def test_verify_incorrect_password():

    hashed = get_password_hash("my_password")

    assert not verify_password("wrong_password", hashed)


def test_hashes_are_different_for_same_password():

    password = "my_password"

    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    assert hash1 != hash2