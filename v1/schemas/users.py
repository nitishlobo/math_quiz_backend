"""User schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# @todo add validator for all email fields


class CreateUserBase(BaseModel):
    """Common fields between create user service and request."""

    first_name: str
    last_name: str
    email: str
    is_superuser: bool
    password: str


class CreateUserRequest(CreateUserBase):
    """Request model for creating a user."""


class CreateUserService(CreateUserBase):
    """Service model for creating a user."""


class UpdateUserBase(BaseModel):
    """Common fields between update user service and request."""

    first_name: str | None
    last_name: str | None
    email: str | None
    is_superuser: bool | None = None
    password: str | None


class UpdateUserService(UpdateUserBase):
    """Service model for updating an existing user."""


class UpdateUserRequest(UpdateUserBase):
    """Request model for updating an existing user."""


class UserResponse(BaseModel):
    """Response model for user."""

    model_config = ConfigDict(populate_by_name=True)

    id_: UUID = Field(alias="id")
    first_name: str
    last_name: str
    email: str
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
