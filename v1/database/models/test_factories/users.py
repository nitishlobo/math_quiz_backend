"""Test related functionality for user database model."""

from datetime import datetime, timezone

import factory
import factory.fuzzy
from argon2 import PasswordHasher

from v1.database.models.test_factories.base import BaseFactory
from v1.database.models.users import User


class UserFactory(BaseFactory):
    """Test factory for user database model."""

    class Meta:
        """Factory boy metadata."""

        model = User
        exclude = ("password",)

    id_ = factory.Faker("uuid4")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}.{str(obj.id_).replace('-', '')}@gmail.com",
    )
    hashed_password = factory.LazyAttribute(lambda obj: PasswordHasher().hash(obj.password))
    is_superuser = False
    created_at = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime(2000, 1, 13, tzinfo=timezone.utc),
        end_dt=datetime.now(timezone.utc),
    )
    updated_at = None
    deleted_at = None

    # Fields not part of the model
    password = "MyNotSecurePassword123!"  # nosec: hardcoded_password_string
