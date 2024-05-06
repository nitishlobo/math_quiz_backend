"""Functionality relating to database connections."""

from collections.abc import Callable, Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import scoped_session, sessionmaker


@contextmanager
def create_database_connection(db_url: str, *, debug_db: bool) -> Generator[Connection, None, None]:
    """Create a database connection."""
    db_engine = create_engine(url=db_url, echo=debug_db)
    with db_engine.connect() as db_connection:
        yield db_connection


def create_db_session(
    db_engine: Engine,
    scoped_session_func: Callable,
    sessionmaker_args: dict | None = None,
    scoped_session_args: dict | None = None,
) -> scoped_session:
    """Create a database session."""
    if sessionmaker_args is None:
        sessionmaker_args = {}
    if scoped_session_args is None:
        scoped_session_args = {}

    # Default autocommit and autoflush to False if not provided in sessionmaker_args
    if "autocommit" not in sessionmaker_args:
        sessionmaker_args["autocommit"] = False
    if "autoflush" not in sessionmaker_args:
        sessionmaker_args["autoflush"] = False

    db_session_factory = sessionmaker(bind=db_engine, **sessionmaker_args)
    return scoped_session(session_factory=db_session_factory, scopefunc=scoped_session_func, **scoped_session_args)
