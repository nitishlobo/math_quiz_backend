"""Common database functionality."""

from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import DateTime

from v1.database.wrappers import UtcNow


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


class TimeAudit:
    """Datetime-with-timezone-stamp fields used for auditing tables.

    For every database table that has the columns defined in this class,
    the updated_at column will have a trigger before insert and update to update the field to the current timestamp.
    See the `triggers` module in this project for execution details.
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=UtcNow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
