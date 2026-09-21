import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleUpdate


async def get_or_create_by_no(db: AsyncSession, vehicle_no: str) -> Vehicle:
    vehicle_no = vehicle_no.strip()
    stmt = select(Vehicle).where(func.lower(Vehicle.vehicle_no) == vehicle_no.lower())
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing is not None:
        return existing
    obj = Vehicle(vehicle_no=vehicle_no)
    db.add(obj)
    await db.flush()
    return obj


async def get(db: AsyncSession, vehicle_id: uuid.UUID) -> Vehicle | None:
    return await db.get(Vehicle, vehicle_id)


async def list_(db: AsyncSession, active_only: bool = False) -> list[Vehicle]:
    stmt = select(Vehicle).order_by(Vehicle.vehicle_no)
    if active_only:
        stmt = stmt.where(Vehicle.is_active.is_(True))
    return list((await db.execute(stmt)).scalars().all())


async def update(db: AsyncSession, obj: Vehicle, data: VehicleUpdate) -> Vehicle:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj
