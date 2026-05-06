from pydantic import BaseModel

class Contact(BaseModel):
    contact_id: int

class ContactEntry(BaseModel):
    contact_name : str
    contact_number : int

class UpdateContactEntry(Contact):
    new_contact_name: str | None
    new_contact_number: int | None

class ContactResponse(Contact):
    contact_name : str