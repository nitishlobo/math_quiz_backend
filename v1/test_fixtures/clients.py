"""Module defining a test instance of the API client.

The test client will have all the required dependencies (e.g. database) overridden with the test equivalent.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from main import main_app


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    """Test FastAPI app."""
    return main_app


@pytest.fixture()
def fastapi_test_client(
    test_app: FastAPI,
    db_session: Session,
    db_connection: Connection,
    mocker: MockerFixture,
) -> TestClient:
    """Test FastAPI client.

    Use this to make requests to endpoints.
    Example:
        fastapi_test_client.get("/health-check")
    """
    main_app.state.db_connection = db_connection
    # Use the database session created in the pytest fixture
    mocker.patch("v1.api_infra.middlewares.database.create_db_session", return_value=db_session)
    return TestClient(test_app)
