import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


TEST_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()