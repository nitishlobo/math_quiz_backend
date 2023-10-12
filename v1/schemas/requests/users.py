"""User request schemas."""
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    """Requests base user model."""

    id_: UUID
    first_name: str
    last_name: str
    email: str

    class Config:
        """Config for User model."""

        orm_mode = True
