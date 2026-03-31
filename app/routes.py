from fastapi import APIRouter, HTTPException

from app.exceptions import ContactNotFoundError
from app.schemas import ContactEntry
from app.services import operations as op

router = APIRouter()

@router.get("/")
def root():
    return "Welcome to Contact Manager API"

@router.get("/contacts/{contact_name}", summary = "Gets the contact entry by name")
def get_one_contact_entry(contact_name: str):
    try:
        contact_number = op.view_one_contact_entry(contact_name = contact_name)
        return {"contact_name": contact_name.title(), "contact_number": contact_number}
    except ContactNotFoundError:
        raise HTTPException(status_code = 404, detail = "Contact Not Found!")

@router.get("/contacts", summary = "Gets all the contact entries stored in the database")
def get_all_contact_entries() -> dict:

    contacts_data = op.view_all_contacts()
    return contacts_data

@router.post("/contacts", summary="Create a new contact")
def create_contact(contact: ContactEntry):
    try:
        contact_name = op.create_contact(contact_name=contact.contact_name, 
                        contact_number=contact.contact_number)
        return {"Message": f"The entry for {contact_name} created successfully!"}
    except ContactNotFoundError:
        raise HTTPException(status_code = 404, detail = "Contact name already exists!")