"""Database related test fixtures."""

import pytest

from v1.schemas.users import CreateUserRequest


@pytest.fixture()
def create_user_request() -> CreateUserRequest:
    """Request data object for creating a user."""
    return CreateUserRequest(
        first_name="Joseph",
        last_name="Ya'aqov",
        email="joseph.yaaqov@gmail.com",
        is_superuser=False,
        password="David@512BC!",  # nosec: hardcoded_password_funcarg
    )
