"""init schema: firms, loading_slips, bilties

Revision ID: 0001
Revises:
Create Date: 2026-09-20

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

FIRMS = [
    "Sri Krishna Transport Company",
    "Shivsakti Transport Company",
    "Shivam Transport Company",
]


def upgrade() -> None:
    op.create_table(
        "firms",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("name", name="uq_firms_name"),
    )

    op.create_table(
        "loading_slips",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("firm_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slip_date", sa.Date, nullable=False),
        sa.Column("vehicle_no", sa.String(50), nullable=False),
        sa.Column("loading_point", sa.String(200), nullable=False),
        sa.Column("destination", sa.String(200), nullable=False),
        sa.Column("goods_description", sa.String(300), nullable=False),
        sa.Column("quantity_weight", sa.String(100), nullable=False),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["firm_id"], ["firms.id"], name="fk_loading_slips_firm_id_firms"
        ),
    )
    op.create_index("ix_loading_slips_firm_id", "loading_slips", ["firm_id"])
    op.create_index("ix_loading_slips_slip_date", "loading_slips", ["slip_date"])

    op.create_table(
        "bilties",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("firm_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("loading_slip_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("bilti_no", sa.String(50), nullable=False),
        sa.Column("bilti_date", sa.Date, nullable=False),
        sa.Column("consignor", sa.String(200), nullable=False),
        sa.Column("consignee", sa.String(200), nullable=False),
        sa.Column("from_location", sa.String(200), nullable=False),
        sa.Column("to_location", sa.String(200), nullable=False),
        sa.Column("vehicle_no", sa.String(50), nullable=False),
        sa.Column("truck_owner", sa.String(200), nullable=False),
        sa.Column("agent", sa.String(200), nullable=True),
        sa.Column("goods_description", sa.String(300), nullable=False),
        sa.Column("weight", sa.String(100), nullable=False),
        sa.Column("freight", sa.Numeric(12, 2), nullable=False),
        sa.Column("dalali", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column(
            "advance_to_owner", sa.Numeric(12, 2), nullable=False, server_default="0"
        ),
        sa.Column(
            "freight_difference", sa.Numeric(12, 2), nullable=False, server_default="0"
        ),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["firm_id"], ["firms.id"], name="fk_bilties_firm_id_firms"
        ),
        sa.ForeignKeyConstraint(
            ["loading_slip_id"],
            ["loading_slips.id"],
            name="fk_bilties_loading_slip_id_loading_slips",
        ),
        sa.UniqueConstraint(
            "firm_id", "bilti_no", name="uq_bilties_firm_id_bilti_no"
        ),
    )
    op.create_index("ix_bilties_firm_id", "bilties", ["firm_id"])
    op.create_index("ix_bilties_bilti_date", "bilties", ["bilti_date"])
    op.create_index("ix_bilties_agent", "bilties", ["agent"])

    firms_table = sa.table("firms", sa.column("id", postgresql.UUID), sa.column("name", sa.String))
    op.bulk_insert(firms_table, [{"id": uuid.uuid4(), "name": name} for name in FIRMS])


def downgrade() -> None:
    op.drop_table("bilties")
    op.drop_table("loading_slips")
    op.drop_table("firms")
