from fastapi import APIRouter, HTTPException

from app.exceptions import ContactNotFoundError, UserAlreadyExistsError
from app.schemas import ContactEntry, UpdateContactEntry, DeleteContactEntry
from app.services import operations as op

router = APIRouter()

@router.get("/")
def root():
    return "Welcome to Contact Manager API"

@router.get("/contacts/{contact_name}",
            status_code=200, 
            summary = "Gets the contact entry by name")
def get_one_contact_entry(contact_name: str):
    try:
        contact_number = op.view_one_contact_entry(contact_name = contact_name)
        return {"contact_name": contact_name.title(), 
                "contact_number": contact_number}
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code = 400, 
            detail = "Contact already exists!"
            )
    except ContactNotFoundError:
        raise HTTPException(
            status_code = 404, 
            detail = "Contact Not Found!"
            )

@router.get("/contacts", 
            status_code=200,
            summary = "Gets all the contact entries stored in the database")
def get_all_contact_entries() -> dict:

    contacts_data = op.view_all_contacts()
    return contacts_data

@router.post("/contacts", 
             status_code=201,
             summary="Create a new contact")
def create_contact(contact: ContactEntry):
    try:
        contact_name = op.create_contact(
                        contact_name = contact.contact_name, 
                        contact_number=contact.contact_number
                        )
        return {"Message": 
                f"The entry for {contact_name} created successfully!"}
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code = 400, 
            detail = "Contact name already exists!"
            )
    
@router.put("/contacts", 
            status_code=200,
            summary="Updates an existing contact")
def update_contact(contact: UpdateContactEntry):
    try:
        updated_contact_name = op.update_contact_entry(
            old_contact_name = contact.old_contact_name,
            updated_contact_name = contact.new_contact_name,
            updated_contact_number = contact.new_contact_number
        )
        return {
            "Message": f"The contact entry for {updated_contact_name} has been updated successfully!"}
    
    except ContactNotFoundError:
        raise HTTPException(
            status_code = 404, 
            detail = "Contact Not Found!"
            )
    
@router.delete("/contacts", 
               status_code=200,
               summary="Deletes an existing contact")
def delete_contact(contact: DeleteContactEntry):
    try:
        contact_name = op.delete_contact(
                        contact_name = contact.contact_name
                        )
        return {"Message": 
                f"The entry for {contact_name} deleted successfully!"}
    except ContactNotFoundError:
        raise HTTPException(
            status_code = 404, 
            detail = "Contact Not Found!"
            )