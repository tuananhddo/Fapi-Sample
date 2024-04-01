import pytest
from fastapi.testclient import TestClient
from collections.abc import Generator
from src.core.settings import settings
from src.dependencies import get_db
from src.main import app
from src.core.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import *
from src.models.base import Base

def generate_test_db_name():
    import random
    import string
    return "test_" + "".join(random.choices(string.ascii_lowercase, k=10))

@pytest.fixture(scope="session")
def engine():
    """
    Creates a SQLAlchemy engine for testing.
    """
    DB_NAME = generate_test_db_name()
    TEST_DATABASE_URL = f"{settings.db_engine}://{settings.db_username}:{settings.db_password}@{settings.db_host}:5432/"
    engine = create_engine(TEST_DATABASE_URL)

    # with engine.connect() as conn:
    #     conn.execute("CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    # engine.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    engine.execute(f"CREATE DATABASE {DB_NAME}")

    # engine.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    # Base.metadata.create_all(engine)  # Create all tables

    yield engine
    # Base.metadata.drop_all(engine)  # Drop all tables after tests
    # engine.execute(f"DROP DATABASE {DB_NAME}")
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
        print("XXXXXXXXXXXXXXX")
        yield session

# @pytest.fixture(scope="module")
# def client() -> Generator[TestClient, None, None]:
#     with TestClient(app) as c:
#         yield c

@pytest.fixture(scope="function")
def client(session):
    """
    Creates a FastAPI test client with access to the test session.
    """
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides = {} 