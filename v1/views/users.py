"""User endpoints."""

from collections.abc import Sequence
from datetime import datetime, timezone
from http import HTTPStatus

from v1.database.models.users import User
from v1.exceptions.users import UserAlreadyExistsError
from v1.schemas.base import DeleteResponse
from v1.schemas.users import CreateUserRequest, CreateUserService, UpdateUserRequest, UpdateUserService, UserResponse
from v1.services import users as users_service
from v1.views.base import APIRouter, DbSession, RouteTags
from v1.views.dependencies.users import UserDependency

router = APIRouter(prefix="/users", tags=[RouteTags.USERS])


@router.post("/", response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(db_session: DbSession, user: CreateUserRequest) -> User:
    """Return created user."""
    db_user = users_service.get_user_from_email(db_session, user.email)
    if db_user:
        raise UserAlreadyExistsError(email=user.email)
    return users_service.create_user(db_session, CreateUserService(**user.model_dump()))


@router.get("/", response_model=list[UserResponse])
def read_users(db_session: DbSession, offset: int = 0, limit: int = 100) -> Sequence[User]:
    """Return list of users in the database."""
    return users_service.get_users(db_session, offset, limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user: UserDependency) -> User:
    """Return user belonging to user id."""
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(db_session: DbSession, user: UserDependency, update_user_data: UpdateUserRequest) -> User | None:
    """Return updated user."""
    users_service.update_user(
        db_session,
        user_id=user.id_,
        update_user_data=UpdateUserService(**update_user_data.model_dump(exclude_unset=True)),
    )
    return users_service.get_user_from_id(db_session, user_id=user.id_)


@router.delete("/{user_id}", response_model=DeleteResponse)
def soft_delete_user(db_session: DbSession, user: UserDependency) -> DeleteResponse:
    """Return success message on delete."""
    users_service.update_user(
        db_session,
        user_id=user.id_,
        update_user_data=UpdateUserService(deleted_at=datetime.now(timezone.utc)),
    )
    return DeleteResponse()
