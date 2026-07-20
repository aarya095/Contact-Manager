# Built-in Modules
import logging

# User-Defined Modules
from app.database.models import User
from app.exceptions import UserNotFoundError, UserAlreadyExistsError

# External Modules
from sqlalchemy import select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def insert_user(
        db: Session,
        username: str,
        password_hash: str,
    ) -> User:
    """
    Creates a new user in the database.
    """

    logger.info(f"Creating user '{username}'.")

    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user is not None:
        logger.warning(f"User '{username}' already exists.")
        raise UserAlreadyExistsError(
            f"Username '{username}' already exists."
        )

    user = User(
        username = username,
        password_hash = password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"User created successfully with ID {user.user_id}.")

    return user


def get_user_by_username(
        username: str,
        db: Session,
    ) -> User:
    """
    Retrieve a user by their ID.
    """

    logger.info(f"Retrieving user with username '{username}'.")

    statement = select(User).where(User.username == username)
    user = db.scalar(statement)

    return user


def get_all_users(db: Session) -> list[User]:
    """
    Return all users from the database.
    """

    logger.info("Retrieving all users.")

    statement = select(User)
    users = db.scalars(statement).all()

    logger.info(f"Retrieved {len(users)} user(s) from the database.")

    return users


def update_user(
        user_id: int,
        db: Session,
        updated_username: str | None = None,
        updated_password_hash: str | None = None,
    ) -> User:
    """
    Update a user's username and password hash.
    """

    logger.info(f"Updating user with ID {user_id}.")

    statement = select(User).where(User.user_id == user_id)
    user = db.scalar(statement)

    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        raise UserNotFoundError

    if updated_username is not None:
        logger.info(
            f"Updating username for user ID {user_id} "
            f"from '{user.username}' to '{updated_username}'."
        )
        user.username = updated_username

    if updated_password_hash is not None:
        logger.info(f"Updating password hash for user ID {user_id}.")
        user.password_hash = updated_password_hash

    db.commit()
    db.refresh(user)

    logger.info(f"Successfully updated user with ID {user.user_id}.")

    return user


def delete_user(
        user_id: int,
        db: Session,
    ) -> str:
    """
    Delete an existing user and return the username.
    """

    logger.info(f"Deleting user with ID {user_id}.")

    statement = select(User).where(User.user_id == user_id)
    user = db.scalar(statement)

    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        raise UserNotFoundError

    username = user.username

    db.delete(user)
    db.commit()

    logger.info(f"Deleted user '{username}' (ID {user_id}).")

    return username