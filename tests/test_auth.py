import uuid

from conftest import client


def test_register():

    unique = uuid.uuid4().hex[:6]

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@example.com",
            "password": "password123",
            "role": "Customer"
        }
    )

    assert response.status_code == 200


def test_login():

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()