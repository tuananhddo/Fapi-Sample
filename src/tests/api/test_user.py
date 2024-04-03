import logging

import pytest
from fastapi import status
from src.tests.db_utils import discard_id


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CREATE_BASE_REQUEST = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "password": "IamNotRobot"
}
USER_BASE = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "is_active": True

}

@pytest.mark.parametrize("input, expected_code, expected_data", [
    (CREATE_BASE_REQUEST, status.HTTP_200_OK, USER_BASE),
    ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_422_UNPROCESSABLE_ENTITY, USER_BASE)
])
def test_create_user(client, input, expected_code, expected_data):
    response = client.post("/users/", json=input)
    logger.info(response.content)
    assert response.status_code == expected_code
    assert discard_id(response.json()) == expected_data
