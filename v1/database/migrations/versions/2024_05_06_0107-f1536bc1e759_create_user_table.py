"""Add trigger function.

Revision ID: f1536bc1e759
Revises:
Create Date: 2024-05-06 01:07:13.803950+00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Revision identifiers used by Alembic
revision: str = "f1536bc1e759"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Perform upgrade actions on the database."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("updated", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    # Manually written code
    op.execute(
        """CREATE OR REPLACE FUNCTION trigger_function_modify_update_at_datetime_stamp()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated = TIMEZONE('utc', CURRENT_TIMESTAMP);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """,
    )
    op.execute(
        """CREATE TRIGGER trigger_modify_update_at_datetime_stamp
            BEFORE INSERT OR UPDATE ON users
            FOR EACH ROW
            EXECUTE FUNCTION trigger_function_modify_update_at_datetime_stamp();
        """,
    )


def downgrade() -> None:
    """Perform downgrade actions on the database."""
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    # Manually written code
    op.execute("DROP TRIGGER IF EXISTS trigger_modify_update_at_datetime_stamp ON users")
    op.execute("DROP FUNCTION IF EXISTS trigger_function_modify_update_at_datetime_stamp")
