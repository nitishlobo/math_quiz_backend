"""Exceptions relating to users."""

from uuid import UUID

from v1.exceptions.base import BaseError


class UserAlreadyExistsError(BaseError):
    """Raise error when user already exists in the database."""

    def __init__(self, email: str) -> None:
        """Email is unique for every user."""
        self.email = email


class UserIdDoesNotExistError(BaseError):
    """Raise error when user id does not exist in the database."""

    def __init__(self, id_: UUID) -> None:
        """User id."""
        self.id_ = id_
