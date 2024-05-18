"""Common database functionality."""

from datetime import datetime
from typing import Any

from sqlalchemy import MetaData, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import DateTime

from v1.database.models.types import ColumnTypes
from v1.database.triggers.functions import trigger_function_modify_updated_at_to_current_timestamp
from v1.database.triggers.triggers import trigger_modify_updated_at_to_current_timestamp
from v1.database.wrappers import UtcNow
from v1.utils.utils import get_class_variables


class SqlAlchemyBase(DeclarativeBase):
    """Base SQL alchemy model."""

    metadata = MetaData(
        # The following shortforms stand for the following constraints
        # ix=index, uq=unique, ck=check, fk=foreign key, pk=primary key
        naming_convention={
            "ix": "ix_%(column_0_N_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
    )

    def to_dict(self) -> dict[str, Any]:
        """Return SQL Alchemy model as a dictionary."""
        return {key: value for key, value in self.__dict__.items() if key != "_sa_instance_state"}


class TimeAudit:
    """Datetime-with-timezone-stamp fields used for auditing tables.

    For every database table that has the columns defined in this class,
    the updated_at column will have a trigger before insert and update to update the field to the current timestamp.
    See the `triggers` module in this project for execution details.
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=UtcNow())
    updated_at: Mapped[ColumnTypes.datetime_tz]
    deleted_at: Mapped[ColumnTypes.datetime_tz | None]


def attach_trigger_function_to_modify_updated_at_to_current_timestamp(
    _target: MetaData,
    db_connection: Connection,
    **_kwargs: dict[str, Any],
) -> None:
    """Attach a trigger function to modify the updated_at column to be the current timestamp."""
    trigger_function = trigger_function_modify_updated_at_to_current_timestamp()
    db_connection.execute(trigger_function)


def attach_trigger_to_modify_updated_at_to_current_timestamp(
    target: MetaData,
    db_connection: Connection,
    **_kwargs: dict[str, Any],
) -> None:
    """Attach a trigger function to modify the updated_at column to be the current timestamp."""
    time_audit_columns = get_class_variables(TimeAudit)
    for key in target.tables:
        current_table = target.tables[key]

        # Check if current table contains TimeAudit columns
        current_table_columns = {col.name for col in current_table.columns}
        if time_audit_columns.issubset(current_table_columns):
            db_connection.execute(trigger_modify_updated_at_to_current_timestamp(current_table.name))


event.listen(
    SqlAlchemyBase.metadata,
    "after_create",
    attach_trigger_function_to_modify_updated_at_to_current_timestamp,
)
event.listen(
    SqlAlchemyBase.metadata,
    "after_create",
    attach_trigger_to_modify_updated_at_to_current_timestamp,
)
