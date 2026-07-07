# Built-in Modules
import logging

# User-Defined Modules
from config.config import config

# External Modules
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

engine = create_engine(config.DATABASE_URL)

SessionLocal = sessionmaker(
                            bind = engine,
                            autoflush = False,
                            autocommit = False
                            )

def empty_database_tables():
    """
    Drops all the tables in the DB
    """

    logger.info("Starting to empty the database.")

    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Drop all tables
    metadata.drop_all(bind=engine)

    logger.info("Database has been emptied successfully.")

def get_db():
    """
    Dependency to get the database session
    """
    
    db = SessionLocal()
    logger.debug("DB session created.")
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == '__main__':
    empty_database_tables()