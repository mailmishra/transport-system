"""widen consignor, consignee, goods_description to Text

Revision ID: 0007
Revises: 0006
Create Date: 2026-09-25
"""

import sqlalchemy as sa
from alembic import op

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("bilties", "consignor", type_=sa.Text(), existing_nullable=False)
    op.alter_column("bilties", "consignee", type_=sa.Text(), existing_nullable=False)
    op.alter_column("bilties", "goods_description", type_=sa.Text(), existing_nullable=False)


def downgrade() -> None:
    op.alter_column("bilties", "consignor", type_=sa.String(200), existing_nullable=False)
    op.alter_column("bilties", "consignee", type_=sa.String(200), existing_nullable=False)
    op.alter_column("bilties", "goods_description", type_=sa.String(300), existing_nullable=False)
