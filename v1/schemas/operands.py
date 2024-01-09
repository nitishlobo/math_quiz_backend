"""Schemas for operands."""
from pydantic import BaseModel


class Operand(BaseModel):
    """Settings for operand."""

    min_: int
    max_: int


class Operands(BaseModel):
    """Operands for a maths problem."""

    first: Operand
    second: Operand
