# Built-in Modules
from datetime import datetime, timedelta, UTC

# User-Defined Modules
from config.config import config
from database.user_db_operations import get_user_by_username

# External Modules
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel
from jose import JWTError, jwt
from pwdlib import PasswordHash

from sqlalchemy.orm import Session


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

    user = get_user_by_username(db, username)
    if not user:
        return False
        
    if not verify_password(password, user['hashed_password']):
        return False
    
    return user