"""User endpoints."""

from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException

from v1.database.base import DbSession
from v1.database.models.users import User
from v1.routers.base import APIRouter, RouteTags
from v1.schemas.users import CreateUserRequest, UpdateUser, UpdateUserRequest, UserResponse
from v1.services import users as users_service

router = APIRouter(prefix="/users", tags=[RouteTags.USERS])


@router.post("/", response_model=UserResponse)
def create_user(db_session: DbSession, user: CreateUserRequest):
    """Return created user."""
    db_user = users_service.get_user_from_email(db_session, user.email)
    if db_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already registered")
    return users_service.create_user(db_session, user)


@router.get("/", response_model=list[UserResponse])
def read_users(db_session: DbSession, offset: int = 0, limit: int = 100) -> list[User]:
    """Return list of users in the database."""
    return users_service.get_users(db_session, offset, limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(db_session: DbSession, user_id: UUID) -> User | None:
    """Return user belonging to user id."""
    return users_service.get_user_from_id(db_session, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(db_session: DbSession, user_id: UUID, user: UpdateUserRequest) -> User | None:
    """Return updated user."""
    return users_service.update_user(db_session, user_id, UpdateUser(**user.model_dump()))


@router.delete("/{user_id}")
def delete_user(db_session: DbSession, user_id: UUID) -> None:
    """Return updated user."""
    # @fix convey information whether deleting was successful
    users_service.delete_user(db_session, user_id)
