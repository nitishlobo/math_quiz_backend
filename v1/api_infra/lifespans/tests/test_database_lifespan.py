"""Test database lifespan for FastAPI."""

import pytest
from fastapi import FastAPI
from pytest_mock import MockerFixture

from v1.api_infra.lifespans.database import database_connection_lifespan
from v1.test_fixtures.database import testing_db_engine


@pytest.mark.asyncio()
async def test_database_connection_lifespan(mocker: MockerFixture):
    """Test database connection lifespan for FastAPI."""
    # Setup app with test database engine
    app = FastAPI()
    mocker.patch("v1.api_infra.lifespans.database.db_engine", testing_db_engine)
    async with database_connection_lifespan(app):
        pass

    # Verify that db_connection is in the FastAPI's app state
    app_state = app.state.__dict__.get("_state", {})
    assert "db_connection" in app_state
    # Verify that connection was made and it was using the correct engine
    assert app_state["db_connection"].engine == testing_db_engine
