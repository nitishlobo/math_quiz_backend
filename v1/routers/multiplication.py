"""Endpoints relating to multiplication operations."""
from collections.abc import Sequence

from v1.routers.base import APIRouter, RouteTags
from v1.schemas.operands import Operand, Operands
from v1.services.multiplication import generate_times_table_grid

router = APIRouter(prefix="/multiplication", tags=[RouteTags.MULTIPLICATION])


@router.post("/")
async def create_multiplication_dataset() -> Sequence[tuple[int, int, int]]:
    """Create multiplication dataset."""
    operands = Operands(first=Operand(min_=2, max_=12), second=Operand(min_=1, max_=12))
    # TODO: Change return data
    return generate_times_table_grid(operands)
