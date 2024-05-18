"""Test module for user router."""

from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import v1_router  # pylint: disable=no-name-in-module
from v1.database.models.test_factories.users import UserFactory
from v1.database.models.users import User
from v1.schemas.users import CreateUserRequest


def datetime_obj_to_str(datetime_obj: datetime):
    """Convert datetime with timezone object to string."""
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f %Z").replace(" UTC", "Z")


@pytest.mark.integration()
def test_create_user(fastapi_test_client: TestClient, db_session: Session, create_user_request: CreateUserRequest):
    """Test create user route and response."""
    # Allow for slight variance between system clock and database clock (i.e. use timedelta)
    datetime_before_request = datetime.now(timezone.utc) - timedelta(minutes=1)
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=create_user_request.model_dump())
    datetime_after_request = datetime.now(timezone.utc) + timedelta(minutes=1)

    # Verify response status and type
    response_data = response.json()
    assert response.status_code == 200
    assert isinstance(response_data, dict)

    # Verify fields in response
    expected_fields = {
        "id",
        "first_name",
        "last_name",
        "email",
        "is_superuser",
        "created_at",
        "updated_at",
        "deleted_at",
    }
    response_fields = set(response_data.keys())
    assert response_fields == expected_fields

    # Explicitly verify password related data is not in response (even though it is covered above)
    assert "password" not in response_fields
    assert "hashed_password" not in response_fields

    # Verify data in response
    assert UUID(response_data["id"]).version == 4
    assert response_data["first_name"] == create_user_request.first_name
    assert response_data["last_name"] == create_user_request.last_name
    assert response_data["email"] == create_user_request.email
    assert response_data["is_superuser"] is False
    response_user_created = datetime.fromisoformat(response_data["created_at"])
    assert datetime_before_request < response_user_created
    assert response_user_created < datetime_after_request
    assert response_data["updated_at"] == response_data["created_at"]
    assert response_data["deleted_at"] is None

    # Verify information recorded in database is correct
    db_user = db_session.query(User).filter_by(id_=response_data["id"]).first()
    assert db_user is not None
    assert db_user.first_name == create_user_request.first_name
    assert db_user.last_name == create_user_request.last_name
    assert db_user.email == create_user_request.email
    assert db_user.is_superuser is False
    assert db_user.created_at == response_user_created
    assert db_user.updated_at == response_user_created
    assert db_user.deleted_at is None


@pytest.mark.integration()
def test_create_same_user_as_above_test_is_possible(
    fastapi_test_client: TestClient,
    create_user_request: CreateUserRequest,
):
    """Test creating the same user as the above test succeeds.

    This test is to ensure that every subsequent test is not affected by the changes
    made in the database from the previous test. Each test should rollback any commits that were made.
    """
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=create_user_request.model_dump())

    # Verify response status and type
    response_data = response.json()
    assert response.status_code == 200
    assert isinstance(response_data, dict)


@pytest.mark.integration()
def test_creating_a_user_who_already_exists_fails(
    fastapi_test_client: TestClient,
    db_session: Session,
    create_user_request: CreateUserRequest,
):
    """Test that given a user already exists, they cannot be created again."""
    user = create_user_request.model_dump()

    # Create the user in the database
    UserFactory(**user)
    db_session.commit()

    # Try to create the user again
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=user)

    # Verify response status and type
    response_data = response.json()
    assert response.status_code == 400
    assert response_data == {
        "message": f"User {user['email']} already exists. Cannot create a user who already exists.",
    }


@pytest.mark.integration()
def test_read_users(fastapi_test_client: TestClient, db_session: Session):
    """Test that given a user already exists, they cannot be created again."""
    # Create users in the database
    datetime_now = datetime.now(timezone.utc)
    user_1 = UserFactory()
    user_2 = UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    user_3 = UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()

    response = fastapi_test_client.get(f"{v1_router.prefix}/users")

    # Verify response status and type
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == [
        {
            "created_at": datetime_obj_to_str(user_1.created_at),
            "deleted_at": user_1.deleted_at,
            "email": user_1.email,
            "first_name": user_1.first_name,
            "id": str(user_1.id_),
            "is_superuser": user_1.is_superuser,
            "last_name": user_1.last_name,
            "updated_at": datetime_obj_to_str(user_1.updated_at),
        },
        {
            "created_at": datetime_obj_to_str(user_2.created_at),
            "deleted_at": user_2.deleted_at,
            "email": user_2.email,
            "first_name": "Fulton",
            "id": str(user_2.id_),
            "is_superuser": True,
            "last_name": "Sheen",
            "updated_at": datetime_obj_to_str(user_2.updated_at),
        },
        {
            "created_at": datetime_obj_to_str(datetime_now),
            "deleted_at": user_3.deleted_at,
            "email": user_3.email,
            "first_name": "John",
            "id": str(user_3.id_),
            "is_superuser": user_3.is_superuser,
            "last_name": "Tolkien",
            "updated_at": datetime_obj_to_str(user_3.updated_at),
        },
    ]
