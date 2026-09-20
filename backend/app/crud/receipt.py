import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate


async def create(db: AsyncSession, data: ReceiptCreate, created_by: str | None) -> Receipt:
    obj = Receipt(**data.model_dump(), created_by=created_by)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get(db: AsyncSession, receipt_id: uuid.UUID) -> Receipt | None:
    stmt = select(Receipt).where(Receipt.id == receipt_id, Receipt.is_deleted.is_(False))
    return (await db.execute(stmt)).scalar_one_or_none()


async def list_(
    db: AsyncSession, firm_id: uuid.UUID | None = None, bilti_id: uuid.UUID | None = None
) -> list[Receipt]:
    stmt = select(Receipt).where(Receipt.is_deleted.is_(False))
    if firm_id is not None:
        stmt = stmt.where(Receipt.firm_id == firm_id)
    if bilti_id is not None:
        stmt = stmt.where(Receipt.bilti_id == bilti_id)
    stmt = stmt.order_by(Receipt.receipt_date.desc(), Receipt.created_at.desc())
    return list((await db.execute(stmt)).scalars().all())


async def soft_delete(db: AsyncSession, obj: Receipt) -> None:
    obj.is_deleted = True
    await db.commit()
