"""Module defining triggers for database."""

from sqlalchemy import DDL


def trigger_modify_updated_at_to_current_timestamp(table_name: str) -> DDL:
    """Return a definition for a trigger on the updated_at column on the specified table."""
    return DDL(
        f"""CREATE TRIGGER trigger__modify_updated_at_to_current_timestamp
            BEFORE INSERT OR UPDATE ON {table_name}
            FOR EACH ROW
            EXECUTE FUNCTION trigger_function__modify_updated_at_to_current_timestamp();
        """,
    )
