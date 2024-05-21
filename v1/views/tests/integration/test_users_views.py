"""Test module for user router."""

import uuid
from datetime import datetime, timedelta, timezone
from operator import itemgetter
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
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
    # Given
    # Allow for slight variance between system clock and database clock (i.e. use timedelta)
    datetime_before_request = datetime.now(timezone.utc) - timedelta(minutes=1)

    # When
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=create_user_request.model_dump())
    datetime_after_request = datetime.now(timezone.utc) + timedelta(minutes=1)

    # Then
    # Verify response status and type
    response_data = response.json()
    assert response.status_code == 201
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
    # When
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=create_user_request.model_dump())

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 201
    assert isinstance(response_data, dict)


@pytest.mark.integration()
def test_create_user_with_an_invalid_email_address_fails(
    fastapi_test_client: TestClient,
    create_user_request: CreateUserRequest,
):
    """Test creating an user with an invalid email address fails."""
    # Given
    user_request = create_user_request
    user_request.email = "florence..faolluiere@gmail.com"

    # When
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=user_request.model_dump())

    # Then
    # Verify response status and type
    response_data = response.json()
    assert response.status_code == 422
    assert isinstance(response_data, dict)


@pytest.mark.integration()
def test_creating_a_user_who_already_exists_fails(
    fastapi_test_client: TestClient,
    db_session: Session,
    create_user_request: CreateUserRequest,
):
    """Test that given a user already exists, they cannot be created again."""
    # Given
    user = create_user_request.model_dump()
    # Create the user in the database
    UserFactory(**user)
    db_session.commit()

    # When
    # Try to create the user again
    response = fastapi_test_client.post(f"{v1_router.prefix}/users", json=user)

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 400
    assert response_data == {
        "message": f"User {user['email']} already exists. Cannot create a user who already exists.",
    }


@pytest.mark.integration()
def test_read_users(fastapi_test_client: TestClient, db_session: Session):
    """Test getting a list of users."""
    # Given
    # Create users in the database
    datetime_now = datetime.now(timezone.utc)
    user_1 = UserFactory()
    user_2 = UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    user_3 = UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()

    # When
    response = fastapi_test_client.get(f"{v1_router.prefix}/users")

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 200
    expected_response = [
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
    # Sort response data and expected response by id to compare
    sorted_response_data = sorted(response_data, key=itemgetter("id"))
    sorted_expected_response = sorted(expected_response, key=itemgetter("id"))
    assert sorted_response_data == sorted_expected_response


@pytest.mark.integration()
def test_read_user(fastapi_test_client: TestClient, db_session: Session):
    """Test getting a single user."""
    # Given
    # Create users in the database
    datetime_now = datetime.now(timezone.utc)
    _user_1 = UserFactory()
    user_2 = UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    _user_3 = UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()

    # When
    response = fastapi_test_client.get(f"{v1_router.prefix}/users/{user_2.id_}")

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 200
    expected_response = {
        "created_at": datetime_obj_to_str(user_2.created_at),
        "deleted_at": user_2.deleted_at,
        "email": user_2.email,
        "first_name": "Fulton",
        "id": str(user_2.id_),
        "is_superuser": True,
        "last_name": "Sheen",
        "updated_at": datetime_obj_to_str(user_2.updated_at),
    }
    assert response_data == expected_response


@pytest.mark.integration()
def test_read_user_with_a_user_id_which_does_not_match_any_users_fails(
    fastapi_test_client: TestClient,
    db_session: Session,
):
    """Test getting a user with an id that does not match any users fails."""
    # Given
    # Create 3 users in the database
    datetime_now = datetime.now(timezone.utc)
    UserFactory()
    UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()

    # When
    # Create a random id that does not match any users
    random_user_id = str(uuid.uuid4())
    response = fastapi_test_client.get(f"{v1_router.prefix}/users/{random_user_id}")

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 400
    assert response_data == {"message": f"User id {random_user_id} does not exist."}


@pytest.mark.integration()
def test_update_user(fastapi_test_client: TestClient, db_session: Session):
    """Test updating a user's information."""
    # Given
    # Create users in the database
    datetime_now = datetime.now(timezone.utc)
    user_1 = UserFactory()
    user_2 = UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    user_3 = UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()
    # Get passwords before request, as PasswordHasher changes these objects (possible bug)
    user_3_hashed_password = user_3.hashed_password

    # When
    response = fastapi_test_client.patch(
        f"{v1_router.prefix}/users/{user_3.id_}",
        json={"first_name": "Jonathan", "is_superuser": True, "password": "MyStronglyFakePassword@!"},
    )

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 200
    expected_response = {
        "created_at": datetime_obj_to_str(user_3.created_at),
        "deleted_at": user_3.deleted_at,
        "email": user_3.email,
        "first_name": "Jonathan",
        "id": str(user_3.id_),
        "is_superuser": True,
        "last_name": "Tolkien",
        # updated_at should reflect a new time after being updated.
        # Therefore, updated_at should be failing but is actually passing!
        # This could be because of a SQLAlchemy/Factory boy bug.
        "updated_at": datetime_obj_to_str(user_3.updated_at),
    }
    assert response_data == expected_response

    # Map database users for verifying data
    db_users = db_session.scalars(select(User)).all()
    db_user_id_to_user_map = {user.id_: user.to_dict() for user in db_users}
    # Verify password is changed
    assert db_user_id_to_user_map[user_3.id_]["hashed_password"] != user_3_hashed_password

    # Verify that user_1 and user_2 data remains the same as before the request
    assert db_user_id_to_user_map[user_1.id_] == user_1.to_dict()
    assert db_user_id_to_user_map[user_2.id_] == user_2.to_dict()


@pytest.mark.integration()
def test_update_user_with_a_user_id_which_does_not_match_any_users_fails(
    fastapi_test_client: TestClient,
    db_session: Session,
):
    """Test updating a user with an id that does not match any users fails."""
    # Given
    # Create 3 users in the database
    datetime_now = datetime.now(timezone.utc)
    UserFactory()
    UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()

    # When
    # Create a random id that does not match any users
    random_user_id = str(uuid.uuid4())
    response = fastapi_test_client.patch(
        f"{v1_router.prefix}/users/{random_user_id}",
        json={"first_name": "Jonathan", "is_superuser": True, "password": "MyStronglyFakePassword@!"},
    )

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 400
    assert response_data == {"message": f"User id {random_user_id} does not exist."}


@pytest.mark.integration()
def test_update_user_with_an_invalid_email_address_fails(fastapi_test_client: TestClient, db_session: Session):
    """Test updating a user using an invalide email address fails."""
    # Given
    user = UserFactory(first_name="Fulton", last_name="Sheen", email="fulton.sheen@gmail.com")
    db_session.commit()

    # When
    response = fastapi_test_client.patch(
        f"{v1_router.prefix}/users/{user.id_}",
        json={"email": "fulton.sheen@elpaso-university.com"},
    )

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 422
    assert isinstance(response_data, dict)


@pytest.mark.integration()
def test_delete_user(fastapi_test_client: TestClient, db_session: Session):
    """Test soft deleting a user."""
    # Given
    # Create users in the database
    user_1 = UserFactory()
    user_2 = UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    user_3 = UserFactory(first_name="John", last_name="Tolkien")
    db_session.commit()
    datetime_before_request = datetime.now(timezone.utc) - timedelta(minutes=1)

    # When
    response = fastapi_test_client.delete(f"{v1_router.prefix}/users/{user_1.id_}")
    datetime_after_request = datetime.now(timezone.utc) + timedelta(minutes=1)

    # Then
    response_data = response.json()
    assert response.status_code == 200
    expected_response = {"message": "success"}
    assert response_data == expected_response

    # Verify that it was only a soft delete - i.e. all 3 users still exist
    db_users = db_session.scalars(select(User)).all()
    assert len(db_users) == 3

    # Verify that user 1 was deleted
    db_user_id_to_user_map = {user.id_: user.to_dict() for user in db_users}
    user_1_deleted_at = db_user_id_to_user_map[user_1.id_]["deleted_at"]
    assert user_1_deleted_at is not None
    assert user_1_deleted_at > datetime_before_request
    assert user_1_deleted_at < datetime_after_request

    # Verify that the user 2 and 3 are not deleted
    assert db_user_id_to_user_map[user_2.id_]["deleted_at"] is None
    assert db_user_id_to_user_map[user_3.id_]["deleted_at"] is None


@pytest.mark.integration()
def test_delete_user_who_has_been_previously_deleted_fails(
    fastapi_test_client: TestClient,
    db_session: Session,
):
    """Test deleting a user who has been previously deleted fails."""
    # Given
    # Create 3 users in the database
    datetime_now = datetime.now(timezone.utc)
    user_1_deleted_at = datetime(1997, 2, 16, 3, 4, 59, 63870, tzinfo=timezone.utc)
    user_1 = UserFactory(deleted_at=user_1_deleted_at)
    UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()

    # When
    response = fastapi_test_client.delete(f"{v1_router.prefix}/users/{user_1.id_}")

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 400
    assert response_data == {
        "message": f"User {user_1.email} has been previously deleted at {user_1.deleted_at.isoformat()}.",
    }


@pytest.mark.integration()
def test_delete_user_with_a_user_id_which_does_not_match_any_users_fails(
    fastapi_test_client: TestClient,
    db_session: Session,
):
    """Test deleting a user with an id that does not match any users fails."""
    # Given
    # Create 3 users in the database
    datetime_now = datetime.now(timezone.utc)
    UserFactory()
    UserFactory(first_name="Fulton", last_name="Sheen", is_superuser=True)
    UserFactory(first_name="John", last_name="Tolkien", created_at=datetime_now)
    db_session.commit()

    # When
    # Create a random id that does not match any users
    random_user_id = str(uuid.uuid4())
    response = fastapi_test_client.delete(f"{v1_router.prefix}/users/{random_user_id}")

    # Then
    # Verify response status and data
    response_data = response.json()
    assert response.status_code == 400
    assert response_data == {"message": f"User id {random_user_id} does not exist."}
