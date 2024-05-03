"""FastAPI database lifespans."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from v1.database.connections import create_database_connection
from v1.settings import DEBUG_DATABASE, db_info


@asynccontextmanager
async def database_connection_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Attach a database connection to the FastAPI application."""
    with create_database_connection(db_url=db_info.url, debug_db=DEBUG_DATABASE) as db_connection:
        app.state.db_connection = db_connection
        yield
