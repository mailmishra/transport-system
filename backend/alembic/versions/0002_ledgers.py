"""normalize agent/truck_owner, add payments + receipts, add money CHECKs

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- master tables -----------------------------------------------
    op.create_table(
        "agents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "truck_owners",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # --- bilties: add FK columns, backfill from free text, drop text ---
    op.add_column("bilties", sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("bilties", sa.Column("truck_owner_id", postgresql.UUID(as_uuid=True), nullable=True))

    op.execute(
        """
        INSERT INTO agents (id, name)
        SELECT gen_random_uuid(), t.name FROM (
            SELECT DISTINCT trim(agent) AS name FROM bilties
            WHERE agent IS NOT NULL AND trim(agent) <> ''
        ) t
        """
    )
    op.execute(
        """
        UPDATE bilties SET agent_id = agents.id
        FROM agents WHERE agents.name = trim(bilties.agent) AND bilties.agent IS NOT NULL
        """
    )
    op.execute(
        """
        INSERT INTO truck_owners (id, name)
        SELECT gen_random_uuid(), t.name FROM (
            SELECT DISTINCT trim(truck_owner) AS name FROM bilties
            WHERE truck_owner IS NOT NULL AND trim(truck_owner) <> ''
        ) t
        """
    )
    op.execute(
        """
        UPDATE bilties SET truck_owner_id = truck_owners.id
        FROM truck_owners WHERE truck_owners.name = trim(bilties.truck_owner)
        """
    )

    op.drop_index("ix_bilties_agent", table_name="bilties")
    op.drop_column("bilties", "agent")
    op.drop_column("bilties", "truck_owner")

    op.alter_column("bilties", "truck_owner_id", nullable=False)
    op.create_foreign_key(
        "fk_bilties_agent_id_agents", "bilties", "agents", ["agent_id"], ["id"], ondelete="RESTRICT"
    )
    op.create_foreign_key(
        "fk_bilties_truck_owner_id_truck_owners",
        "bilties",
        "truck_owners",
        ["truck_owner_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_index("ix_bilties_agent_id", "bilties", ["agent_id"])
    op.create_index("ix_bilties_truck_owner_id", "bilties", ["truck_owner_id"])

    # --- money invariants, enforced at the schema level too ------------
    op.create_check_constraint("ck_bilties_freight_positive", "bilties", "freight > 0")
    op.create_check_constraint("ck_bilties_dalali_non_negative", "bilties", "dalali >= 0")
    op.create_check_constraint(
        "ck_bilties_advance_to_owner_non_negative", "bilties", "advance_to_owner >= 0"
    )
    op.create_check_constraint(
        "ck_bilties_freight_difference_non_negative", "bilties", "freight_difference >= 0"
    )

    # --- agent_payments --------------------------------------------------
    op.create_table(
        "agent_payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("firm_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("payment_date", sa.Date, nullable=False),
        sa.Column("mode", sa.String(50), nullable=True),
        sa.Column("remarks", sa.String(300), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["firm_id"], ["firms.id"], name="fk_agent_payments_firm_id_firms"),
        sa.ForeignKeyConstraint(
            ["agent_id"], ["agents.id"], name="fk_agent_payments_agent_id_agents", ondelete="RESTRICT"
        ),
        sa.CheckConstraint("amount > 0", name="ck_agent_payments_amount_positive"),
    )
    op.create_index("ix_agent_payments_firm_id", "agent_payments", ["firm_id"])
    op.create_index("ix_agent_payments_agent_id", "agent_payments", ["agent_id"])
    op.create_index("ix_agent_payments_payment_date", "agent_payments", ["payment_date"])

    # --- truck_owner_payments --------------------------------------------
    op.create_table(
        "truck_owner_payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("firm_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("truck_owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bilti_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("payment_date", sa.Date, nullable=False),
        sa.Column("mode", sa.String(50), nullable=True),
        sa.Column("remarks", sa.String(300), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["firm_id"], ["firms.id"], name="fk_truck_owner_payments_firm_id_firms"),
        sa.ForeignKeyConstraint(
            ["truck_owner_id"],
            ["truck_owners.id"],
            name="fk_truck_owner_payments_truck_owner_id_truck_owners",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["bilti_id"], ["bilties.id"], name="fk_truck_owner_payments_bilti_id_bilties"
        ),
        sa.CheckConstraint("amount > 0", name="ck_truck_owner_payments_amount_positive"),
    )
    op.create_index("ix_truck_owner_payments_firm_id", "truck_owner_payments", ["firm_id"])
    op.create_index("ix_truck_owner_payments_truck_owner_id", "truck_owner_payments", ["truck_owner_id"])
    op.create_index("ix_truck_owner_payments_payment_date", "truck_owner_payments", ["payment_date"])

    # --- receipts ----------------------------------------------------------
    op.create_table(
        "receipts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("firm_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bilti_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("receipt_date", sa.Date, nullable=False),
        sa.Column("received_from", sa.String(200), nullable=False),
        sa.Column("remarks", sa.String(300), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["firm_id"], ["firms.id"], name="fk_receipts_firm_id_firms"),
        sa.ForeignKeyConstraint(
            ["bilti_id"], ["bilties.id"], name="fk_receipts_bilti_id_bilties", ondelete="RESTRICT"
        ),
        sa.CheckConstraint("amount > 0", name="ck_receipts_amount_positive"),
    )
    op.create_index("ix_receipts_firm_id", "receipts", ["firm_id"])
    op.create_index("ix_receipts_bilti_id", "receipts", ["bilti_id"])
    op.create_index("ix_receipts_receipt_date", "receipts", ["receipt_date"])


def downgrade() -> None:
    op.drop_table("receipts")
    op.drop_table("truck_owner_payments")
    op.drop_table("agent_payments")

    op.drop_constraint("ck_bilties_freight_difference_non_negative", "bilties", type_="check")
    op.drop_constraint("ck_bilties_advance_to_owner_non_negative", "bilties", type_="check")
    op.drop_constraint("ck_bilties_dalali_non_negative", "bilties", type_="check")
    op.drop_constraint("ck_bilties_freight_positive", "bilties", type_="check")

    op.add_column("bilties", sa.Column("agent", sa.String(200), nullable=True))
    op.add_column("bilties", sa.Column("truck_owner", sa.String(200), nullable=True))
    op.execute(
        "UPDATE bilties SET agent = agents.name FROM agents WHERE agents.id = bilties.agent_id"
    )
    op.execute(
        "UPDATE bilties SET truck_owner = truck_owners.name "
        "FROM truck_owners WHERE truck_owners.id = bilties.truck_owner_id"
    )
    op.alter_column("bilties", "truck_owner", nullable=False)
    op.create_index("ix_bilties_agent", "bilties", ["agent"])

    op.drop_index("ix_bilties_truck_owner_id", table_name="bilties")
    op.drop_index("ix_bilties_agent_id", table_name="bilties")
    op.drop_constraint("fk_bilties_truck_owner_id_truck_owners", "bilties", type_="foreignkey")
    op.drop_constraint("fk_bilties_agent_id_agents", "bilties", type_="foreignkey")
    op.drop_column("bilties", "truck_owner_id")
    op.drop_column("bilties", "agent_id")

    op.drop_table("truck_owners")
    op.drop_table("agents")
