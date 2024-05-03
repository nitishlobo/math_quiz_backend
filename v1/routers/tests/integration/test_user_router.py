"""Test router for user."""

from main import v1_router

# client = TestClient(main_app)


def test_create_user(test_client):
    """Test create user."""
    # @fix invoke test database instead of real database
    response = test_client.post(
        f"{v1_router.prefix}/users",
        json={
            "first_name": "Joseph",
            "last_name": "Ya'aqov",
            "email": "joseph.yaaqov@gmail.com",
            "is_superuser": False,
            "password": "David@512BC!",
        },
    )
    from pprint import pprint

    pprint(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)
