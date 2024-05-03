"""Module defining a test instance of the API client.

The test client will have all the required dependencies (e.g. database) overriden with the test equivalent.
"""
from collections.abc import Generator
from typing import Any
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from main import main_app
from v1.database.base import get_db, get_engine, get_session
from v1.settings import DEBUG_TEST_DATABASE, db_info

test_db_info = db_info
test_db_info.name = f"{test_db_info.name}-test-{uuid4().hex}"


def get_test_engine(database_info, debug_database):
    # Create test database if it does not exist
    if database_exists(database_info.url):
        drop_database(database_info.url)
    create_database(database_info.url)

    return create_engine(database_info.url, echo=debug_database)


def get_test_session(database_info, debug_database):
    engine = get_test_engine(database_info, debug_database)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_db():
    """Create new database session."""
    TestingSessionLocal = get_test_session(test_db_info, DEBUG_TEST_DATABASE)
    db = TestingSessionLocal()
    db.begin_nested()
    yield db
    db.rollback()
    db.close()
    # drop_database(test_db_info.url)


@pytest.fixture()
def test_client() -> Generator[TestClient, Any, None]:
    main_app.dependency_overrides[get_engine] = get_test_engine
    main_app.dependency_overrides[get_session] = get_test_session
    main_app.dependency_overrides[get_db] = test_db
    return TestClient(main_app)


# def get_test_db(test_db):
#     yield test_db


# @pytest.fixture(scope="function")
# def test_client() -> Generator[TestClient, Any, None]:
#     main_app.dependency_overrides[get_db] = get_test_db
#     yield TestClient(main_app)
