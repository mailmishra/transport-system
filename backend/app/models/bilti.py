import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import ActorTrackedMixin, SoftDeleteMixin, TimestampMixin, UUIDPKMixin


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
    vehicle_no: Mapped[str] = mapped_column(String(50), nullable=False)
    truck_owner: Mapped[str] = mapped_column(String(200), nullable=False)
    agent: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    goods_description: Mapped[str] = mapped_column(String(300), nullable=False)
    weight: Mapped[str] = mapped_column(String(100), nullable=False)
    freight: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    dalali: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    advance_to_owner: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    # Hidden field: excluded from BiltiPrint schema / the /print endpoint.
    freight_difference: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
