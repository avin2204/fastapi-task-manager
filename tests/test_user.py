from .conftest import client

import uuid


def test_register():

    unique_id = str(uuid.uuid4())

    response = client.post(
        "/register",
        json={
            "username": f"user_{unique_id}",
            "email": f"{unique_id}@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == "User created successfully"


def test_login():

    unique_id = str(uuid.uuid4())

    username = f"user_{unique_id}"

    email = f"{unique_id}@test.com"

    client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": "123456"
        }
    )

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    assert response.status_code == 200

    assert "access_token" in response.json()

    assert response.json()["token_type"] == "bearer"