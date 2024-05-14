"""Test all FastAPI lifespans."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from pytest_mock import MockerFixture

from v1.api_infra.lifespans.all import lifespans


@pytest.mark.asyncio()
async def test_lifespans(mocker: MockerFixture):
    """Test FastAPI lifespans."""
    # Setup app with mocked lifespans
    app = FastAPI()
    mock_database_connection_lifespan = mocker.patch(
        "v1.api_infra.lifespans.all.database_connection_lifespan",
        MagicMock(AsyncMock),
    )

    async with lifespans(app):
        # Verify that database_connection_lifespan is invoked with the app
        mock_database_connection_lifespan.assert_called_once_with(app)

    # Verify database lifespan is cleaned up properly
    mock_database_connection_lifespan.return_value.__aexit__.assert_called_once()
