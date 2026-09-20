from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import TimestampMixin, UUIDPKMixin


class Firm(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "firms"

    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
