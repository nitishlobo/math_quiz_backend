"""User schemas."""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from v1.services.datetime_ import validate_datetime_is_utc_timezone
from v1.services.emails import validate_and_normalize_email

Email = Annotated[str, AfterValidator(validate_and_normalize_email)]
UtcDatetime = Annotated[datetime, AfterValidator(validate_datetime_is_utc_timezone)]


class CreateUserBase(BaseModel):
    """Common fields between create user service and request."""

    first_name: str
    last_name: str
    email: Email
    is_superuser: bool
    password: str


class CreateUserRequest(CreateUserBase):
    """Request model for creating a user."""


class CreateUserService(CreateUserBase):
    """Service model for creating a user."""


class UpdateUserBase(BaseModel):
    """Common fields between update user service and request."""

    first_name: str | None = None
    last_name: str | None = None
    email: Email | None = None
    is_superuser: bool | None = None
    password: str | None = None


class UpdateUserService(UpdateUserBase):
    """Service model for updating an existing user."""

    deleted_at: UtcDatetime | None = None


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
