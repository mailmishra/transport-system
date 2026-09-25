import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.agent import Agent
from app.models.base import ActorTrackedMixin, SoftDeleteMixin, TimestampMixin, UUIDPKMixin
from app.models.truck_owner import TruckOwner
from app.models.vehicle import Vehicle


class Bilti(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, ActorTrackedMixin, Base):
    __tablename__ = "bilties"
    __table_args__ = (UniqueConstraint("firm_id", "bilti_no", name="uq_bilties_firm_id_bilti_no"),)

    firm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id"), nullable=False, index=True
    )
    loading_slip_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("loading_slips.id"), nullable=True
    )
    bilti_no: Mapped[str] = mapped_column(String(50), nullable=False)
    bilti_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    consignor: Mapped[str] = mapped_column(String(200), nullable=False)
    consignee: Mapped[str] = mapped_column(String(200), nullable=False)
    from_location: Mapped[str] = mapped_column(String(200), nullable=False)
    to_location: Mapped[str] = mapped_column(String(200), nullable=False)
    # Normalized so the ledgers can aggregate by identity instead of free text
    # (see backend/app/models/agent.py, truck_owner.py, vehicle.py).
    # RESTRICT: an agent/owner/vehicle with ledger history must never be
    # deletable out from under it -- deactivate (is_active=false) instead.
    vehicle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # "Palti Truck No." -- an alternate/transship vehicle noted on some GRs.
    palti_vehicle_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=True
    )
    truck_owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("truck_owners.id", ondelete="RESTRICT"), nullable=False
    )
    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    goods_description: Mapped[str] = mapped_column(String(300), nullable=False)
    # Actual weight as loaded; charged_weight is what freight is billed on
    # (may differ after rounding/minimum-weight rules) -- both appear
    # separately on the real GR form.
    weight: Mapped[str] = mapped_column(String(100), nullable=False)
    weight_per_bag: Mapped[Decimal | None] = mapped_column(Numeric(12, 3), nullable=True)
    charged_weight: Mapped[str | None] = mapped_column(String(100), nullable=True)
    package_count: Mapped[str | None] = mapped_column(String(50), nullable=True)
    package_unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    freight: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    # Per-unit rate shown on the form alongside the total freight amount.
    freight_rate: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    dalali: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    advance_to_owner: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    # Hidden field: excluded from BiltiPrint schema / the /print endpoint.
    freight_difference: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    # Charge breakdown from the rate table on the real GR form.
    other_charges: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    kanta_charges: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    bahi_charges: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    service_tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    hamali: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    p_freight: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    # Validated at the app layer (see schemas/bilti.py) against
    # consignor/consignee/transporter/exempted rather than a DB CHECK, so a
    # future allowed value doesn't need a migration.
    gst_paid_by: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eway_bill_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    invoice_value: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    # Insurance block from the real GR form.
    insured: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    insurance_company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    insurance_policy_no: Mapped[str | None] = mapped_column(String(100), nullable=True)
    insurance_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    insurance_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    insurance_risk: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # Separate from agent_id/the Agent-Dalal ledger on purpose -- this is
    # the insurance company's agent, an unrelated party.
    insurance_agent_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # "Value Rs." near Truck Owner Name -- declared value at owner's risk.
    goods_value_declared: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    remark: Mapped[str | None] = mapped_column(String(500), nullable=True)

    vehicle: Mapped[Vehicle] = relationship(lazy="joined", foreign_keys=[vehicle_id])
    palti_vehicle: Mapped[Vehicle | None] = relationship(
        lazy="joined", foreign_keys=[palti_vehicle_id]
    )
    truck_owner: Mapped[TruckOwner] = relationship(lazy="joined")
    agent: Mapped[Agent | None] = relationship(lazy="joined")
