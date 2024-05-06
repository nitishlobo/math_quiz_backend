"""${message}.

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
${imports if imports else ""}

# Revision identifiers used by Alembic
revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    """Perform upgrade actions on the database."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Perform downgrade actions on the database."""
    ${downgrades if downgrades else "pass"}
