"""Exceptions relating to users."""

from v1.exceptions.base import BaseError


class UserAlreadyExistsError(BaseError):
    """Raise error when user already exists in the database."""

    def __init__(self, email: str) -> None:
        """Email is unique for every user."""
        self.email = email
