"""Database related test fixtures."""

from collections.abc import Generator
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import scoped_session
from sqlalchemy_utils import create_database, database_exists, drop_database

from v1.api_infra.middlewares.database import get_request_id
from v1.database.base import SqlAlchemyBase
from v1.database.connections import create_db_session
from v1.database.models.test_factories.users import UserFactory
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

    # Create all the database tables
    SqlAlchemyBase.metadata.create_all(db_engine)

    with db_engine.connect() as db_connection:
        # Create a session
        db_session = create_db_session(db_engine=db_connection.engine, scoped_session_func=get_request_id)
        # Attach factories to the current session
        UserFactory._meta.sqlalchemy_session = db_session  # pylint: disable=protected-access
        yield db_connection

    # Teardown
    drop_database(test_db_info.url)


@pytest.fixture(autouse=True, name="db_session")
def fixture_db_session(db_connection: Connection) -> Generator[scoped_session, None, None]:
    """Create a new database session."""
    db_session = create_db_session(db_engine=db_connection.engine, scoped_session_func=get_request_id)

    yield db_session

    db_session.rollback()
