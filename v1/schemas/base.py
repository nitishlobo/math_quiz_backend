"""Common schemas."""

from pydantic import BaseModel


class DeleteResponse(BaseModel):
    """Delete response for the API."""

    message: str = "success"
