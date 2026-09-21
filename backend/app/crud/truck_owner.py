import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.truck_owner import TruckOwner
from app.pagination import DEFAULT_LIMIT, apply_sort, paginate
from app.schemas.truck_owner import TruckOwnerUpdate

_SORTABLE = {"name": TruckOwner.name}
_DEFAULT_SORT = [TruckOwner.name.asc()]


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


async def list_(
    db: AsyncSession,
    active_only: bool = False,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
) -> tuple[list[TruckOwner], int, int, int]:
    stmt = select(TruckOwner)
    if active_only:
        stmt = stmt.where(TruckOwner.is_active.is_(True))
    if q:
        stmt = stmt.where(TruckOwner.name.ilike(f"%{q.strip()}%"))
    stmt = apply_sort(stmt, sort, _SORTABLE, _DEFAULT_SORT)
    return await paginate(db, stmt, page, limit)


async def update(db: AsyncSession, obj: TruckOwner, data: TruckOwnerUpdate) -> TruckOwner:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj
