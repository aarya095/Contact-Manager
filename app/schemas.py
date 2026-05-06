from pydantic import BaseModel

class Contact(BaseModel):
    contact_id: int

class ContactEntry(BaseModel):
    contact_name : str
    contact_number : int

class UpdateContactEntry(BaseModel):
    old_contact_name : str
    new_contact_name : str | None
    new_contact_number : int | None

class DeleteContactEntry(BaseModel):
    contact_name : str

class ContactResponse(BaseModel):
    contact_id : int
    contact_name : str