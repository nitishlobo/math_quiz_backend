"""Main app for math quiz."""

from fastapi import APIRouter, FastAPI

from v1.api_infra.lifespans.all import lifespans
from v1.exceptions.handlers.users import user_already_exists_exception_handler, user_id_does_not_exist_exception_handler
from v1.exceptions.users import UserAlreadyExistsError, UserIdDoesNotExistError
from v1.settings import APP_TITLE, DEBUG_FASTAPI_APP
from v1.views.health_check import router as health_check_router
from v1.views.users import router as user_router

# Main app and versions
main_app = FastAPI(title=APP_TITLE, version="1.0.0", lifespan=lifespans, debug=DEBUG_FASTAPI_APP)

# API v1 routes
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health_check_router)
v1_router.include_router(user_router)

# Main app routes
main_app.include_router(health_check_router)
main_app.include_router(v1_router)

# Exceptions
main_app.exception_handler(UserAlreadyExistsError)(user_already_exists_exception_handler)
main_app.exception_handler(UserIdDoesNotExistError)(user_id_does_not_exist_exception_handler)
