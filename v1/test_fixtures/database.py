"""Database related test fixtures.

Based on: https://stackoverflow.com/a/67348153/5702056
"""

import importlib
import pkgutil
from collections.abc import Generator
from uuid import uuid4

import pytest
from sqlalchemy import RootTransaction, create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from v1.database.models.base import SqlAlchemyBase
from v1.database.models.test_factories.base import BaseFactory
from v1.settings import DEBUG_TEST_DATABASE, db_info

testing_db_info = db_info
testing_db_info.name = f"test-{testing_db_info.name}-{uuid4().hex}"
testing_db_engine = create_engine(url=testing_db_info.url, echo=DEBUG_TEST_DATABASE)
TestingDbSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=testing_db_engine)


def get_database_model_factories() -> list[type(BaseFactory)]:
    """Return a list of factories for database models."""
    package = "v1.database.models.test_factories"

    # Iterate through all modules in the test_factories package and load these modules
    for _importer, modname, _ispkg in pkgutil.iter_modules(importlib.import_module(package).__path__):
        full_module_name = f"{package}.{modname}"
        importlib.import_module(full_module_name)

    return BaseFactory.__subclasses__()


def add_database_model_factories_to_db_session(provided_db_session: Session) -> None:
    """Add all database model factories to the provided database session."""
    factory_models = get_database_model_factories()
    for factory in factory_models:
        factory._meta.sqlalchemy_session = provided_db_session  # pylint: disable=protected-access


@pytest.fixture(scope="session", autouse=True)
def _testing_db() -> Generator[None, None, None]:
    """Create a test database."""
    # If database already exists, drop and create a fresh one again
    if database_exists(testing_db_info.url):
        drop_database(testing_db_info.url)

    create_database(url=testing_db_info.url)

    SqlAlchemyBase.metadata.create_all(bind=testing_db_engine)
    yield
    SqlAlchemyBase.metadata.drop_all(bind=testing_db_engine)
    drop_database(testing_db_info.url)


@pytest.fixture(name="db_session")
def fixture_db_session(_testing_db: Generator[None, None, None]):
    """Yield a test database session.

    Create a nested transaction, recreate it when the application code calls session.commit()
    and roll it back at the end.
    """
    db_connection = testing_db_engine.connect()
    db_transaction = db_connection.begin()
    db_session = TestingDbSessionLocal(bind=db_connection)

    # Attach factories to the current session
    add_database_model_factories_to_db_session(db_session)

    # Begin a nested transaction (using SAVEPOINT).
    nested = db_connection.begin_nested()

    @event.listens_for(db_session, "after_transaction_end")
    def end_savepoint(_session: Session, _transaction: RootTransaction) -> None:
        """Start a new savepoint if the application code calls session.commit().

        This is because when session.commit() is called, it will end the nested transaction.
        """
        nonlocal nested
        if not nested.is_active:
            nested = db_connection.begin_nested()

    yield db_session

    # Rollback the overall transaction, restoring the state before the test ran.
    db_session.close()
    db_transaction.rollback()
    db_connection.close()
