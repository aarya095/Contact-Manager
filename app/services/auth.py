# User-Defined Modules
from config.config import config

# External Modules
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from pwdlib import PasswordHash


password_context = PasswordHash.recommended()
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password: str) -> str:
    return password_context.hash(plain_password)

