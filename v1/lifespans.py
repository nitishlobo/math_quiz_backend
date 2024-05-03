"""FastAPI lifespan events."""

from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

from fastapi import FastAPI
from sqlalchemy.engine import Connection

from v1.database.connections import create_database_connection
from v1.settings import DEBUG_DATABASE, db_info


class LifespanStates(TypedDict):
    """API lifespan states."""

    # http_client: httpx.AsyncClient
    db_connection: Connection


@asynccontextmanager
async def database_connection_lifespan(_app: FastAPI) -> AsyncGenerator[Connection, None]:
    """Attach a database connection to the FastAPI application."""
    with create_database_connection(db_url=db_info.url, debug_db=DEBUG_DATABASE) as db_connection:
        yield db_connection


@asynccontextmanager
async def lifespans(app: FastAPI) -> AsyncIterator[LifespanStates]:
    """Attach all lifespans to the FastAPI application.

    See https://fastapi.tiangolo.com/advanced/events/ for details.
    """
    # async with database_connection_lifespan(app) as db_connection, httpx.AsyncClient() as client:
    #     yield {"http_client": client, "db_connection": db_connection}
    async with database_connection_lifespan(app) as db_connection:
        yield {"db_connection": db_connection}
