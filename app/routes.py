from fastapi import APIRouter

from app.schemas import ContactEntry
from app.services import operations as op

router = APIRouter()

@router.get("/")
def root():
    return "Welcome to Contact Manager API"

@router.get("/contacts/{contact_name}", summary = "Gets the contact entry by name")
def get_one_contact_entry(contact_name: str):
    contact_number = op.view_one_contact_entry(contact_name = contact_name)

    if contact_number == "Null":
        return {"Error": f"The entry for {contact_name} doesn't exist!"}
    else:
        return {"contact_name": contact_name.title(), "contact_number": contact_number}

@router.get("/contacts", summary = "Gets all the contact entries stored in the database")
def get_all_contact_entries() -> dict:

    contacts_data = op.view_all_contacts()
    return contacts_data

@router.post("/contacts", summary="Create a new contact")
def create_contact(contact: ContactEntry):
    contact_name = op.create_contact(contact_name=contact.contact_name, 
                      contact_number=contact.contact_number)
    
    if contact_name == "Null":
        return {"Error": f"The entry for {contact.contact_name} already exist!"}
    else:
        return {"Message": f"The entry for {contact_name} created successfully!"}