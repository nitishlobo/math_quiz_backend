"""Schemas relating directly to database information."""

from typing import Self

from pydantic import BaseModel


class DatabaseInfo(BaseModel):
    """Database connection information."""

    type_: str
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def url(self: Self) -> str:
        """Return database connection URL."""
        return f"{self.type_}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
