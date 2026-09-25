"""bilti goods_items JSONB + party/invoice fields + un_load_labour

Revision ID: 0008
Revises: 0007
Create Date: 2026-09-26
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("bilties", sa.Column("goods_items", postgresql.JSONB(), nullable=True))
    op.add_column("bilties", sa.Column("consignor_gstin", sa.String(20), nullable=True))
    op.add_column("bilties", sa.Column("consignee_gstin", sa.String(20), nullable=True))
    op.add_column("bilties", sa.Column("consignor_address", sa.Text(), nullable=True))
    op.add_column("bilties", sa.Column("consignee_address", sa.Text(), nullable=True))
    op.add_column("bilties", sa.Column("consignee_mobile", sa.String(20), nullable=True))
    op.add_column("bilties", sa.Column("billing_party", sa.Text(), nullable=True))
    op.add_column("bilties", sa.Column("invoice_no", sa.String(100), nullable=True))
    op.add_column("bilties", sa.Column("invoice_date", sa.Date(), nullable=True))
    op.add_column(
        "bilties",
        sa.Column("un_load_labour", sa.Numeric(12, 2), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    for col in [
        "goods_items", "consignor_gstin", "consignee_gstin",
        "consignor_address", "consignee_address", "consignee_mobile",
        "billing_party", "invoice_no", "invoice_date", "un_load_labour",
    ]:
        op.drop_column("bilties", col)
