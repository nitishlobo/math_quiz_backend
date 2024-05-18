"""Test users service."""

import uuid
from collections.abc import Sequence
from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from v1.database.models.test_factories.users import UserFactory
from v1.database.models.users import User
from v1.schemas.users import CreateUserRequest, CreateUserService
from v1.services.users import create_user, get_user_from_email, get_user_from_id, get_users


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
    db_user = get_user_from_id(db_session, user.id_)

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
    db_user = get_user_from_id(db_session, random_id)

    # Then
    assert db_user is None


def test_get_user_from_email(db_session: Session):
    """Test service for getting a user from an email."""
    # Given
    user = UserFactory()
    db_session.commit()

    # When
    db_user = get_user_from_email(db_session, user.email)

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
    db_user = get_user_from_email(db_session, random_email)

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
    expected_users = db_session.scalars(select(User).order_by(User.first_name.asc(), User.last_name.asc())).all()
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
