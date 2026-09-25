import uuid
from datetime import date

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import agent as agent_crud
from app.crud import truck_owner as truck_owner_crud
from app.crud import vehicle as vehicle_crud
from app.models.agent import Agent
from app.models.bilti import Bilti
from app.models.loading_slip import LoadingSlip
from app.models.vehicle import Vehicle
from app.pagination import DEFAULT_LIMIT, apply_sort, paginate
from app.schemas.bilti import BiltiCreate, BiltiUpdate

_SORTABLE = {"bilti_date": Bilti.bilti_date, "bilti_no": Bilti.bilti_no, "freight": Bilti.freight}
_DEFAULT_SORT = [Bilti.bilti_date.desc(), Bilti.created_at.desc()]

_NAME_FIELDS = {"vehicle_no", "palti_vehicle_no", "truck_owner_name", "agent_name"}


async def create(db: AsyncSession, data: BiltiCreate, created_by: str | None) -> Bilti:
    payload = data.model_dump(exclude=_NAME_FIELDS)
    vehicle = await vehicle_crud.get_or_create_by_no(db, data.vehicle_no)
    palti_vehicle = (
        await vehicle_crud.get_or_create_by_no(db, data.palti_vehicle_no)
        if data.palti_vehicle_no
        else None
    )
    truck_owner = await truck_owner_crud.get_or_create_by_name(db, data.truck_owner_name)
    agent = (
        await agent_crud.get_or_create_by_name(db, data.agent_name) if data.agent_name else None
    )
    obj = Bilti(
        **payload,
        vehicle_id=vehicle.id,
        palti_vehicle_id=palti_vehicle.id if palti_vehicle else None,
        truck_owner_id=truck_owner.id,
        agent_id=agent.id if agent else None,
        created_by=created_by,
    )
    db.add(obj)
    await db.commit()
    return await get(db, obj.id)


async def get(db: AsyncSession, bilti_id: uuid.UUID) -> Bilti | None:
    # populate_existing: with expire_on_commit=False (see app/db.py), an
    # object already in the identity map (e.g. the one create()/update()
    # just committed) would otherwise be returned as-is with its pre-commit
    # Python-side values (e.g. Decimal("750") instead of the DB's stored
    # Decimal("750.00")) rather than what Postgres actually persisted.
    stmt = (
        select(Bilti)
        .where(Bilti.id == bilti_id, Bilti.is_deleted.is_(False))
        .execution_options(populate_existing=True)
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def list_(
    db: AsyncSession,
    firm_id: uuid.UUID | None = None,
    agent_id: uuid.UUID | None = None,
    truck_owner_id: uuid.UUID | None = None,
    vehicle_id: uuid.UUID | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    q: str | None = None,
    vehicle_no: str | None = None,
    from_location: str | None = None,
    to_location: str | None = None,
    agent_name: str | None = None,
    factory_name: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
) -> tuple[list[Bilti], int, int, int]:
    stmt = select(Bilti).where(Bilti.is_deleted.is_(False))
    if firm_id is not None:
        stmt = stmt.where(Bilti.firm_id == firm_id)
    if agent_id is not None:
        stmt = stmt.where(Bilti.agent_id == agent_id)
    if truck_owner_id is not None:
        stmt = stmt.where(Bilti.truck_owner_id == truck_owner_id)
    if vehicle_id is not None:
        stmt = stmt.where(Bilti.vehicle_id == vehicle_id)
    if date_from is not None:
        stmt = stmt.where(Bilti.bilti_date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Bilti.bilti_date <= date_to)
    # q: free-text across bilti_no, consignor, consignee, vehicle_no
    if q:
        needle = f"%{q.strip()}%"
        stmt = stmt.join(Vehicle, Bilti.vehicle_id == Vehicle.id).where(
            or_(
                Bilti.bilti_no.ilike(needle),
                Bilti.consignor.ilike(needle),
                Bilti.consignee.ilike(needle),
                Vehicle.vehicle_no.ilike(needle),
            )
        )
    # dedicated report filters -- applied independently of q
    if vehicle_no:
        if q:
            # Vehicle already joined above; reuse it
            stmt = stmt.where(Vehicle.vehicle_no.ilike(f"%{vehicle_no.strip()}%"))
        else:
            stmt = stmt.join(Vehicle, Bilti.vehicle_id == Vehicle.id).where(
                Vehicle.vehicle_no.ilike(f"%{vehicle_no.strip()}%")
            )
    if from_location:
        stmt = stmt.where(Bilti.from_location.ilike(f"%{from_location.strip()}%"))
    if to_location:
        stmt = stmt.where(Bilti.to_location.ilike(f"%{to_location.strip()}%"))
    if agent_name:
        stmt = stmt.join(Agent, Bilti.agent_id == Agent.id).where(
            Agent.name.ilike(f"%{agent_name.strip()}%")
        )
    if factory_name:
        stmt = stmt.join(LoadingSlip, Bilti.loading_slip_id == LoadingSlip.id).where(
            LoadingSlip.factory_name.ilike(f"%{factory_name.strip()}%")
        )
    stmt = apply_sort(stmt, sort, _SORTABLE, _DEFAULT_SORT)
    return await paginate(db, stmt, page, limit)


async def update(db: AsyncSession, obj: Bilti, data: BiltiUpdate) -> Bilti:
    updates = data.model_dump(exclude_unset=True, exclude=_NAME_FIELDS)
    for field, value in updates.items():
        setattr(obj, field, value)
    if data.vehicle_no is not None:
        vehicle = await vehicle_crud.get_or_create_by_no(db, data.vehicle_no)
        obj.vehicle_id = vehicle.id
    if "palti_vehicle_no" in data.model_fields_set:
        obj.palti_vehicle_id = (
            (await vehicle_crud.get_or_create_by_no(db, data.palti_vehicle_no)).id
            if data.palti_vehicle_no
            else None
        )
    if data.truck_owner_name is not None:
        truck_owner = await truck_owner_crud.get_or_create_by_name(db, data.truck_owner_name)
        obj.truck_owner_id = truck_owner.id
    if "agent_name" in data.model_fields_set:
        obj.agent_id = (
            (await agent_crud.get_or_create_by_name(db, data.agent_name)).id
            if data.agent_name
            else None
        )
    await db.commit()
    return await get(db, obj.id)


async def soft_delete(db: AsyncSession, obj: Bilti) -> None:
    obj.is_deleted = True
    await db.commit()
