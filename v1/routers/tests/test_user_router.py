"""Test router for user."""
from fastapi.testclient import TestClient

from main import main_app, v1_router

client = TestClient(main_app)


def test_create_user():
    """Test create user."""
    # TODO: invoke test database instead of real database
    response = client.post(
        f"{v1_router.prefix}/users",
        json={
            "first_name": "Joseph",
            "last_name": "Ya'aqov",
            "email": "joseph.yaaqov@gmail.com",
            "is_superuser": False,
            "password": "David@512BC!",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
