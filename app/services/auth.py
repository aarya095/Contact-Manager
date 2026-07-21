# Built-in Modules
import logging
from datetime import (
    datetime, 
    timedelta, 
    UTC
    )

# User-Defined Modules
from config.config import config
from app.schemas import TokenData, UserResponse
from app.database.user_db_operations import get_user_by_username
from app.database.database import get_db

# External Modules
from fastapi import (
    HTTPException, 
    Depends, 
    status
    )
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from pwdlib import PasswordHash

from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

password_context = PasswordHash.recommended()
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return password_context.hash(plain_password)


def authenticate_user(
        username: str, 
        password: str,
        db: Session,
    ):
    """
    Authenticate a user using their username and password.

    Retrieves the user from the database and verifies the provided
    password against the stored password hash.
    """

    user = get_user_by_username(username, db)
    if not user:
        logger.info(f"Login failed: user '{username}' not found.")
        return False
        
    if not verify_password(password, user.password_hash):
        logger.info(f"Login failed: invalid password for '{username}'.")
        return False
    
    return user


def create_access_token(
        data: dict, 
        expires_delta: timedelta | None = None
        ) -> str:
    """
    Create a JWT access token.

    Encodes the provided payload into a JSON Web Token (JWT) and
    adds an expiration ("exp") claim. If no expiration duration is
    provided, the token expires after 15 minutes.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes = 15)

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(
        to_encode, 
        key = config.SECRET_KEY, 
        algorithm = config.ALGORITHM
        )

    return encoded_jwt


def get_current_user(
        db: Session  = Depends(get_db), 
        token: str = Depends(oauth_2_scheme)
        ):
    """
    Retrieve the currently authenticated user from a JWT access token.

    Decodes and validates the provided JWT, extracts the username from
    the token's "sub" claim, and fetches the corresponding user from
    the database.
    """

    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = "Could not validate credentials", 
        headers = {"WWW-Authenticate" : "Bearer"}
        )
    
    try:
        payload = jwt.decode(
            token = token, 
            key = config.SECRET_KEY, 
            algorithms = [config.ALGORITHM]
            )
        
        username : str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username = username)

    except JWTError:
        logger.warning("JWT validation failed due to an invalid or expired token.")
        raise credential_exception
    
    user = get_user_by_username(username = token_data.username, db = db)

    if user is None:
        logger.warning(
            f"Authentication failed: user '{token_data.username}' not found."
        )
        raise credential_exception
    
    return UserResponse(
        username = user.username,
        user_id = user.user_id
    )   