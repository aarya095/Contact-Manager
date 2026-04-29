import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

env_file_path = ".env.dev"
load_dotenv(dotenv_path = env_file_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
                            bind = engine,
                            autoflush = False,
                            autocommit = False
                            )

def get_db():
    """Dependency to get the database session"""
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

