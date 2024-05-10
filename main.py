"""Main app for math quiz."""

from fastapi import APIRouter, FastAPI

from v1.api_infra.lifespans.all import lifespans
from v1.api_infra.middlewares.database import db_session_middleware
from v1.routers.health_check import router as health_check_router
from v1.routers.users import router as user_router
from v1.settings import APP_TITLE, DEBUG_FASTAPI_APP

# Main app and versions
main_app = FastAPI(title=APP_TITLE, version="1.0.0", lifespan=lifespans, debug=DEBUG_FASTAPI_APP)

# API v1 routes
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health_check_router)
v1_router.include_router(user_router)

# Main app routes
main_app.include_router(health_check_router)
main_app.include_router(v1_router)

# Middlewares
main_app.middleware("http")(db_session_middleware)
