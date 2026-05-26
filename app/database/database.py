import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import config

logger = logging.getLogger(__name__)

engine = create_engine(config.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
                            bind = engine,
                            autoflush = False,
                            autocommit = False
                            )

def get_db():
    """Dependency to get the database session"""
    
    db = SessionLocal()
    logger.debug("DB session created.")
    try:
        yield db
    finally:
        db.close()