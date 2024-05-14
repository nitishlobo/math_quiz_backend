"""Test database connections module."""

import contextlib
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from v1.database.connections import get_db_session


def test_get_db_session(mocker: MockerFixture):
    """Test get database session."""
    # Mock the DbSessionLocal to ensure no real database connection is made
    mock_db_session = MagicMock()
    mock_db_session.close = MagicMock()

    mocker.patch("v1.database.connections.DbSessionLocal", return_value=mock_db_session)

    db_session = get_db_session()
    # Assert that the session is the mock session
    assert next(db_session) is mock_db_session

    # Iterate the generator to close the session and check the cleanup has been called
    with contextlib.suppress(StopIteration):
        next(db_session)
    mock_db_session.close.assert_called_once()
