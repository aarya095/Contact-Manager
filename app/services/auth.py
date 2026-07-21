# Built-in Modules
import logging
from datetime import datetime, timedelta, UTC

# User-Defined Modules
from config.config import config
from app.schemas import TokenData
from database.user_db_operations import get_user_by_username

# External Modules
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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
