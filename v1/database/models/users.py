"""User database model."""

from sqlalchemy.orm import Mapped, mapped_column

from v1.database.models.base import SqlAlchemyBase, TimeAudit
from v1.database.models.types import ColumnTypes


class User(SqlAlchemyBase, TimeAudit):
    """User database model."""

    __tablename__ = "users"

    id: Mapped[ColumnTypes.id_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool]
