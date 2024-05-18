"""Users service."""

from datetime import datetime, timezone
from uuid import UUID

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
    # @todo change query style to SQLAlchemy 2.0
    return db_session.query(User).filter(User.id_ == user_id).first()


def get_user_from_email(db_session: Session, email: str) -> User | None:
    """Return user by email."""
    return db_session.query(User).filter(User.email == email).first()


def get_users(db_session: Session, offset: int = 0, limit: int = 100) -> list[User]:
    """Return users based on the offset and limit restriction applied."""
    # @todo sort by first name so that the order is always the same
    return db_session.query(User).offset(offset).limit(limit).all()


def update_user(db_session: Session, user_id: UUID, user: UpdateUserService) -> User | None:
    """Return updated user."""
    user_data = user.model_dump(exclude={"password"}, exclude_unset=True)
    if user.password:
        user_data["hashed_password"] = common_services.hash_password(user.password)

    db_session.query(User).filter_by(id_=user_id).update(user_data)
    db_session.commit()
    return get_user_from_id(db_session, user_id)


def soft_delete_user(db_session: Session, user_id: UUID) -> None:
    """Delete user using user id."""
    db_session.query(User).filter_by(id_=user_id).update({"deleted": datetime.now(timezone.utc)})
