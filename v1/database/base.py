"""Database base functionality."""

from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime


class SqlAlchemyBase(DeclarativeBase):
    """Base SQL alchemy model."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_N_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
    )


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
