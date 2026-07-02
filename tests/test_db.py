from sqlalchemy import delete 

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.services.operations import create_contact
from app.database.models import Contact, Base

import logging

logger = logging.getLogger(__name__)

# Set up test db
env_file_path = ".env.test"
load_dotenv(dotenv_path = env_file_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
                            bind = engine,
                            autoflush = False,
                            autocommit = False
                            )