import logging

import pytest
from fastapi import status
from src.tests.db_utils import discard_id, to_param, to_test_params


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CREATE_BASE_REQUEST = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "password": "IamNotRobot",
}
USER_BASE = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "is_active": True,
}
CREATE_USER_TEST_SUITE = [
    (CREATE_BASE_REQUEST, status.HTTP_200_OK, USER_BASE, "Test1"),
    ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None, "Test2"),
    ({**CREATE_BASE_REQUEST, "username": None}, status.HTTP_400_BAD_REQUEST, None, "Test3"),
    ({**CREATE_BASE_REQUEST, "name": None}, status.HTTP_400_BAD_REQUEST, None, "Test4"),
    ({**CREATE_BASE_REQUEST, "password": None}, status.HTTP_400_BAD_REQUEST, None, "Test5"),
    # ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None),
    # ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None),
]

CREATE_USER_TEST_SUITE = {
    "name": ["input", "expected_code", "expected_data"],
    "value": [
    (CREATE_BASE_REQUEST, status.HTTP_200_OK, USER_BASE, "Test1"),
    ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None, "Test2"),
    ({**CREATE_BASE_REQUEST, "username": None}, status.HTTP_400_BAD_REQUEST, None, "Test3"),
    ({**CREATE_BASE_REQUEST, "name": None}, status.HTTP_400_BAD_REQUEST, None, "Test4"),
    ({**CREATE_BASE_REQUEST, "password": None}, status.HTTP_400_BAD_REQUEST, None, "Test5"),
        # ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None),
        # ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None),
    ],
}


@pytest.mark.parametrize(
    *to_test_params(CREATE_USER_TEST_SUITE)
)
def test_create_user(client, input, expected_code, expected_data):
    response = client.post("/users/", json=input)
    logger.info(response.content)
    assert response.status_code == expected_code
    if expected_data:
        assert discard_id(response.json()) == expected_data
