from fastapi import APIRouter, HTTPException, Depends

from app.exceptions import ContactNotFoundError, UserAlreadyExistsError
from app.schemas import ContactEntry, UpdateContactEntry, DeleteContactEntry
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
    
@router.get("/contacts/{contact_name}",
            status_code = 200, 
            summary = "Gets the contact entry by name")
def get_one_contact_entry(
                        contact_name: str,
                        db: Session = Depends(get_db)):
    logger.info("GET /contacts/{contact_name} - request received")
    try:
        contact_number = op.view_one_contact_entry(
                                contact_name = contact_name,
                                db = db
                                )
        logger.info(f"GET /contacts/{contact_name} - success (status=201, name={contact_name})")
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
            status_code = 200,
            summary = "Gets all the contact entries stored in the database")
def get_all_contact_entries(db: Session = Depends(get_db)) -> dict:
    
    logger.info("GET /contacts - request received")
    
    contacts_data = op.view_all_contacts(db)
    
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
        updated_contact_data = op.update_contact_entry(
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
                    contact: DeleteContactEntry,
                    db: Session = Depends(get_db)
                    ):
    logger.info("DELETE /contacts - request received")
    try:
        deleted_contact_data = op.delete_contact(
                        contact_name = contact.contact_name,
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