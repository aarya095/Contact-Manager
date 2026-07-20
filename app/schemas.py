# External Modules
from pydantic import BaseModel

class UserBase(BaseModel):
    username : str

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    user_id : int

class ContactBase(BaseModel):
    owner_id : int
    contact_name : str
    contact_number : int

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    contact_id: int

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str | None = None

class User(BaseModel):
    username : str 

class UserInDB(User):
    hashed_password : str