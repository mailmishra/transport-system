from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import TimestampMixin, UUIDPKMixin


class Firm(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "firms"

    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String(300), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    pan_no: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bank_account_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    bank_branch: Mapped[str | None] = mapped_column(String(200), nullable=True)
    bank_ifsc: Mapped[str | None] = mapped_column(String(20), nullable=True)
