
CREATE_BASE_REQUEST = {
    "email": "ab@def.xyz",
    "username": "family",
    "name": "Edric",
    "password": "IamNotRobot"
}
def test_create_user(client):
    response = client.post("/users/", json=CREATE_BASE_REQUEST)
    assert response.status_code == 200
    assert response.json() == {"message": "Pong"}