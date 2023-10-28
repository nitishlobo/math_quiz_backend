"""User schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """User model with attributes common between request(s) and/or response(s)."""

    first_name: str
    last_name: str
    email: str
    is_superuser: bool


class CreateUserRequest(UserBase):
    """Request model for creating a user."""

    password: str


class UpdateUserRequest(CreateUserRequest):
    """Request model for updating an existing user."""


class UserResponse(UserBase):
    """Response model for user."""

    id_: UUID = Field(alias="id")
    created: datetime
    updated: datetime
    deleted: datetime

    class Config:
        """Config for User model."""

        orm_mode = True
