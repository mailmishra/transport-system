import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import agent as agent_crud
from app.crud import truck_owner as truck_owner_crud
from app.crud import vehicle as vehicle_crud
from app.models.loading_slip import LoadingSlip
from app.schemas.loading_slip import LoadingSlipCreate, LoadingSlipUpdate

_NAME_FIELDS = {"vehicle_no", "truck_owner_name", "agent_name"}


async def create(
    db: AsyncSession, data: LoadingSlipCreate, created_by: str | None
) -> LoadingSlip:
    payload = data.model_dump(exclude=_NAME_FIELDS)
    vehicle = await vehicle_crud.get_or_create_by_no(db, data.vehicle_no)
    truck_owner = (
        await truck_owner_crud.get_or_create_by_name(db, data.truck_owner_name)
        if data.truck_owner_name
        else None
    )
    agent = (
        await agent_crud.get_or_create_by_name(db, data.agent_name) if data.agent_name else None
    )
    obj = LoadingSlip(
        **payload,
        vehicle_id=vehicle.id,
        truck_owner_id=truck_owner.id if truck_owner else None,
        agent_id=agent.id if agent else None,
        created_by=created_by,
    )
    db.add(obj)
    await db.commit()
    return await get(db, obj.id)


async def get(db: AsyncSession, slip_id: uuid.UUID) -> LoadingSlip | None:
    # populate_existing: see the matching comment in crud/bilti.py::get().
    stmt = (
        select(LoadingSlip)
        .where(LoadingSlip.id == slip_id, LoadingSlip.is_deleted.is_(False))
        .execution_options(populate_existing=True)
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
    updates = data.model_dump(exclude_unset=True, exclude=_NAME_FIELDS)
    for field, value in updates.items():
        setattr(obj, field, value)
    if data.vehicle_no is not None:
        vehicle = await vehicle_crud.get_or_create_by_no(db, data.vehicle_no)
        obj.vehicle_id = vehicle.id
    if "truck_owner_name" in data.model_fields_set:
        obj.truck_owner_id = (
            (await truck_owner_crud.get_or_create_by_name(db, data.truck_owner_name)).id
            if data.truck_owner_name
            else None
        )
    if "agent_name" in data.model_fields_set:
        obj.agent_id = (
            (await agent_crud.get_or_create_by_name(db, data.agent_name)).id
            if data.agent_name
            else None
        )
    await db.commit()
    return await get(db, obj.id)


async def soft_delete(db: AsyncSession, obj: LoadingSlip) -> None:
    obj.is_deleted = True
    await db.commit()
