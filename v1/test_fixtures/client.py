"""Module defining a test instance of the API client.

The test client will have all the required dependencies (e.g. database) overridden with the test equivalent.
"""


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
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
    db_session: Session,  # pylint: disable=unused-argument
    db_connection: Connection,
) -> TestClient:
    """Test FastAPI client.

    Use this to make requests to endpoints.
    Example:
        fastapi_test_client.get("/health-check")
    """
    main_app.state.db_connection = db_connection
    return TestClient(test_app)
