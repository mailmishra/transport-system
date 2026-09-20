import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.truck_owner import TruckOwner
from app.schemas.truck_owner import TruckOwnerUpdate


async def get_or_create_by_name(db: AsyncSession, name: str) -> TruckOwner:
    name = name.strip()
    stmt = select(TruckOwner).where(func.lower(TruckOwner.name) == name.lower())
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing is not None:
        return existing
    obj = TruckOwner(name=name)
    db.add(obj)
    await db.flush()
    return obj


async def get(db: AsyncSession, truck_owner_id: uuid.UUID) -> TruckOwner | None:
    return await db.get(TruckOwner, truck_owner_id)


async def list_(db: AsyncSession, active_only: bool = False) -> list[TruckOwner]:
    stmt = select(TruckOwner).order_by(TruckOwner.name)
    if active_only:
        stmt = stmt.where(TruckOwner.is_active.is_(True))
    return list((await db.execute(stmt)).scalars().all())


async def update(db: AsyncSession, obj: TruckOwner, data: TruckOwnerUpdate) -> TruckOwner:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj
