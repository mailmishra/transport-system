import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import ActorTrackedMixin, SoftDeleteMixin, TimestampMixin, UUIDPKMixin


class LoadingSlip(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, ActorTrackedMixin, Base):
    __tablename__ = "loading_slips"

    firm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("firms.id"), nullable=False, index=True
    )
    slip_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    vehicle_no: Mapped[str] = mapped_column(String(50), nullable=False)
    loading_point: Mapped[str] = mapped_column(String(200), nullable=False)
    destination: Mapped[str] = mapped_column(String(200), nullable=False)
    goods_description: Mapped[str] = mapped_column(String(300), nullable=False)
    quantity_weight: Mapped[str] = mapped_column(String(100), nullable=False)
