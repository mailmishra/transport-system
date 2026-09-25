"""bilties: add weight_per_bag for auto-calculating total weight from package count

Revision ID: 0006
Revises: 0005
Create Date: 2026-09-25

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bilties", sa.Column("weight_per_bag", sa.Numeric(12, 3), nullable=True))


def downgrade() -> None:
    op.drop_column("bilties", "weight_per_bag")
