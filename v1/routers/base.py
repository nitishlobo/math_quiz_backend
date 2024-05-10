"""Router related code."""

from collections.abc import Callable
from enum import Enum
from typing import Annotated, Any, Self

from fastapi import APIRouter as FastAPIRouter
from fastapi import Depends, Request
from sqlalchemy.orm.session import Session


class APIRouter(FastAPIRouter):
    """API router class to resolve 307 Temporary Redirect issue.

    Refer to here: https://github.com/tiangolo/fastapi/issues/2060
    """

    def add_api_route(
        self: Self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        include_in_schema: bool = True,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Override for original API route."""
        alternate_path = path[:-1] if path.endswith("/") else path + "/"
        super().add_api_route(alternate_path, endpoint, include_in_schema=False, **kwargs)
        return super().add_api_route(path, endpoint, include_in_schema=include_in_schema, **kwargs)


class RouteTags(Enum):
    """API route tags that can be used in documentation (e.g. OpenAPI Schema)."""

    HEALTH_CHECK = "health-check"
    USERS = "users"


def get_db_session(request: Request) -> Session:
    """Return current database session from fastapi request state."""
    return request.state.db_session  # type: ignore[no-any-return]


DbSession = Annotated[Session, Depends(get_db_session)]
