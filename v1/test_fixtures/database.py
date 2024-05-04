"""Database related test fixtures."""

from collections.abc import Generator
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from v1.api_infra.middlewares.database import get_request_id
from v1.settings import DEBUG_TEST_DATABASE, db_info


@pytest.fixture(scope="session", name="db_connection")
def fixture_db_connection() -> Generator[Connection, None, None]:
    """Create a database and yield connection to it.

    On teardown, destroy the created database.
    """
    test_db_info = db_info
    test_db_info.name = f"test-{test_db_info.name}-{uuid4().hex}"

    # If database already exists, drop and create a fresh one again
    if database_exists(test_db_info.url):
        drop_database(test_db_info.url)

    create_database(url=test_db_info.url)

    db_engine = create_engine(url=test_db_info.url, echo=DEBUG_TEST_DATABASE)
    with db_engine.connect() as db_connection_:
        yield db_connection_

    # Teardown
    drop_database(test_db_info.url)


@pytest.fixture(autouse=True)
def db_session(db_connection: Connection) -> Generator[Session, None, None]:
    """Create a new database session."""
    db_session_factory = sessionmaker(bind=db_connection.engine, autocommit=False, autoflush=False)
    db_session_ = scoped_session(session_factory=db_session_factory, scopefunc=get_request_id)

    yield db_session_

    db_session_.rollback()
