"""Exception handlers for users."""

from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from v1.exceptions.users import UserAlreadyExistsError, UserHasBeenPreviouslyDeletedError, UserIdDoesNotExistError


async def user_already_exists_exception_handler(_request: Request, exc: UserAlreadyExistsError) -> JSONResponse:
    """Return 400 when user already exists."""
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"message": f"User {exc.email} already exists. Cannot create a user who already exists."},
    )


async def user_id_does_not_exist_exception_handler(_request: Request, exc: UserIdDoesNotExistError) -> JSONResponse:
    """Return 400 when user id does not exists."""
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"message": f"User id {exc.id!s} does not exist."},
    )


async def user_has_been_previously_deleted_exception_handler(
    _request: Request,
    exc: UserHasBeenPreviouslyDeletedError,
) -> JSONResponse:
    """Return 400 when user has been deleted previously."""
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"message": f"User {exc.email} has been previously deleted at {exc.deleted_at.isoformat()}."},
    )
