import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import ActorTrackedMixin, SoftDeleteMixin, TimestampMixin, UUIDPKMixin


class Receipt(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, ActorTrackedMixin, Base):
    __tablename__ = "receipts"

    firm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id"), nullable=False, index=True
    )
    # NOT NULL + RESTRICT: a receipt with no matching Bilti isn't meaningful,
    # and it must never be orphaned by deleting the Bilti it settles.
    bilti_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bilties.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    received_from: Mapped[str] = mapped_column(String(200), nullable=False)
    remarks: Mapped[str | None] = mapped_column(String(300), nullable=True)
