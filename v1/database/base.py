"""Database base functionality."""
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime

from v1.database.settings import DATABASE_URL, DEBUG_DATABASE

engine = create_engine(DATABASE_URL, echo=DEBUG_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
