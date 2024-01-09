"""Services for multiplication."""
from collections.abc import Sequence

from v1.schemas.operands import Operands


# TODO: split `operands` argument into two arguments - first operator and second operator.
def generate_times_table_grid(operands: Operands) -> Sequence[tuple[int, int, int]]:
    """Return a list of tuples with each tuple containing operands and the correct solution.

    Keywords:
    operands -- operand settings for multiplication
    """
    times_table = []
    for first_op in range(operands.first.min_, operands.first.max_ + 1):
        for second_op in range(operands.second.min_, operands.second.max_ + 1):
            times_table.append((first_op, second_op, first_op * second_op))
    return times_table
