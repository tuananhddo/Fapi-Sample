import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CREATE_BASE_REQUEST = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "password": "IamNotRobot"
}
USER_BASE = {
    "id": 1,
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "is_active": "IamNotRobot"
}
def test_create_user(client):
    response = client.post("/users/", json=CREATE_BASE_REQUEST)
    logger.info(response.content)
    assert response.status_code == 200
    assert response.json() == USER_BASE