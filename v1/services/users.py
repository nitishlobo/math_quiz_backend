"""Users service."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from v1.database.models.users import User
from v1.schemas.users import CreateUserRequest, UpdateUser
from v1.services import passwords as common_services


# @todo remove CreateUserRequest from this service file as this is a view model
def create_user(db: Session, user: CreateUserRequest) -> User:
    """Return created user."""
    hashed_password = common_services.hash_password(user.password)
    db_user = User(hashed_password=hashed_password, **user.model_dump(exclude={"password"}))
    db.add(db_user)
    # Flush to make User persistent in this session and get id and created_at.
    db.flush()
    # Refresh to get `updated_at` field in db_user model.
    db.refresh(db_user)
    return db_user


def get_user_from_id(db: Session, user_id: UUID) -> User | None:
    """Return user model object from user id."""
    return db.query(User).filter(User.id_ == user_id).first()


def get_user_from_email(db: Session, email: str) -> User | None:
    """Return user by email."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, offset: int = 0, limit: int = 100) -> list[User]:
    """Return users based on the offset and limit restriction applied."""
    return db.query(User).offset(offset).limit(limit).all()


# @todo remove UpdateUserRequest from this service file as this is a view model
def update_user(db: Session, user_id: UUID, user: UpdateUser) -> User | None:
    """Return updated user."""
    user_data = user.model_dump(exclude={"password"}, exclude_unset=True)
    if user.password:
        user_data["hashed_password"] = common_services.hash_password(user.password)

    db.query(User).filter_by(id_=user_id).update(user_data)
    db.commit()
    return get_user_from_id(db, user_id)


def delete_user(db: Session, user_id: UUID) -> None:
    """Delete user using user id."""
    db.query(User).filter_by(id_=user_id).update({"deleted": datetime.now(timezone.utc)})
