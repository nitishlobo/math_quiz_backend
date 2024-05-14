"""FastAPI database lifespans."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from v1.database.connections import db_engine


@asynccontextmanager
async def database_connection_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Attach a database connection to the FastAPI application."""
    with db_engine.connect() as db_connection:
        app.state.db_connection = db_connection
        yield
