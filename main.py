"""Main app for math quiz."""
from fastapi import FastAPI

from v1.multiplication import router as multiplication_router
from v1.multiplication.service import generate_times_table_grid
from v1.operands.schemas import Operand, Operands
from v1.ping import router as ping_router

# Main app and versions
main_app = FastAPI()
app_v1 = FastAPI()

# Main app routes
main_app.include_router(ping_router.router)

# API v1 routes
app_v1.include_router(ping_router.router)
app_v1.include_router(multiplication_router.router)

# Attach API v1 to main app
main_app.mount("/v1", app_v1)


if __name__ == "__main__":
    operands = Operands(first=Operand(min_=2, max_=12), second=Operand(min_=1, max_=12))
    times_table = generate_times_table_grid(operands)
