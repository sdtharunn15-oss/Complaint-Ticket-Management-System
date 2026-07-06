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


def test_agent_tickets():

    token = get_token()

    response = client.get(
        "/agents/2/tickets",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 404]