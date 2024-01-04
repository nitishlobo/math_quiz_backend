"""Health check endpoints."""
from v1.router import APIRouter, RouteTags

router = APIRouter(prefix="/health-check", tags=[RouteTags.HEALTH_CHECK])


@router.get("/")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"message": "Alive and well!"}
