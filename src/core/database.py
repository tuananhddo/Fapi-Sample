from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from src.core.settings import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def reset_database():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    print(inspector.get_table_names())  # See if the table exists multiple times
    SQLModel.metadata.drop_all(engine)  # ❌ Drop all tables (deletes all data)
    SQLModel.metadata.create_all(engine)  # ✅ Recreate tables



def get_session():
    with Session(engine) as session:
        yield session

