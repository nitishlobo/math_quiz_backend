"""Database base functionality."""

from typing import Annotated, Any

from fastapi import Depends, Request
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime

SqlAlchemyBase = declarative_base()


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


def get_db(request: Request) -> Session:
    """Return current database session from fastapi request state."""
    return request.state.db_session


DbSession = Annotated[Session, Depends(get_db)]
