"""Test related functionality for user database model."""

from datetime import datetime, timezone

import factory
from argon2 import PasswordHasher

from v1.database.models.test_factories.base import BaseFactory
from v1.database.models.users import User


class UserFactory(BaseFactory):
    """Test factory for user database model."""

    id_ = factory.Faker("uuid4")
    first_name = "John"
    last_name = "Francesco"
    email = "john.francesco@gmail.com"
    hashed_password = PasswordHasher().hash("MyNotSecurePassword123!")
    is_superuser = False
    created_at = datetime(2024, 5, 29, 1, 6, 40, 336080, tzinfo=timezone.utc)
    updated_at = None
    deleted_at = None

    class Meta:
        """Factory boy metadata."""

        model = User
