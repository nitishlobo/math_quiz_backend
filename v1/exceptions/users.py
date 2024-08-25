"""Exceptions relating to users."""

from datetime import datetime
from uuid import UUID

from v1.exceptions.base import BaseError


class UserAlreadyExistsError(BaseError):
    """Raise error when user already exists in the database."""

    def __init__(self, email: str) -> None:
        """Email is unique for every user."""
        self.email = email


class UserIdDoesNotExistError(BaseError):
    """Raise error when user id does not exist in the database."""

    def __init__(self, id: UUID) -> None:
        """User id."""
        self.id = id


class UserHasBeenPreviouslyDeletedError(BaseError):
    """Raise error when user had been previously deleted."""

    def __init__(self, email: str, deleted_at: datetime) -> None:
        """Email is unique for every user."""
        self.email = email
        self.deleted_at = deleted_at
