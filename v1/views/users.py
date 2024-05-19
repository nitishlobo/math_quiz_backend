"""User endpoints."""

from http import HTTPStatus
from uuid import UUID

from v1.database.models.users import User
from v1.exceptions.users import UserAlreadyExistsError
from v1.schemas.base import DeleteResponse
from v1.schemas.users import CreateUserRequest, CreateUserService, UpdateUserRequest, UpdateUserService, UserResponse
from v1.services import users as users_service
from v1.views.base import APIRouter, DbSession, RouteTags

router = APIRouter(prefix="/users", tags=[RouteTags.USERS])


@router.post("/", response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(db_session: DbSession, user: CreateUserRequest) -> User:
    """Return created user."""
    db_user = users_service.get_user_from_email(db_session, user.email)
    if db_user:
        raise UserAlreadyExistsError(email=user.email)
    return users_service.create_user(db_session, CreateUserService(**user.model_dump()))


@router.get("/", response_model=list[UserResponse])
def read_users(db_session: DbSession, offset: int = 0, limit: int = 100) -> list[User]:
    """Return list of users in the database."""
    return users_service.get_users(db_session, offset, limit)


# @todo add dependency for user to return an error if user does not exist
# @todo add integration test for deleting user who does not exist and check response
@router.get("/{user_id}", response_model=UserResponse)
def read_user(db_session: DbSession, user_id: UUID) -> User | None:
    """Return user belonging to user id."""
    return users_service.get_user_from_id(db_session, user_id)


# @todo add dependency for user to return an error if user does not exist
# @todo add integration test for deleting user who does not exist and check response
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(db_session: DbSession, user_id: UUID, user: UpdateUserRequest) -> User | None:
    """Return updated user."""
    return users_service.update_user(db_session, user_id, UpdateUserService(**user.model_dump(exclude_unset=True)))


# @todo add dependency for user to return an error if user does not exist
# @todo add integration test for deleting user who does not exist and check response
@router.delete("/{user_id}", response_model=DeleteResponse)
def soft_delete_user(db_session: DbSession, user_id: UUID) -> DeleteResponse:
    """Return success message on delete."""
    users_service.soft_delete_user(db_session, user_id)
    return DeleteResponse()
