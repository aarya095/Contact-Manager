from pydantic import BaseModel

class ContactEntry(BaseModel):
    contact_name : str
    contact_number : int

class UpdateContactEntry(BaseModel):
    old_contact_name : str
    new_contact_name : str | None
    new_contact_number : int | None

class DeleteContactEntry(BaseModel):
    contact_name : str