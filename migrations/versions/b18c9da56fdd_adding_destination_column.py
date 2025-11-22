"""adding destination column

Revision ID: b18c9da56fdd
Revises: a77c8afce060
Create Date: 2025-11-22 09:46:33.580805

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b18c9da56fdd"
down_revision: Union[str, Sequence[str], None] = "a77c8afce060"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "shipments",
        sa.Column(
            "destination",
            sa.INTEGER,
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("shipments", "destination")
    pass
