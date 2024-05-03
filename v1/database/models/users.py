"""User database model."""
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from v1.database.base import SqlAlchemyBase, UtcNow


class User(SqlAlchemyBase):
    """User database model."""

    __tablename__ = "users"

    id_ = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_superuser = Column(Boolean)
    created = Column(DateTime(timezone=True), server_default=UtcNow())
    updated = Column(DateTime(timezone=True), onupdate=UtcNow())
    deleted = Column(DateTime(timezone=True))
