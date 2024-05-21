"""Test users service."""

import uuid
from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from v1.database.models.test_factories.users import UserFactory
from v1.database.models.users import User
from v1.schemas.users import CreateUserRequest, CreateUserService, UpdateUserService
from v1.services.users import (
    create_user,
    get_user_from_email,
    get_user_from_id,
    get_users,
    soft_delete_user_using_id,
    update_user_using_id,
)


def test_create_user(db_session: Session, create_user_request: CreateUserRequest):
    """Test service for creating a user."""
    # Given
    user = CreateUserService(**create_user_request.model_dump())

    # When
    db_user = create_user(db_session, user)

    # Then
    # Verify the user fields
    assert db_user is not None
    assert db_user.id_ is not None
    assert db_user.first_name == user.first_name
    assert db_user.last_name == user.last_name
    assert db_user.email == user.email
    assert db_user.hashed_password is not None
    assert db_user.is_superuser is user.is_superuser

    # Verify the database has a record
    users = db_session.scalars(select(User).filter_by(email=db_user.email)).all()
    assert len(users) == 1
    assert users[0].to_dict() == db_user.to_dict()


def test_get_user_from_id(db_session: Session):
    """Test service for getting a user from an id."""
    # Given
    user = UserFactory()
    db_session.commit()

    # When
    db_user = get_user_from_id(db_session, user_id=user.id_)

    # Then
    assert db_user is not None
    assert db_user.to_dict() == user.to_dict()


def test_get_user_from_id_using_an_id_that_does_not_match_any_user(db_session: Session):
    """Test service for getting a user by using an id that does not match any user."""
    # Given
    UserFactory()
    db_session.commit()
    # A random uuid, which does not match any user
    random_id = uuid.uuid4()

    # When
    db_user = get_user_from_id(db_session, user_id=random_id)

    # Then
    assert db_user is None


def test_get_user_from_email(db_session: Session):
    """Test service for getting a user from an email."""
    # Given
    user = UserFactory()
    db_session.commit()

    # When
    db_user = get_user_from_email(db_session, email=user.email)

    # Then
    assert db_user is not None
    assert db_user.to_dict() == user.to_dict()


def test_get_user_from_email_using_an_email_that_does_not_match_any_user(db_session: Session):
    """Test service for getting a user from an email."""
    # Given
    UserFactory()
    db_session.commit()
    # A random email, which does not match any user
    random_email = f"jane.doe.{str(uuid.uuid4()).replace('-', '')}"

    # When
    db_user = get_user_from_email(db_session, email=random_email)

    # Then
    assert db_user is None


def get_users_as_list_of_dict(users: Sequence[User]) -> list[dict[str, Any]]:
    """Return users as a list of dictionary objects."""
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return users_list


@pytest.mark.slow()
def test_get_users(db_session: Session):
    """Test service for getting a users."""
    # Given
    # Create 200 users
    UserFactory.create_batch(200)
    db_session.commit()
    expected_users = db_session.scalars(
        select(User).order_by(User.first_name.asc(), User.last_name.asc(), User.id_.asc()),
    ).all()
    expected_user_list = get_users_as_list_of_dict(expected_users)

    # When
    # Default query - no offset, no limit
    page_1_of_2_db_users = get_users(db_session)
    page_2_of_2_db_users = get_users(db_session, offset=100)

    # Custom query - offset and limit provided
    page_1_of_4_db_users = get_users(db_session, offset=0, limit=50)
    page_2_of_4_db_users = get_users(db_session, offset=50, limit=50)
    page_3_of_4_db_users = get_users(db_session, offset=100, limit=50)
    page_4_of_4_db_users = get_users(db_session, offset=150, limit=50)

    # Then
    # Verify 200 users were created
    assert len(expected_users) == 200

    # Verify that by default only 100 results are given back
    assert len(page_1_of_2_db_users) == 100
    assert len(page_2_of_2_db_users) == 100
    # Verify that the boundary results are not repeated
    assert page_1_of_2_db_users[49].to_dict() != page_2_of_2_db_users[0].to_dict()
    # Verify that combining the paginated database users matches the full set of actual database records
    page_1_of_2_db_users_list = get_users_as_list_of_dict(page_1_of_2_db_users)
    page_2_of_2_db_users_list = get_users_as_list_of_dict(page_2_of_2_db_users)
    assert [*page_1_of_2_db_users_list, *page_2_of_2_db_users_list] == expected_user_list

    # Verify that each pagination produces the correct limit amount
    assert len(page_1_of_4_db_users) == 50
    assert len(page_2_of_4_db_users) == 50
    assert len(page_3_of_4_db_users) == 50
    assert len(page_4_of_4_db_users) == 50
    # Verify that the boundary results are not repeated
    assert page_1_of_4_db_users[49].to_dict() != page_2_of_4_db_users[0].to_dict()
    assert page_2_of_4_db_users[49].to_dict() != page_3_of_4_db_users[0].to_dict()
    assert page_3_of_4_db_users[49].to_dict() != page_4_of_4_db_users[0].to_dict()
    # Verify that combining the paginated database users matches the full set of actual database records
    page_1_of_4_db_users_list = get_users_as_list_of_dict(page_1_of_4_db_users)
    page_2_of_4_db_users_list = get_users_as_list_of_dict(page_2_of_4_db_users)
    page_3_of_4_db_users_list = get_users_as_list_of_dict(page_3_of_4_db_users)
    page_4_of_4_db_users_list = get_users_as_list_of_dict(page_4_of_4_db_users)
    assert [
        *page_1_of_4_db_users_list,
        *page_2_of_4_db_users_list,
        *page_3_of_4_db_users_list,
        *page_4_of_4_db_users_list,
    ] == expected_user_list

    # Verify that boundary results are the same between function calls with different params
    assert page_1_of_2_db_users[0].to_dict() == page_1_of_4_db_users[0].to_dict()
    assert page_1_of_2_db_users[49].to_dict() == page_1_of_4_db_users[49].to_dict()
    assert page_1_of_2_db_users[50].to_dict() == page_2_of_4_db_users[0].to_dict()
    assert page_1_of_2_db_users[99].to_dict() == page_2_of_4_db_users[49].to_dict()

    assert page_2_of_2_db_users[0].to_dict() == page_3_of_4_db_users[0].to_dict()
    assert page_2_of_2_db_users[49].to_dict() == page_3_of_4_db_users[49].to_dict()
    assert page_2_of_2_db_users[50].to_dict() == page_4_of_4_db_users[0].to_dict()
    assert page_2_of_2_db_users[99].to_dict() == page_4_of_4_db_users[49].to_dict()


def test_get_users_when_no_users_are_present(db_session: Session):
    """Test getting users when no users are present in the database."""
    # When
    users_1 = get_users(db_session)
    users_2 = get_users(db_session, offset=100)
    users_3 = get_users(db_session, offset=7, limit=3)

    # Then
    assert users_1 == []
    assert users_2 == []
    assert users_3 == []


def test_update_user(db_session: Session):  # pylint: disable=too-many-statements
    """Test update user."""
    # Given
    user_1 = UserFactory(first_name="Mary", last_name="Magdela", is_superuser=False)
    user_2 = UserFactory(first_name="Flora", last_name="Sarason", is_superuser=True)
    user_3 = UserFactory(first_name="Teresa", last_name="Alejandra", is_superuser=False)
    db_session.commit()
    # Get passwords before request, as PasswordHasher changes these objects (possible bug)
    user_1_hashed_password = user_1.hashed_password
    user_2_hashed_password = user_2.hashed_password
    user_3_hashed_password = user_3.hashed_password
    # Allow for slight variance between system clock and database clock (i.e. use timedelta)
    datetime_before_request = datetime.now(timezone.utc) - timedelta(minutes=1)

    # When
    user_1_update = UpdateUserService(last_name="Salvae", is_superuser=True)
    user_2_update = UpdateUserService(email="flora123solace@yahoo.com")
    user_3_update = UpdateUserService(password="MySuperCoolPassword@789!!")
    update_user_using_id(db_session, user_id=user_1.id_, update_user_data=user_1_update)
    update_user_using_id(db_session, user_id=user_2.id_, update_user_data=user_2_update)
    update_user_using_id(db_session, user_id=user_3.id_, update_user_data=user_3_update)
    datetime_after_request = datetime.now(timezone.utc) + timedelta(minutes=1)

    # Then
    # Verify fields on user 1 that should not be changed
    db_user_1 = db_session.get(User, user_1.id_)
    assert db_user_1 is not None
    assert db_user_1.id_ == user_1.id_
    assert db_user_1.first_name == user_1.first_name
    assert db_user_1.email == user_1.email
    assert db_user_1.hashed_password == user_1_hashed_password
    assert db_user_1.created_at == user_1.created_at
    assert db_user_1.deleted_at is None
    # Verify fields on user 1 that should be changed
    assert db_user_1.last_name == user_1_update.last_name
    assert db_user_1.is_superuser == user_1_update.is_superuser
    assert db_user_1.updated_at > datetime_before_request
    assert db_user_1.updated_at < datetime_after_request

    # Verify fields on user 2 that should not be changed
    db_user_2 = db_session.get(User, user_2.id_)
    assert db_user_2 is not None
    assert db_user_2.id_ == user_2.id_
    assert db_user_2.first_name == user_2.first_name
    assert db_user_2.last_name == user_2.last_name
    assert db_user_2.hashed_password == user_2_hashed_password
    assert db_user_2.is_superuser == user_2.is_superuser
    assert db_user_2.created_at == user_2.created_at
    assert db_user_2.deleted_at is None
    # Verify fields on user 2 that should be changed
    assert db_user_2.email == user_2_update.email
    assert db_user_2.updated_at > datetime_before_request
    assert db_user_2.updated_at < datetime_after_request

    # Verify fields on user 3 that should not be changed
    db_user_3 = db_session.get(User, user_3.id_)
    assert db_user_3 is not None
    assert db_user_3.id_ == user_3.id_
    assert db_user_3.first_name == user_3.first_name
    assert db_user_3.last_name == user_3.last_name
    assert db_user_3.email == user_3.email
    assert db_user_3.is_superuser == user_3.is_superuser
    assert db_user_3.created_at == user_3.created_at
    assert db_user_3.deleted_at is None
    # Verify fields on user 3 that should be changed
    assert db_user_3.hashed_password != user_3_hashed_password
    assert db_user_3.updated_at > datetime_before_request
    assert db_user_3.updated_at < datetime_after_request


def test_soft_delete_user(db_session: Session):
    """Test soft deleting a user."""
    # Given
    user = UserFactory(first_name="Mary", last_name="Magdela", is_superuser=False)
    db_session.commit()
    user_hashed_password = user.hashed_password
    # Allow for slight variance between system clock and database clock (i.e. use timedelta)
    datetime_before_request = datetime.now(timezone.utc) - timedelta(minutes=1)

    # When
    soft_delete_user_using_id(db_session, user.id_)
    datetime_after_request = datetime.now(timezone.utc) + timedelta(minutes=1)

    # Then
    db_user = db_session.get(User, user.id_)
    # Verify fields on user that should not be changed
    assert db_user is not None
    assert db_user.id_ == user.id_
    assert db_user.first_name == user.first_name
    assert db_user.last_name == user.last_name
    assert db_user.email == user.email
    assert db_user.hashed_password == user_hashed_password
    assert db_user.is_superuser == user.is_superuser
    assert db_user.created_at == user.created_at
    assert db_user.updated_at == user.updated_at
    # Verify fields on user that should be changed
    assert db_user.deleted_at is not None
    assert db_user.deleted_at > datetime_before_request
    assert db_user.deleted_at < datetime_after_request
