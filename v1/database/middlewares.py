"""Database middleware.

The code in this module is based on:
https://github.com/Netflix/dispatch/blob/master/src/dispatch/main.py
"""

from contextvars import ContextVar
from typing import Final
from uuid import uuid1

from fastapi import Request, Response
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.middleware.base import RequestResponseEndpoint

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[str | None] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> str | None:
    """Return the unique ID of the current request."""
    return _request_id_ctx_var.get()


async def db_session_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Attach a database session to the request."""
    # Based on: https://github.com/Netflix/dispatch/blob/master/src/dispatch/main.py
    request_id = str(uuid1())

    # We create a per-request id such that we can ensure that our session is scoped for a particular request.
    # See: https://github.com/tiangolo/fastapi/issues/726
    ctx_token = _request_id_ctx_var.set(request_id)

    try:
        # Create a database session
        with request.state.db_connection as db_connection:
            db_session_factory = sessionmaker(engine=db_connection.engine, autocommit=False, autoflush=False)
            db_session = scoped_session(session_factory=db_session_factory, scopefunc=get_request_id)

        # Attach database session to the request
        request.state.db_session = db_session

        # Get response from the call and commit if status was a success, otherwise rollback
        response = await call_next(request)
        if response.status_code < 400:
            db_session.commit()
        else:
            db_session.rollback()
    finally:
        _request_id_ctx_var.reset(ctx_token)

    return response
