from pydantic import BaseModel

class ContactBase(BaseModel):
    contact_name : str
    contact_number : int

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    contact_id: int