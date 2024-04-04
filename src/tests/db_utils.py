import pytest
from sqlalchemy import delete

from src.models.user import User

def extract_to_dict(suite_list, param_num):
    return [ {"data": test_data, "test_name": None} if len(test_data) == param_num else {"data": test_data[:-1], "test_name": test_data[-1]} for test_data in suite_list]
def to_param(suite_list, param_num):
    return [pytest.param(*(item["data"]), id=item["test_name"]) for item in extract_to_dict(suite_list, param_num)]

def to_test_params(config_dict: dict):
    is_exist = all(key in config_dict for key in ["name", "value"])
    if not is_exist:
        raise ValueError("Missing name or value if config_dict")
    return (",".join(config_dict['name']), to_param(config_dict['value'], len(config_dict['name'])))


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