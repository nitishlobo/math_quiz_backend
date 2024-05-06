"""Module defining trigger functions for database."""

from sqlalchemy import DDL


def trigger_function_modify_updated_at_to_current_timestamp() -> DDL:
    """Return a definition for a trigger function to modify updated_at column with the current datetime stamp."""
    return DDL(
        """CREATE OR REPLACE FUNCTION trigger_function__modify_updated_at_to_current_timestamp()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = TIMEZONE('utc', CURRENT_TIMESTAMP);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """,
    )
