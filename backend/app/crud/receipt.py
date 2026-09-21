import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.receipt import Receipt
from app.pagination import DEFAULT_LIMIT, apply_sort, paginate
from app.schemas.receipt import ReceiptCreate

_SORTABLE = {"receipt_date": Receipt.receipt_date, "amount": Receipt.amount}
_DEFAULT_SORT = [Receipt.receipt_date.desc(), Receipt.created_at.desc()]


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
    db: AsyncSession,
    firm_id: uuid.UUID | None = None,
    bilti_id: uuid.UUID | None = None,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
) -> tuple[list[Receipt], int, int, int]:
    stmt = select(Receipt).where(Receipt.is_deleted.is_(False))
    if firm_id is not None:
        stmt = stmt.where(Receipt.firm_id == firm_id)
    if bilti_id is not None:
        stmt = stmt.where(Receipt.bilti_id == bilti_id)
    if q:
        stmt = stmt.where(Receipt.received_from.ilike(f"%{q.strip()}%"))
    stmt = apply_sort(stmt, sort, _SORTABLE, _DEFAULT_SORT)
    return await paginate(db, stmt, page, limit)


async def soft_delete(db: AsyncSession, obj: Receipt) -> None:
    obj.is_deleted = True
    await db.commit()
