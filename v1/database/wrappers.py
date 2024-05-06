"""Database wrappers."""

from typing import Any

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime


class UtcNow(FunctionElement):  # pylint: disable=too-many-ancestors, abstract-method
    """UTC wrapper for postgresql database."""

    type_ = DateTime()
    inherit_cache = True


@compiles(UtcNow, "postgresql")
def pg_utcnow(
    element: FunctionElement,  # pylint: disable=unused-argument
    compiler: Any,  # pylint: disable=unused-argument; # noqa: ANN401
    **kwargs: Any,  # pylint: disable=unused-argument; # noqa: ANN401
) -> str:
    """Return current UTC time for postgresql database."""
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
