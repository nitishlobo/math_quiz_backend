"""Functionality relating to database connections."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection


@contextmanager
def create_database_connection(db_url: str, *, debug_db: bool) -> Generator[Connection, None, None]:
    """Create a database connection."""
    db_engine = create_engine(url=db_url, echo=debug_db)
    with db_engine.connect() as db_connection:
        yield db_connection
