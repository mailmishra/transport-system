import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loading_slip import LoadingSlip
from app.schemas.loading_slip import LoadingSlipCreate, LoadingSlipUpdate


async def create(
    db: AsyncSession, data: LoadingSlipCreate, created_by: str | None
) -> LoadingSlip:
    obj = LoadingSlip(**data.model_dump(), created_by=created_by)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get(db: AsyncSession, slip_id: uuid.UUID) -> LoadingSlip | None:
    stmt = select(LoadingSlip).where(
        LoadingSlip.id == slip_id, LoadingSlip.is_deleted.is_(False)
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def list_(
    db: AsyncSession,
    firm_id: uuid.UUID | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[LoadingSlip]:
    stmt = select(LoadingSlip).where(LoadingSlip.is_deleted.is_(False))
    if firm_id is not None:
        stmt = stmt.where(LoadingSlip.firm_id == firm_id)
    if date_from is not None:
        stmt = stmt.where(LoadingSlip.slip_date >= date_from)
    if date_to is not None:
        stmt = stmt.where(LoadingSlip.slip_date <= date_to)
    stmt = stmt.order_by(LoadingSlip.slip_date.desc(), LoadingSlip.created_at.desc())
    return list((await db.execute(stmt)).scalars().all())


async def update(
    db: AsyncSession, obj: LoadingSlip, data: LoadingSlipUpdate
) -> LoadingSlip:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj


async def soft_delete(db: AsyncSession, obj: LoadingSlip) -> None:
    obj.is_deleted = True
    await db.commit()
