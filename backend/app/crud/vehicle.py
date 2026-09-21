import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vehicle import Vehicle
from app.pagination import DEFAULT_LIMIT, apply_sort, paginate
from app.schemas.vehicle import VehicleUpdate

_SORTABLE = {"vehicle_no": Vehicle.vehicle_no}
_DEFAULT_SORT = [Vehicle.vehicle_no.asc()]


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


async def list_(
    db: AsyncSession,
    active_only: bool = False,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
) -> tuple[list[Vehicle], int, int, int]:
    stmt = select(Vehicle)
    if active_only:
        stmt = stmt.where(Vehicle.is_active.is_(True))
    if q:
        stmt = stmt.where(Vehicle.vehicle_no.ilike(f"%{q.strip()}%"))
    stmt = apply_sort(stmt, sort, _SORTABLE, _DEFAULT_SORT)
    return await paginate(db, stmt, page, limit)


async def update(db: AsyncSession, obj: Vehicle, data: VehicleUpdate) -> Vehicle:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj
