import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import bilti as crud
from app.deps import Actor, get_current_actor, get_db
from app.models.bilti import Bilti
from app.models.firm import Firm
from app.models.loading_slip import LoadingSlip
from app.pagination import DEFAULT_LIMIT, Page
from app.schemas.bilti import BiltiCreate, BiltiPrint, BiltiRead, BiltiUpdate

router = APIRouter(prefix="/bilties", tags=["bilties"])


async def _assert_firm_exists(db: AsyncSession, firm_id: uuid.UUID) -> None:
    if await db.get(Firm, firm_id) is None:
        raise HTTPException(status_code=422, detail=f"firm_id {firm_id} does not exist")


async def _assert_loading_slip_exists(db: AsyncSession, slip_id: uuid.UUID) -> None:
    slip = await db.get(LoadingSlip, slip_id)
    if slip is None or slip.is_deleted:
        raise HTTPException(status_code=422, detail=f"loading_slip_id {slip_id} does not exist")


async def _get_or_404(db: AsyncSession, bilti_id: uuid.UUID):
    obj = await crud.get(db, bilti_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bilti not found")
    return obj


@router.get("/next-no")
async def next_bilti_no(firm_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Return the next suggested bilti_no for the given firm (max numeric value + 1)."""
    rows = (
        await db.execute(
            select(Bilti.bilti_no).where(Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False))
        )
    ).scalars().all()
    nums = [int(r) for r in rows if r.strip().isdigit()]
    return {"next_no": str(max(nums) + 1) if nums else "1"}


@router.post("", response_model=BiltiRead, status_code=status.HTTP_201_CREATED)
async def create_bilti(
    data: BiltiCreate,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(get_current_actor),
):
    await _assert_firm_exists(db, data.firm_id)
    if data.loading_slip_id is not None:
        await _assert_loading_slip_exists(db, data.loading_slip_id)
    try:
        return await crud.create(db, data, created_by=actor.id)
    except Exception as exc:  # unique (firm_id, bilti_no) violation, etc.
        if "uq_bilties_firm_id_bilti_no" in str(exc):
            raise HTTPException(
                status_code=409, detail="bilti_no already used for this firm"
            ) from exc
        raise


@router.get("", response_model=Page[BiltiRead])
async def list_bilties(
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
    db: AsyncSession = Depends(get_db),
):
    items, total, page, limit = await crud.list_(
        db, firm_id=firm_id, agent_id=agent_id, truck_owner_id=truck_owner_id,
        vehicle_id=vehicle_id, date_from=date_from, date_to=date_to,
        q=q, vehicle_no=vehicle_no, from_location=from_location,
        to_location=to_location, agent_name=agent_name, factory_name=factory_name,
        sort=sort, page=page, limit=limit,
    )
    return Page(items=items, total=total, page=page, limit=limit)


@router.get("/{bilti_id}", response_model=BiltiRead)
async def get_bilti(bilti_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, bilti_id)


@router.get("/{bilti_id}/print", response_model=BiltiPrint)
async def print_bilti(bilti_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    # freight_difference is intentionally absent from BiltiPrint.
    return await _get_or_404(db, bilti_id)


@router.patch("/{bilti_id}", response_model=BiltiRead)
async def update_bilti(bilti_id: uuid.UUID, data: BiltiUpdate, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, bilti_id)
    if data.firm_id is not None:
        await _assert_firm_exists(db, data.firm_id)
    if data.loading_slip_id is not None:
        await _assert_loading_slip_exists(db, data.loading_slip_id)
    return await crud.update(db, obj, data)


@router.delete("/{bilti_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bilti(bilti_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, bilti_id)
    await crud.soft_delete(db, obj)
