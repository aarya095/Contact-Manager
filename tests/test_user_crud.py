from sqlalchemy import delete, select 
from sqlalchemy.orm import Session

from app.database.user_db_operations import (
    insert_user, 
    get_user_by_id,
    get_all_users,
    )
from app.database.models import User

import logging

logger = logging.getLogger(__name__)


def test_create_user(db_session: Session):
    user = insert_user(
        db = db_session,
        username = "testuser",
        password_hash = "hashed_password",
    )

    saved_user = db_session.scalar(
        select(User).where(User.user_id == user.user_id)
    )

    assert saved_user is not None
    assert saved_user.username == "testuser"
    assert saved_user.password_hash == "hashed_password"

def test_get_user_by_id(db_session: Session):
    # Arrange
    created_user = insert_user(
        db = db_session,
        username = "testuser",
        password_hash = "hashed_password",
    )

    # Act
    retrieved_user = get_user_by_id(
        user_id = created_user.user_id,
        db = db_session,
    )

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.user_id == created_user.user_id
    assert retrieved_user.username == created_user.username
    assert retrieved_user.password_hash == created_user.password_hash

    # Cleanup
    db_session.delete(created_user)
    db_session.commit()

def test_get_all_users(db_session):

    user1 = User(
        username="alice",
        password_hash="hash1",
    )
    user2 = User(
        username="bob",
        password_hash="hash2",
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    users = get_all_users(db_session)

    assert len(users) == 2
    assert users[0].username == "alice"
    assert users[1].username == "bob"