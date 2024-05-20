"""Exception handlers for users."""

from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from v1.exceptions.users import UserAlreadyExistsError, UserIdDoesNotExistError


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
        content={"message": f"User id {exc.id_!s} does not exist."},
    )
