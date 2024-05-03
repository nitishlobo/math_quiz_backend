"""All FastAPI lifespans.

If there are more than 3 lifespans, then we would want to use a lifespan manager. For ideas, see:
- https://github.com/tiangolo/fastapi/discussions/9397
- https://github.com/uriyyo/fastapi-lifespan-manager
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from v1.api_infra.lifespans.database import database_connection_lifespan


@asynccontextmanager
async def lifespans(app: FastAPI) -> AsyncGenerator[None, None]:
    """Attach all lifespans to the FastAPI application.

    See https://fastapi.tiangolo.com/advanced/events/ for details.
    """
    async with database_connection_lifespan(app):
        yield
