"""Main app for math quiz."""
from fastapi import FastAPI

from routers import multiplication, ping
from schemas.operands import Operand, Operands
from services.multiplication import generate_times_table_grid

# Main app and versions
main_app = FastAPI()
app_v1 = FastAPI()

# Main app routes
main_app.include_router(ping.router)

# API v1 routes
app_v1.include_router(ping.router)
app_v1.include_router(multiplication.router)

# Attach API v1 to main app
main_app.mount("/v1", app_v1)


if __name__ == "__main__":
    operands = Operands(first=Operand(min_=2, max_=12), second=Operand(min_=1, max_=12))
    times_table = generate_times_table_grid(operands)
