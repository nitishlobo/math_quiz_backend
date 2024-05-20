"""Dependencies for users router."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends

from v1.database.models.users import User
from v1.exceptions.users import UserIdDoesNotExistError
from v1.services import users as users_service
from v1.views.base import DbSession


def get_user_parameter_from_user_id(db_session: DbSession, user_id: UUID) -> User:
    """Get user object from user id."""
    user = users_service.get_user_from_id(db_session, user_id)
    if user is None:
        raise UserIdDoesNotExistError(id_=user_id)
    return user


UserDependency = Annotated[User, Depends(get_user_parameter_from_user_id)]
