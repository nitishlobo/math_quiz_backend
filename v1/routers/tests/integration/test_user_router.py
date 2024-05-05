"""Test module for user router."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import v1_router
from v1.database.models.users import User
from v1.schemas.users import CreateUserRequest


def test_create_user(fastapi_test_client: TestClient, db_session: Session, create_user_request: CreateUserRequest):
    """Test create user."""
    datetime_before_request = datetime.now(timezone.utc)
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=create_user_request.model_dump())
    datetime_after_request = datetime.now(timezone.utc)

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
        "created",
        "deleted",
        "is_superuser",
        "updated",
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
    response_user_created = datetime.fromisoformat(response_data["created"])
    assert datetime_before_request < response_user_created
    assert response_user_created < datetime_after_request
    assert response_data["deleted"] is None
    assert response_data["is_superuser"] is False
    assert response_data["updated"] is None

    # Verify information recorded in database is correct
    db_user = db_session.query(User).filter_by(id_=response_data["id"]).first()
    # assert db_user is not None
    assert db_user.first_name == create_user_request.first_name
    assert db_user.last_name == create_user_request.last_name
    assert db_user.email == create_user_request.email
    assert db_user.created == response_user_created
    assert db_user.deleted is None
    assert db_user.is_superuser is False
    assert db_user.updated is None
