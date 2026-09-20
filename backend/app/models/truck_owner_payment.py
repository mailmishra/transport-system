import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.base import ActorTrackedMixin, SoftDeleteMixin, TimestampMixin, UUIDPKMixin
from app.models.truck_owner import TruckOwner


class TruckOwnerPayment(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, ActorTrackedMixin, Base):
    __tablename__ = "truck_owner_payments"

    firm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id"), nullable=False, index=True
    )
    truck_owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("truck_owners.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    # Nullable: a payment can be a lump sum settlement not tied to one Bilti.
    bilti_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bilties.id"), nullable=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    mode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(300), nullable=True)

    truck_owner: Mapped[TruckOwner] = relationship(lazy="joined")
