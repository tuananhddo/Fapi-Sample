import logging

import pytest
from fastapi import status
from src.tests.db_utils import discard_id, get_random_email, to_param, to_test_params


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CREATE_BASE_REQUEST = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "password": "IamNot@1Robot",
}
USER_BASE = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "is_active": True,
}

CREATE_USER_TEST_SUITE = {
    "name": ["input", "expected_code", "expected_data"],
    "value": [
    (CREATE_BASE_REQUEST, status.HTTP_200_OK, USER_BASE, "Test Success"),
    ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None, "Create Without Email"),
    ({**CREATE_BASE_REQUEST, "username": None}, status.HTTP_400_BAD_REQUEST, None, "Create Without Username"),
    ({**CREATE_BASE_REQUEST, "name": None}, status.HTTP_400_BAD_REQUEST, None, "Create Without Name"),
    ({**CREATE_BASE_REQUEST, "password": None}, status.HTTP_400_BAD_REQUEST, None, "Create Without Password"),
    ({**CREATE_BASE_REQUEST, "email": "Nones@"}, status.HTTP_400_BAD_REQUEST, None, "Invalid Email Format"),
    ({**CREATE_BASE_REQUEST, "email": f"{get_random_email(256)}"}, status.HTTP_400_BAD_REQUEST, 
     'value is not a valid email address: The email address is too long before the @-sign (184 characters too many).', "Invalid Email Length"),

        # ({**CREATE_BASE_REQUEST, "email": None}, status.HTTP_400_BAD_REQUEST, None),
    ],
}


@pytest.mark.parametrize(
    *to_test_params(CREATE_USER_TEST_SUITE)
)
def test_create_user(client, input, expected_code, expected_data):
    logger.error(input)
    response = client.post("/users/", json=input)
    logger.info(response.content)
    assert response.status_code == expected_code
    
    if expected_code == status.HTTP_200_OK:
        assert discard_id(response.json()) == expected_data
    else:
        if expected_data:
            error = response.json()
            assert error['detail'][0]['msg'] == expected_data
        # assert
