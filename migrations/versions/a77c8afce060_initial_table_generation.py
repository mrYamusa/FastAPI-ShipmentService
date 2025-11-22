"""initial table generation

Revision ID: a77c8afce060
Revises:
Create Date: 2025-11-20 21:09:44.671573

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a77c8afce060"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "shipments",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("content", sa.CHAR, nullable=False),
        sa.Column("status", sa.CHAR, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("shipments")
