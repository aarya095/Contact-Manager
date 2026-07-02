from app.database.models import User

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