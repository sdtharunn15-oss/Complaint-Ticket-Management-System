from conftest import client


def get_token():

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "admin123"
        }
    )

    return response.json()["access_token"]


def test_get_customers():

    token = get_token()

    response = client.get(
        "/customers/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200