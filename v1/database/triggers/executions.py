"""Module defining executions for trigger functions and triggers for database."""

from typing import Any

from sqlalchemy import MetaData, event
from sqlalchemy.engine import Connection

from v1.database.models.base import SqlAlchemyBase, TimeAudit
from v1.database.triggers.functions import trigger_function_modify_updated_at_to_current_timestamp
from v1.database.triggers.triggers import trigger_modify_updated_at_to_current_timestamp
from v1.utils import get_class_variables


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
