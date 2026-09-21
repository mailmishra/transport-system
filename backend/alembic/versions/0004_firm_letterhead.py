"""firms: logo, GSTIN, signatory, jurisdiction text for the PDF letterhead

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-21

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("firms", sa.Column("logo_url", sa.String(500), nullable=True))
    op.add_column("firms", sa.Column("gstin", sa.String(20), nullable=True))
    op.add_column("firms", sa.Column("signatory_name", sa.String(200), nullable=True))
    op.add_column("firms", sa.Column("signatory_designation", sa.String(100), nullable=True))
    op.add_column("firms", sa.Column("jurisdiction_text", sa.String(200), nullable=True))


def downgrade() -> None:
    op.drop_column("firms", "jurisdiction_text")
    op.drop_column("firms", "signatory_designation")
    op.drop_column("firms", "signatory_name")
    op.drop_column("firms", "gstin")
    op.drop_column("firms", "logo_url")
