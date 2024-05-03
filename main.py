"""Main app for math quiz."""

from fastapi import APIRouter, FastAPI

from v1.database.middlewares import db_session_middleware
from v1.lifespans import lifespans
from v1.routers.health_check import router as health_check_router
from v1.routers.multiplication import router as multiplication_router
from v1.routers.users import router as user_router
from v1.schemas.operands import Operand, Operands
from v1.services.multiplication import generate_times_table_grid
from v1.settings import APP_TITLE, DEBUG_FASTAPI_APP

# Main app and versions
main_app = FastAPI(title=APP_TITLE, version="1.0.0", lifespan=lifespans, debug=DEBUG_FASTAPI_APP)

# API v1 routes
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health_check_router)
v1_router.include_router(multiplication_router)
v1_router.include_router(user_router)

# Main app routes
main_app.include_router(health_check_router)
main_app.include_router(v1_router)

# Middlewares
main_app.middleware("http")(db_session_middleware)


if __name__ == "__main__":
    operands = Operands(first=Operand(min_=2, max_=12), second=Operand(min_=1, max_=12))
    times_table = generate_times_table_grid(operands)
