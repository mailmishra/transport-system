"""normalize vehicles; capture full paper Loading Slip / Bilti-GR fields

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-21

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- vehicles master table, mirroring agents/truck_owners ------------
    op.create_table(
        "vehicles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vehicle_no", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # --- backfill vehicles from distinct free-text vehicle_no values -----
    op.execute(
        """
        INSERT INTO vehicles (id, vehicle_no)
        SELECT gen_random_uuid(), t.vehicle_no FROM (
            SELECT DISTINCT trim(vehicle_no) AS vehicle_no FROM loading_slips
            WHERE vehicle_no IS NOT NULL AND trim(vehicle_no) <> ''
            UNION
            SELECT DISTINCT trim(vehicle_no) AS vehicle_no FROM bilties
            WHERE vehicle_no IS NOT NULL AND trim(vehicle_no) <> ''
        ) t
        """
    )

    # --- loading_slips: vehicle_no -> vehicle_id -------------------------
    op.add_column("loading_slips", sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.execute(
        """
        UPDATE loading_slips SET vehicle_id = vehicles.id
        FROM vehicles WHERE lower(vehicles.vehicle_no) = lower(trim(loading_slips.vehicle_no))
        """
    )
    op.drop_column("loading_slips", "vehicle_no")
    op.alter_column("loading_slips", "vehicle_id", nullable=False)
    op.create_foreign_key(
        "fk_loading_slips_vehicle_id_vehicles",
        "loading_slips",
        "vehicles",
        ["vehicle_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_index("ix_loading_slips_vehicle_id", "loading_slips", ["vehicle_id"])

    # --- bilties: vehicle_no -> vehicle_id, plus palti_vehicle_id --------
    op.add_column("bilties", sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.execute(
        """
        UPDATE bilties SET vehicle_id = vehicles.id
        FROM vehicles WHERE lower(vehicles.vehicle_no) = lower(trim(bilties.vehicle_no))
        """
    )
    op.drop_column("bilties", "vehicle_no")
    op.alter_column("bilties", "vehicle_id", nullable=False)
    op.create_foreign_key(
        "fk_bilties_vehicle_id_vehicles", "bilties", "vehicles", ["vehicle_id"], ["id"], ondelete="RESTRICT"
    )
    op.create_index("ix_bilties_vehicle_id", "bilties", ["vehicle_id"])

    op.add_column("bilties", sa.Column("palti_vehicle_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_bilties_palti_vehicle_id_vehicles",
        "bilties",
        "vehicles",
        ["palti_vehicle_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # --- loading_slips: broker/addressee + package/advance fields --------
    op.add_column("loading_slips", sa.Column("truck_owner_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("loading_slips", sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_loading_slips_truck_owner_id_truck_owners",
        "loading_slips",
        "truck_owners",
        ["truck_owner_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_loading_slips_agent_id_agents",
        "loading_slips",
        "agents",
        ["agent_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_index("ix_loading_slips_truck_owner_id", "loading_slips", ["truck_owner_id"])
    op.create_index("ix_loading_slips_agent_id", "loading_slips", ["agent_id"])
    op.add_column("loading_slips", sa.Column("package_count", sa.String(50), nullable=True))
    op.add_column(
        "loading_slips", sa.Column("advance_amount", sa.Numeric(12, 2), nullable=False, server_default="0")
    )
    op.add_column("loading_slips", sa.Column("advance_note", sa.String(500), nullable=True))
    op.create_check_constraint(
        "ck_loading_slips_advance_amount_non_negative", "loading_slips", "advance_amount >= 0"
    )

    # --- bilties: charge breakdown, GST/E-Way/Invoice, insurance, misc ---
    op.add_column("bilties", sa.Column("charged_weight", sa.String(100), nullable=True))
    op.add_column("bilties", sa.Column("package_count", sa.String(50), nullable=True))
    op.add_column("bilties", sa.Column("package_unit", sa.String(50), nullable=True))
    op.add_column("bilties", sa.Column("freight_rate", sa.Numeric(12, 2), nullable=True))
    op.add_column("bilties", sa.Column("other_charges", sa.Numeric(12, 2), nullable=False, server_default="0"))
    op.add_column("bilties", sa.Column("kanta_charges", sa.Numeric(12, 2), nullable=False, server_default="0"))
    op.add_column("bilties", sa.Column("bahi_charges", sa.Numeric(12, 2), nullable=False, server_default="0"))
    op.add_column("bilties", sa.Column("service_tax", sa.Numeric(12, 2), nullable=False, server_default="0"))
    op.add_column("bilties", sa.Column("hamali", sa.Numeric(12, 2), nullable=False, server_default="0"))
    op.add_column("bilties", sa.Column("p_freight", sa.Numeric(12, 2), nullable=False, server_default="0"))
    op.add_column("bilties", sa.Column("gst_paid_by", sa.String(20), nullable=True))
    op.add_column("bilties", sa.Column("eway_bill_no", sa.String(50), nullable=True))
    op.add_column("bilties", sa.Column("invoice_value", sa.Numeric(12, 2), nullable=True))
    op.add_column("bilties", sa.Column("insured", sa.Boolean, nullable=True))
    op.add_column("bilties", sa.Column("insurance_company", sa.String(200), nullable=True))
    op.add_column("bilties", sa.Column("insurance_policy_no", sa.String(100), nullable=True))
    op.add_column("bilties", sa.Column("insurance_amount", sa.Numeric(12, 2), nullable=True))
    op.add_column("bilties", sa.Column("insurance_date", sa.Date, nullable=True))
    op.add_column("bilties", sa.Column("insurance_risk", sa.String(200), nullable=True))
    op.add_column("bilties", sa.Column("insurance_agent_name", sa.String(200), nullable=True))
    op.add_column("bilties", sa.Column("goods_value_declared", sa.Numeric(12, 2), nullable=True))
    op.add_column("bilties", sa.Column("remark", sa.String(500), nullable=True))

    for name, expr in [
        ("freight_rate", "freight_rate >= 0"),
        ("other_charges", "other_charges >= 0"),
        ("kanta_charges", "kanta_charges >= 0"),
        ("bahi_charges", "bahi_charges >= 0"),
        ("service_tax", "service_tax >= 0"),
        ("hamali", "hamali >= 0"),
        ("p_freight", "p_freight >= 0"),
        ("invoice_value", "invoice_value >= 0"),
        ("insurance_amount", "insurance_amount >= 0"),
        ("goods_value_declared", "goods_value_declared >= 0"),
    ]:
        op.create_check_constraint(f"ck_bilties_{name}_non_negative", "bilties", expr)

    # --- firms: letterhead / bank details for the printed GR -------------
    op.add_column("firms", sa.Column("address", sa.String(300), nullable=True))
    op.add_column("firms", sa.Column("phone", sa.String(30), nullable=True))
    op.add_column("firms", sa.Column("email", sa.String(200), nullable=True))
    op.add_column("firms", sa.Column("pan_no", sa.String(20), nullable=True))
    op.add_column("firms", sa.Column("bank_account_no", sa.String(50), nullable=True))
    op.add_column("firms", sa.Column("bank_name", sa.String(200), nullable=True))
    op.add_column("firms", sa.Column("bank_branch", sa.String(200), nullable=True))
    op.add_column("firms", sa.Column("bank_ifsc", sa.String(20), nullable=True))

    # Real values from the firm's own printed Bilti/GR pad.
    op.execute(
        """
        UPDATE firms SET
            address = 'Mirzapur Road, Near Kuthla Thana, PURAINI, KATNI (M.P.)',
            phone = '9685745454',
            email = 'shrikrishnatransportco@gmail.com',
            pan_no = 'AGWPM1764F',
            bank_account_no = '3646 1660 068',
            bank_name = 'SBI Lamtara',
            bank_branch = 'SBI Lamtara (18766)',
            bank_ifsc = 'SBIN0018766'
        WHERE name = 'Sri Krishna Transport Company'
        """
    )


def downgrade() -> None:
    for col in (
        "bank_ifsc",
        "bank_branch",
        "bank_name",
        "bank_account_no",
        "pan_no",
        "email",
        "phone",
        "address",
    ):
        op.drop_column("firms", col)

    for name in (
        "goods_value_declared",
        "insurance_amount",
        "invoice_value",
        "p_freight",
        "hamali",
        "service_tax",
        "bahi_charges",
        "kanta_charges",
        "other_charges",
        "freight_rate",
    ):
        op.drop_constraint(f"ck_bilties_{name}_non_negative", "bilties", type_="check")

    for col in (
        "remark",
        "goods_value_declared",
        "insurance_agent_name",
        "insurance_risk",
        "insurance_date",
        "insurance_amount",
        "insurance_policy_no",
        "insurance_company",
        "insured",
        "invoice_value",
        "eway_bill_no",
        "gst_paid_by",
        "p_freight",
        "hamali",
        "service_tax",
        "bahi_charges",
        "kanta_charges",
        "other_charges",
        "freight_rate",
        "package_unit",
        "package_count",
        "charged_weight",
    ):
        op.drop_column("bilties", col)

    op.drop_constraint("ck_loading_slips_advance_amount_non_negative", "loading_slips", type_="check")
    op.drop_column("loading_slips", "advance_note")
    op.drop_column("loading_slips", "advance_amount")
    op.drop_column("loading_slips", "package_count")
    op.drop_index("ix_loading_slips_agent_id", table_name="loading_slips")
    op.drop_index("ix_loading_slips_truck_owner_id", table_name="loading_slips")
    op.drop_constraint("fk_loading_slips_agent_id_agents", "loading_slips", type_="foreignkey")
    op.drop_constraint(
        "fk_loading_slips_truck_owner_id_truck_owners", "loading_slips", type_="foreignkey"
    )
    op.drop_column("loading_slips", "agent_id")
    op.drop_column("loading_slips", "truck_owner_id")

    op.drop_constraint("fk_bilties_palti_vehicle_id_vehicles", "bilties", type_="foreignkey")
    op.drop_column("bilties", "palti_vehicle_id")

    op.add_column("bilties", sa.Column("vehicle_no", sa.String(50), nullable=True))
    op.execute(
        "UPDATE bilties SET vehicle_no = vehicles.vehicle_no FROM vehicles WHERE vehicles.id = bilties.vehicle_id"
    )
    op.alter_column("bilties", "vehicle_no", nullable=False)
    op.drop_index("ix_bilties_vehicle_id", table_name="bilties")
    op.drop_constraint("fk_bilties_vehicle_id_vehicles", "bilties", type_="foreignkey")
    op.drop_column("bilties", "vehicle_id")

    op.add_column("loading_slips", sa.Column("vehicle_no", sa.String(50), nullable=True))
    op.execute(
        "UPDATE loading_slips SET vehicle_no = vehicles.vehicle_no "
        "FROM vehicles WHERE vehicles.id = loading_slips.vehicle_id"
    )
    op.alter_column("loading_slips", "vehicle_no", nullable=False)
    op.drop_index("ix_loading_slips_vehicle_id", table_name="loading_slips")
    op.drop_constraint("fk_loading_slips_vehicle_id_vehicles", "loading_slips", type_="foreignkey")
    op.drop_column("loading_slips", "vehicle_id")

    op.drop_table("vehicles")
