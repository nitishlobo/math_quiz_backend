"""Module defining a test instance of the API client.

The test client will have all the required dependencies (e.g. database) overridden with the test equivalent.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import main_app
from v1.views.base import get_db_session


@pytest.fixture()
def fastapi_test_client(db_session: Generator[Session, None, None]):
    """Test FastAPI client.

    Use this to make requests to endpoints.
    Example:
        fastapi_test_client.get("/health-check")
    """

    def override_get_db_session() -> Generator[Generator[Session, None, None], None, None]:
        yield db_session

    main_app.dependency_overrides[get_db_session] = override_get_db_session
    yield TestClient(main_app)
    del main_app.dependency_overrides[get_db_session]
