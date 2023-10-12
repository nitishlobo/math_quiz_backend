"""User database model."""
import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from v1.database import SqlAlchemyBase, UtcNow


class User(SqlAlchemyBase):
    """User database model."""

    __tablename__ = "users"

    id_ = Column(UUID(as_uuid=True), alias="id", primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created = Column(DateTime(timezone=True), server_default=UtcNow())
    updated = Column(DateTime(timezone=True), onupdate=UtcNow())
    deleted = Column(DateTime(timezone=True))
