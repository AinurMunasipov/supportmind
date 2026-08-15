"""Add summary to memories.

Revision ID: 20260815_0002
Revises: 20260815_0001
Create Date: 2026-08-15
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260815_0002"
down_revision: str | None = "20260815_0001"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.add_column(
        "memories",
        sa.Column(
            "summary",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("memories", "summary")
