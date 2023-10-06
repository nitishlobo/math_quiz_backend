"""Router related code."""
from typing import Any, Callable

from fastapi import APIRouter as FastAPIRouter
from typing_extensions import Self


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
