"""Database table column type mappings.

As per the SQLAlchemy conventions the following shortforms are used:
    Constraints:
        - ix=index, uq=unique, ck=check, fk=foreign key, pk=primary key

    Types:
        - tz=timezone
"""

import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column
from sqlalchemy.types import DateTime


class ColumnTypes:
    """Class that defines common database column types."""

    # UUID types
    id_pk = Annotated[uuid.UUID, mapped_column(primary_key=True, index=True, default=uuid.uuid4)]

    # Datetime types
    datetime_tz = Annotated[datetime, mapped_column(DateTime(timezone=True))]
