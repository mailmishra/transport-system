import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bilti import Bilti
from app.schemas.bilti import BiltiCreate, BiltiUpdate


async def create(db: AsyncSession, data: BiltiCreate, created_by: str | None) -> Bilti:
    obj = Bilti(**data.model_dump(), created_by=created_by)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get(db: AsyncSession, bilti_id: uuid.UUID) -> Bilti | None:
    stmt = select(Bilti).where(Bilti.id == bilti_id, Bilti.is_deleted.is_(False))
    return (await db.execute(stmt)).scalar_one_or_none()


async def list_(
    db: AsyncSession,
    firm_id: uuid.UUID | None = None,
    agent: str | None = None,
) -> list[Bilti]:
    stmt = select(Bilti).where(Bilti.is_deleted.is_(False))
    if firm_id is not None:
        stmt = stmt.where(Bilti.firm_id == firm_id)
    if agent is not None:
        stmt = stmt.where(Bilti.agent == agent)
    stmt = stmt.order_by(Bilti.bilti_date.desc(), Bilti.created_at.desc())
    return list((await db.execute(stmt)).scalars().all())


async def update(db: AsyncSession, obj: Bilti, data: BiltiUpdate) -> Bilti:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj


async def soft_delete(db: AsyncSession, obj: Bilti) -> None:
    obj.is_deleted = True
    await db.commit()
