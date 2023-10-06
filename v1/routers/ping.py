"""Health check endpoints."""
from v1.routers.settings.routers import APIRouter
from v1.routers.settings.tags import RouteTags

router = APIRouter(prefix="/ping", tags=[RouteTags.PING])


@router.get("/")
def ping() -> dict:
    """Health check endpoint."""
    return {"message": "pong"}
