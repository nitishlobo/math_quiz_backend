"""Main app for math quiz."""
from fastapi import APIRouter, FastAPI

from v1.database.base import SqlAlchemyBase, engine
from v1.routers.health_check import router as health_check_router
from v1.routers.multiplication import router as multiplication_router
from v1.routers.users import router as user_router
from v1.schemas.operands import Operand, Operands
from v1.services.multiplication import generate_times_table_grid

# Database
SqlAlchemyBase.metadata.create_all(bind=engine)

# Main app and versions
main_app = FastAPI()

# API v1 routes
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health_check_router)
v1_router.include_router(multiplication_router)
v1_router.include_router(user_router)

# Main app routes
main_app.include_router(health_check_router)
main_app.include_router(v1_router)


if __name__ == "__main__":
    operands = Operands(first=Operand(min_=2, max_=12), second=Operand(min_=1, max_=12))
    times_table = generate_times_table_grid(operands)
