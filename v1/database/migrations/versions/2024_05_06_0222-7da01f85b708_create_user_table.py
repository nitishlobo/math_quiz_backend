"""Create user table.

Revision ID: 7da01f85b708
Revises:
Create Date: 2024-05-06 02:22:36.863036+00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Revision identifiers used by Alembic
revision: str = "7da01f85b708"
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
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    # Manually written code
    op.execute(
        """CREATE OR REPLACE FUNCTION trigger_function__modify_updated_at_to_current_timestamp()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = TIMEZONE('utc', CURRENT_TIMESTAMP);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """,
    )
    op.execute(
        """CREATE TRIGGER trigger__modify_updated_at_to_current_timestamp
            BEFORE INSERT OR UPDATE ON users
            FOR EACH ROW
            EXECUTE FUNCTION trigger_function__modify_updated_at_to_current_timestamp();
        """,
    )


def downgrade() -> None:
    """Perform downgrade actions on the database."""
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    # Manually written code
    op.execute("DROP TRIGGER IF EXISTS trigger__modify_updated_at_to_current_timestamp ON users")
    op.execute("DROP FUNCTION IF EXISTS trigger_function__modify_updated_at_to_current_timestamp")
