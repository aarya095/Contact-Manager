from app.database.models import User

from app.exceptions import UserNotFoundError

from sqlalchemy import select
from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)

def insert_user(
        db: Session,
        username: str,
        password_hash: str,
    ) -> User:
    """
    Creates a new user in the database.
    """
    
    user = User(
        username=username,
        password_hash=password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(
        user_id: int, 
        db: Session
    ) -> User:
    """
    Retrieve a user by their ID.
    """

    statement = select(User).where(User.user_id == user_id)
    user = db.scalar(statement)

    return user

def get_all_users(db_session: Session) -> list[User]:
    """Return all users from the database."""
    
    statement = select(User)
    users =  db_session.scalars(statement).all()

    return users


def update_user(
        user_id: int,
        db: Session,
        updated_username: str | None = None,
        updated_password_hash: str | None = None,
    ) -> User:
    """Update a user's username and password hash."""

    statement = select(User).where(User.user_id == user_id)
    user = db.scalar(statement)

    if user is None:
        raise ValueError(f"User with ID {user_id} not found.")

    if updated_username is not None:
        user.username = updated_username

    if updated_password_hash is not None:
        user.password_hash = updated_password_hash

    db.commit()
    db.refresh(user)

    return user


def check_user_exists(
        user_id: int, 
        db: Session
        ) -> bool:
    """
    Check whether a user exists in the database.
    """

    statement = select(User.user_id).where(User.user_id == user_id)
    user_to_find = db.execute(statement).first()

    if user_to_find:
        logger.info(f"Contact found in the database: {user_id}")
        return True
    return False