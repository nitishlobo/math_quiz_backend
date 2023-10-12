"""Health check endpoints."""
from v1.router import APIRouter, RouteTags

router = APIRouter(prefix="/ping", tags=[RouteTags.PING])


@router.get("/")
def ping() -> dict:
    """Health check endpoint."""
    return {"message": "pong"}
