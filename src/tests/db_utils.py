import pytest
from sqlalchemy import delete

from src.models.user import User


@pytest.fixture(scope="function")
def clear_user(session):
    yield
    delete_statement = delete(User)
    session.execute(delete_statement)
    session.commit()

def discard_id(data_dict):
    if "id" in data_dict:
        del data_dict["id"]
    return data_dict