import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.agent import Agent
from app.models.base import ActorTrackedMixin, SoftDeleteMixin, TimestampMixin, UUIDPKMixin
from app.models.truck_owner import TruckOwner
from app.models.vehicle import Vehicle


class LoadingSlip(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, ActorTrackedMixin, Base):
    __tablename__ = "loading_slips"

    firm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id"), nullable=False, index=True
    )
    slip_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    # Normalized so the same value typed on Bilti/GR reuses the same row
    # instead of drifting into near-duplicate free text (see agent.py /
    # truck_owner.py for the same pattern).
    vehicle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # The paper slip is addressed to a specific truck owner ("M/s ...") and
    # arranged through a broker ("बोकर") -- both optional since a Loading
    # Slip can be raised before either is finalized.
    truck_owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("truck_owners.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    loading_point: Mapped[str] = mapped_column(String(200), nullable=False)
    destination: Mapped[str] = mapped_column(String(200), nullable=False)
    goods_description: Mapped[str] = mapped_column(String(300), nullable=False)
    quantity_weight: Mapped[str] = mapped_column(String(100), nullable=False)
    # "कट्टी" -- bag/package count noted on the paper slip.
    package_count: Mapped[str | None] = mapped_column(String(50), nullable=True)
    advance_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    # Free text: the paper slip has four blank itemized advance lines whose
    # meaning varies shipment to shipment -- a note captures that faithfully
    # without forcing an arbitrary rigid structure.
    advance_note: Mapped[str | None] = mapped_column(String(500), nullable=True)

    vehicle: Mapped[Vehicle] = relationship(lazy="joined")
    truck_owner: Mapped[TruckOwner | None] = relationship(lazy="joined")
    agent: Mapped[Agent | None] = relationship(lazy="joined")
