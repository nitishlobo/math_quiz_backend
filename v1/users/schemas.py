"""User schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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

    model_config = ConfigDict(from_attributes=True)

    id_: UUID = Field(alias="id")
    created: datetime
    updated: datetime
    deleted: datetime
