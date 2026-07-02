from app.database.models import User

from app.exceptions import UserNotFoundError

from sqlalchemy import select
from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)

def create_user(
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