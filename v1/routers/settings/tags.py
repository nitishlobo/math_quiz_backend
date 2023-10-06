"""API route tags to be used in documentation (e.g. OpenAPI Schema)."""
from enum import Enum


class RouteTags(Enum):
    """Tags for API routes."""

    # Health check
    PING = "ping"

    # Operations
    MULTIPLICATION = "multiplication"
