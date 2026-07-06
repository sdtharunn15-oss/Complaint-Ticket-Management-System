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


def test_get_tickets():

    token = get_token()

    response = client.get(
        "/tickets/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200