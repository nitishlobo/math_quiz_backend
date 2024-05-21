"""Users service."""

from collections.abc import Sequence
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from v1.database.models.users import User
from v1.schemas.users import CreateUserService, UpdateUserService
from v1.services import passwords as common_services


def create_user(db_session: Session, user: CreateUserService) -> User:
    """Return created user."""
    hashed_password = common_services.hash_password(user.password)
    db_user = User(hashed_password=hashed_password, **user.model_dump(exclude={"password"}))
    db_session.add(db_user)
    db_session.commit()
    return db_user


def get_user_from_id(db_session: Session, user_id: UUID) -> User | None:
    """Return user model object from user id."""
    return db_session.get(User, user_id)


def get_user_from_email(db_session: Session, email: str) -> User | None:
    """Return user by email."""
    return db_session.execute(select(User).filter_by(email=email)).scalar_one_or_none()


def get_users(db_session: Session, offset: int = 0, limit: int = 100) -> Sequence[User]:
    """Return users sorted by first, then last name, then id and also based on the offset and limit restriction."""
    return db_session.scalars(
        select(User).order_by(User.first_name.asc(), User.last_name.asc(), User.id_.asc()).offset(offset).limit(limit),
    ).all()


def update_user(db_session: Session, user_id: UUID, update_user_data: UpdateUserService) -> None:
    """Update user."""
    update_user_dict = update_user_data.model_dump(exclude={"password"}, exclude_unset=True)
    if update_user_data.password:
        update_user_dict["hashed_password"] = common_services.hash_password(update_user_data.password)

    db_session.execute(update(User).where(User.id_ == user_id).values(**update_user_dict))
    db_session.commit()


def soft_delete_user(db_session: Session, user_id: UUID) -> None:
    """Soft delete a user using user id."""
    update_user(db_session, user_id, update_user_data=UpdateUserService(deleted_at=datetime.now(timezone.utc)))
