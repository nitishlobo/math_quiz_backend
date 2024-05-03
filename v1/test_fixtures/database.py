"""Test database setup."""
from collections.abc import Generator
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils.functions import create_database, drop_database

from v1.settings import DEBUG_TEST_DATABASE, db_info


@pytest.fixture(scope="session")
def session_maker() -> Generator[sessionmaker[Session], Any, Any]:
    """Return a newly created test database."""
    # Modify env. database name for test database by suffixing it with test and a random uuid.
    test_db_info = db_info
    test_db_info.name = f"{test_db_info.name}-test-{uuid4().hex}"

    # Create test database
    create_database(test_db_info.url)

    engine = create_engine(test_db_info.url, echo=DEBUG_TEST_DATABASE)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield TestingSessionLocal
    drop_database(test_db_info.url)


@pytest.fixture(autouse=True)
def test_db(session_maker) -> Generator[sessionmaker[Session], Any, Any]:
    """Create new database session."""
    db = session_maker()
    db.begin_nested()
    yield db
    db.rollback()
    db.close()
