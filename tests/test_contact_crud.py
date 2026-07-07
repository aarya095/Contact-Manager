from sqlalchemy import select 
from sqlalchemy.orm import Session

from app.database.contact_db_operations import (
    insert_contact,
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