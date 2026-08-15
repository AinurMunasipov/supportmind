"""Add importance to memories.

Revision ID: 20260815_0001
Revises:
Create Date: 2026-08-15
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260815_0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.add_column(
        "memories",
        sa.Column(
            "importance",
            sa.Integer(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("memories", "importance")
