"""User endpoints."""
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from v1.database.base import get_db
from v1.database.users import User
from v1.routers.base import APIRouter, RouteTags
from v1.schemas.users import CreateUserRequest, UpdateUserRequest, UserResponse
from v1.services import users as users_service

router = APIRouter(prefix="/users", tags=[RouteTags.USERS])


@router.post("/", response_model=UserResponse)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)) -> User:
    """Return created user."""
    db_user = users_service.get_user_from_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already registered")
    return users_service.create_user(db, user)


@router.get("/", response_model=list[UserResponse])
def read_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[User]:
    """Return list of users in the database."""
    return users_service.get_users(db, offset, limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: UUID, db: Session = Depends(get_db)) -> User | None:
    """Return user belonging to user id."""
    return users_service.get_user_from_id(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user: UpdateUserRequest, db: Session = Depends(get_db)) -> User | None:
    """Return updated user."""
    return users_service.update_user(db, user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)) -> None:
    """Return updated user."""
    # TODO: convey information whether deleting was successful
    users_service.delete_user(db, user_id)
