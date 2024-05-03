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


class UpdateUserRequest(BaseModel):
    """Request model for updating an existing user."""

    first_name: str | None
    last_name: str | None
    email: str | None
    is_superuser: bool | None = None
    password: str | None


class UserResponse(UserBase):
    """Response model for user."""

    model_config = ConfigDict(populate_by_name=True)

    id_: UUID = Field(alias="id")
    created: datetime
    updated: datetime | None = None
    deleted: datetime | None = None


class UpdateUser(BaseModel):
    """Service model for updating an existing user."""

    first_name: str | None
    last_name: str | None
    email: str | None
    is_superuser: bool | None = None
    password: str | None
