"""Main app for math quiz."""
from fastapi import APIRouter, FastAPI

from v1.multiplication.router import router as multiplication_router
from v1.multiplication.service import generate_times_table_grid
from v1.operands.schemas import Operand, Operands
from v1.ping.router import router as ping_router

# Main app and versions
main_app = FastAPI()

# API v1 routes
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(ping_router)
v1_router.include_router(multiplication_router)

# Main app routes
main_app.include_router(ping_router)
main_app.include_router(v1_router)


if __name__ == "__main__":
    operands = Operands(first=Operand(min_=2, max_=12), second=Operand(min_=1, max_=12))
    times_table = generate_times_table_grid(operands)
