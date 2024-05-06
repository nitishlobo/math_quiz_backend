"""User database model."""

import uuid
from datetime import datetime

from sqlalchemy import DDL, DateTime, String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from v1.database.base import SqlAlchemyBase, UtcNow


class User(SqlAlchemyBase):
    """User database model."""

    __tablename__ = "users"

    id_: Mapped[uuid.UUID] = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool]
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=UtcNow())
    updated: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    deleted: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


trigger_function_modify_update_at_datetime_stamp = DDL(
    """CREATE OR REPLACE FUNCTION trigger_function_modify_update_at_datetime_stamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated = TIMEZONE('utc', CURRENT_TIMESTAMP);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """,
)

trigger_modify_update_at_datetime_stamp = DDL(
    """CREATE TRIGGER trigger_modify_update_at_datetime_stamp
        BEFORE INSERT OR UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION trigger_function_modify_update_at_datetime_stamp();
    """,
)

event.listen(User.__table__, "after_create", trigger_function_modify_update_at_datetime_stamp)
event.listen(User.__table__, "after_create", trigger_modify_update_at_datetime_stamp)
