"""Endpoints relating to multiplication operations."""
from collections.abc import Sequence

from schemas.operands import Operand, Operands
from services.multiplication import generate_times_table_grid

from routers.settings.routers import APIRouter
from routers.settings.tags import RouteTags

router = APIRouter(prefix="/multiplication", tags=[RouteTags.MULTIPLICATION])


@router.post("/")
async def create_multiplication_dataset() -> Sequence[tuple]:
    """Create multiplication dataset."""
    operands = Operands(first=Operand(min_=2, max_=12), second=Operand(min_=1, max_=12))
    return generate_times_table_grid(operands)
