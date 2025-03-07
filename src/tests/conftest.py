import pytest
from fastapi.testclient import TestClient
from collections.abc import Generator
from ..core.settings import settings
from ..dependencies import get_session
from ..main import app
from ..core.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import *
from .db_utils import clear_user

def generate_test_db_name():
    import random
    import string
    return "test_" + "".join(random.choices(string.ascii_lowercase, k=10))

@pytest.fixture(scope="session")
def engine():
    """
    Creates a SQLAlchemy engine for testing.
    """

    # DB_NAME = generate_test_db_name()
    # print(DB_NAME)
    DB_NAME = "test_lmhtrgyier"
    TEST_DATABASE_URL = f"{settings.db_engine}://{settings.db_username}:{settings.db_password}@{settings.db_host}:5432/{DB_NAME}"
    engine = create_engine(TEST_DATABASE_URL)
    from sqlalchemy_utils import database_exists, create_database, drop_database

    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)
        # Base.metadata.create_all(engine)  # Create all tables

    # if database_exists(TEST_DATABASE_URL):
    #     Base.metadata.drop_all(engine)
    #     drop_database(TEST_DATABASE_URL)

    # create_database(TEST_DATABASE_URL)
    # Base.metadata.create_all(engine)   
    # Todo: init db data
    yield engine

    # Base.metadata.drop_all(engine)  # Drop all tables after tests
    # drop_database(TEST_DATABASE_URL)
    engine.dispose()

@pytest.fixture(scope="session")
def session_factory(engine):
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield factory

@pytest.fixture(scope="function")
def session(session_factory):
    """
    Creates a SQLAlchemy session for each test function.
    """
    with session_factory() as session:
        # init_db(session)
        yield session
        # session.rollback()  # Rollback after test
    # try:
    #     session = session_factory()
    #     yield session
    # finally:
    #     session.rollback()  # Rollback any changes
    #     session.close() 

@pytest.fixture(scope="function")
def client(session, clear_user):
    """
    Creates a FastAPI test client with access to the test session.
    """
    def override_get_db():
        yield session

    app.dependency_overrides[get_session] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides = {} 