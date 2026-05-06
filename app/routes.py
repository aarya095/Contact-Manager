from fastapi import APIRouter, HTTPException, Depends

from app.exceptions import ContactNotFoundError, UserAlreadyExistsError
from app.schemas import ContactEntry, UpdateContactEntry, Contact
from app.services import operations as op

from sqlalchemy.orm import Session

from app.database.database import get_db

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def root():
    return "Welcome to Contact Manager API"


@router.post("/contacts", 
             status_code = 201,
             summary = "Create a new contact")
def create_contact(
                    contact: ContactEntry,
                    db: Session = Depends(get_db)
                    ):
    logger.info("POST /contacts - request received")
    try:
        contact_data = op.create_contact(
                        contact_name = contact.contact_name, 
                        contact_number=contact.contact_number,
                        db = db
                        )
        logger.info(f"POST /contacts - success (status=201, name={contact.contact_name})")
        
        return {"Message": "Contact created successfully",
                "contact": {
                    "contact_id": contact_data.contact_id,
                    "contact_name": contact_data.contact_name
                    }
                }
    
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code = 400, 
            detail = "Contact name already exists!"
            )
    
@router.get("/contacts/{contact_id}",
            status_code = 200, 
            summary = "Gets the contact entry by name")
def get_contact(
                contact_id: int,
                db: Session = Depends(get_db)):
    logger.info("GET /contacts/{contact_id} - request received")
    try:
        contact_number = op.get_contact(
                                contact_id = contact_id,
                                db = db
                                )
        logger.info(f"GET /contacts/{contact_id} - success (status=201, id={contact_id})")
        return {"contact_number": contact_number}
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
            status_code = 200,
            summary = "Gets all the contact entries stored in the database")
def list_contacts(db: Session = Depends(get_db)) -> dict:
    
    logger.info("GET /contacts - request received")
    
    contacts_data = op.list_contacts(db)
    
    logger.info("GET /contacts - success (status=201)")

    return contacts_data
    

@router.put("/contacts", 
            status_code = 200,
            summary = "Updates an existing contact")
def update_contact(
                   contact: UpdateContactEntry,
                   db: Session = Depends(get_db)
                   ):
    logger.info("PUT /contacts - request received")
    try:
        updated_contact_data = op.update_contact(
            old_contact_name = contact.old_contact_name,
            updated_contact_name = contact.new_contact_name,
            updated_contact_number = contact.new_contact_number,
            db = db
        )
        logger.info(f"PUT /contacts - success (status=201, name={contact.new_contact_name})")
        
        return {"Message": "Contact updated successfully",
                "contact": {
                    "contact_id": updated_contact_data.contact_id,
                    "contact_name": updated_contact_data.contact_name
                    }
                }
    
    except ContactNotFoundError:
        raise HTTPException(
            status_code = 404, 
            detail = "Contact Not Found!"
            )
    
    
@router.delete("/contacts", 
               status_code = 200,
               summary = "Deletes an existing contact")
def delete_contact(
                    contact: Contact,
                    db: Session = Depends(get_db)
                    ):
    logger.info("DELETE /contacts - request received")
    try:
        deleted_contact_data = op.delete_contact(
                        contact_id = Contact.contact_id,
                        db = db
                        )
        logger.info(f"DELETE /contacts - success (status=201, name={contact.contact_name})")

        return {"Message": "Contact deleted successfully",
                "contact": {
                    "contact_id": deleted_contact_data["id"],
                    "contact_name": deleted_contact_data["contact_name"]
                    }
                }
    
    except ContactNotFoundError:
        raise HTTPException(
            status_code = 404, 
            detail = "Contact Not Found!"
            )