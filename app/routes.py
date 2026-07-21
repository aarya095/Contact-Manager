# Built-in Modules
import logging
from datetime import timedelta

# User-Defined Modules
from config.config import config
from app.exceptions import (
    ContactNotFoundError, 
    UserAlreadyExistsError,
    )
from app.schemas import (
    UserCreate, UserResponse,
    ContactCreate, ContactUpdate,
    Token,
)
from app.services import operations as op
from app.services import auth 
from app.database import user_db_operations as user_db_ops
from app.database.database import get_db

# External Modules
from fastapi import (
    APIRouter, 
    HTTPException, 
    Request, 
    status,
    Depends
    )
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/frontend/templates"
)

@router.get("/")
def root(request : Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html"
    )


@router.post(
        "/register",
        status_code = 201,
        summary = "Register user"
        )
def register_user(
    user : UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    
    logger.info("POST /register - request received")

    try:
        password_hash = auth.get_password_hash(
            plain_password = user.password
        )
        user = user_db_ops.insert_user(
            db,
            username = user.username,
            password_hash = password_hash,
        )

        return UserResponse(
            user_id = user.user_id,
            username = user.username,
        )

    except UserAlreadyExistsError:
        raise HTTPException(
            status_code = 400, 
            detail = "Username already exists!"
            )
    

@router.post(
        "/token", 
        summary = "Authenticates users and returns the access token", 
        response_model = Token,
        )
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    ) -> dict:

    user = auth.authenticate_user(
        username = form_data.username, 
        password = form_data.password, 
        db = db
        )

    if not user:
        raise HTTPException(        
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = "Incorrect Username or Password", 
        headers = {"WWW-Authenticate" : "Bearer"}
        )
    
    access_toekn_expires = timedelta(minutes = config.ACCESS_TOKEN_EXPIRE_TIME)

    access_token = auth.create_access_token(
        data = {"sub" : user['username']},
        expires_delta = access_toekn_expires
    )

    return {"access_token" : access_token, "token_type" : "bearer"}
    

@router.post(
        "/contacts", 
        status_code = 201,
        summary = "Create a new contact"
        )
def create_contact(
                    contact: ContactCreate,
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
                    "contact_name": contact_data.contact_name,
                    "contact_number": contact_data.contact_number
                    }
                }
    
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code = 400, 
            detail = "Contact name already exists!"
            )
    
@router.get(
        "/contacts/{contact_id}",
        status_code = 200, 
        summary = "Gets the contact entry by id"
        )
def get_contact(
                contact_id: int,
                db: Session = Depends(get_db)):
    logger.info(f"GET /contacts/{contact_id} - request received")
    try:
        contact_data = op.get_contact(
                                contact_id = contact_id,
                                db = db
                                )
        
        logger.info(f"GET /contacts/{contact_id} - success (status=201, id={contact_id})")
        return contact_data
    
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


@router.get(
        "/contacts", 
        status_code = 200,
        summary = "Gets all the contact entries stored in the database"
        )
def list_contacts(db: Session = Depends(get_db)) -> list[dict[str, str | int]]:
    
    logger.info("GET /contacts - request received")
    
    contacts_data = op.list_contacts(db)
    
    logger.info("GET /contacts - success (status=201)")

    return contacts_data
    

@router.put(
        "/contacts/{contact_id}", 
        status_code = 200,
        summary = "Updates an existing contact"
        )
def update_contact(
                   contact_id: int,
                   contact: ContactUpdate,
                   db: Session = Depends(get_db)
                   ):
    logger.info("PUT /contacts - request received")
    try:
        updated_contact_data = op.update_contact(
            contact_id = contact_id,
            updated_contact_name = contact.contact_name,
            updated_contact_number = contact.contact_number,
            db = db
        )
        logger.info(f"PUT /contacts - success (status=201, name={contact.contact_name})")
        
        return {"Message": "Contact updated successfully",
                "contact": {
                    "contact_id": updated_contact_data.contact_id,
                    "contact_name": updated_contact_data.contact_name,
                    "contact_number": updated_contact_data.contact_number
                    }
                }
    
    except ContactNotFoundError:
        raise HTTPException(
            status_code = 404, 
            detail = "Contact Not Found!"
            )
    
    
@router.delete(
        "/contacts/{contact_id}", 
        status_code = 200,
        summary = "Deletes an existing contact"
        )
def delete_contact(
                    contact_id: int,
                    db: Session = Depends(get_db)
                    ):
    logger.info("DELETE /contacts - request received")
    try:
        deleted_contact_data = op.delete_contact(
                        contact_id = contact_id,
                        db = db
                        )
        logger.info(f"DELETE /contacts - success (status=201, name={deleted_contact_data["contact_name"]})")

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