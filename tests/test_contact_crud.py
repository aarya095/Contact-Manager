from sqlalchemy import select 
from sqlalchemy.orm import Session

from app.database.contact_db_operations import (
    insert_contact,
    retrieve_contact_by_id,
    retrieve_all_contacts,
    update_contact_by_id,
)

from app.database.user_db_operations import (
    insert_user, 
)

from app.database.models import Contact

def test_insert_contact(db_session: Session):

    # Arrange
    username = "test_user"
    password_hash = "hashed_password"

    created_user = insert_user(
        db=db_session,
        username=username,
        password_hash=password_hash,
    )

    contact_name = "John Doe"
    encrypted_contact_number = b"encrypted_phone_number"

    # Act
    created_contact = insert_contact(
        owner_id=created_user.user_id,
        contact_name=contact_name,
        encrypted_contact_number=encrypted_contact_number,
        db=db_session,
    )

    # Assert
    assert created_contact.contact_id is not None
    assert created_contact.contact_name == contact_name
    assert created_contact.contact_number == encrypted_contact_number
    assert created_contact.user_id == created_user.user_id

    stored_contact = (
        db_session.query(Contact)
        .filter(Contact.contact_id == created_contact.contact_id)
        .first()
    )

    assert stored_contact is not None
    assert stored_contact.contact_name == contact_name
    assert stored_contact.contact_number == encrypted_contact_number
    assert stored_contact.user_id == created_user.user_id


def test_retrieve_contact_by_id(db_session: Session):
    # Arrange
    username = "test_user"
    password_hash = "hashed_password"

    created_user = insert_user(
        db=db_session,
        username=username,
        password_hash=password_hash,
    )

    contact_name = "John Doe"
    encrypted_contact_number = b"encrypted_phone_number"

    created_contact = insert_contact(
        owner_id=created_user.user_id,
        contact_name=contact_name,
        encrypted_contact_number=encrypted_contact_number,
        db=db_session,
    )

    # Act
    retrieved_contact = retrieve_contact_by_id(
        owner_id=created_user.user_id,
        contact_id=created_contact.contact_id,
        db=db_session,
    )

    # Assert
    assert retrieved_contact is not None
    assert retrieved_contact.contact_id == created_contact.contact_id
    assert retrieved_contact.contact_name == contact_name
    assert retrieved_contact.contact_number == encrypted_contact_number
    assert retrieved_contact.user_id == created_user.user_id


def test_retrieve_all_contacts(db_session: Session):
    # Arrange
    username = "test_user"
    password_hash = "hashed_password"

    created_user = insert_user(
        db=db_session,
        username=username,
        password_hash=password_hash,
    )

    first_contact = insert_contact(
        owner_id=created_user.user_id,
        contact_name="John Doe",
        encrypted_contact_number=b"encrypted_number_1",
        db=db_session,
    )

    second_contact = insert_contact(
        owner_id=created_user.user_id,
        contact_name="Jane Smith",
        encrypted_contact_number=b"encrypted_number_2",
        db=db_session,
    )

    # Act
    retrieved_contacts = retrieve_all_contacts(
        owner_id=created_user.user_id,
        db=db_session,
    )

    # Assert
    assert len(retrieved_contacts) == 2

    retrieved_contact_ids = {
        contact.contact_id for contact in retrieved_contacts
    }

    assert first_contact.contact_id in retrieved_contact_ids
    assert second_contact.contact_id in retrieved_contact_ids


def test_update_contact_by_id(db_session: Session):
    
    # Arrange
    username = "test_user"
    password_hash = "hashed_password"

    created_user = insert_user(
        db=db_session,
        username=username,
        password_hash=password_hash,
    )

    created_contact = insert_contact(
        owner_id=created_user.user_id,
        contact_name="John Doe",
        encrypted_contact_number=b"encrypted_number",
        db=db_session,
    )

    updated_contact_name = "Jane Doe"
    updated_encrypted_contact_number = b"updated_encrypted_number"

    # Act
    updated_contact = update_contact_by_id(
        owner_id=created_user.user_id,
        contact_id=created_contact.contact_id,
        updated_name=updated_contact_name,
        updated_encrypted_contact_number=updated_encrypted_contact_number,
        db=db_session,
    )

    # Assert
    assert updated_contact.contact_id == created_contact.contact_id
    assert updated_contact.contact_name == updated_contact_name
    assert (
        updated_contact.contact_number
        == updated_encrypted_contact_number
    )
    assert updated_contact.user_id == created_user.user_id