import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPKMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    # Accounting records are never hard-deleted; DELETE endpoints flip this.
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ActorTrackedMixin:
    # Nullable until Supabase auth lands (see app/deps.py Actor).
    created_by: Mapped[str | None] = mapped_column(nullable=True)
