import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import loading_slip as crud
from app.deps import Actor, get_current_actor, get_db
from app.models.firm import Firm
from app.schemas.loading_slip import LoadingSlipCreate, LoadingSlipRead, LoadingSlipUpdate

router = APIRouter(prefix="/loading-slips", tags=["loading-slips"])


async def _assert_firm_exists(db: AsyncSession, firm_id: uuid.UUID) -> None:
    if await db.get(Firm, firm_id) is None:
        raise HTTPException(status_code=422, detail=f"firm_id {firm_id} does not exist")


async def _get_or_404(db: AsyncSession, slip_id: uuid.UUID):
    obj = await crud.get(db, slip_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loading slip not found")
    return obj


@router.post("", response_model=LoadingSlipRead, status_code=status.HTTP_201_CREATED)
async def create_loading_slip(
    data: LoadingSlipCreate,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(get_current_actor),
):
    await _assert_firm_exists(db, data.firm_id)
    return await crud.create(db, data, created_by=actor.id)


@router.get("", response_model=list[LoadingSlipRead])
async def list_loading_slips(
    firm_id: uuid.UUID | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_(db, firm_id=firm_id, date_from=date_from, date_to=date_to)


@router.get("/{slip_id}", response_model=LoadingSlipRead)
async def get_loading_slip(slip_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, slip_id)


@router.patch("/{slip_id}", response_model=LoadingSlipRead)
async def update_loading_slip(
    slip_id: uuid.UUID, data: LoadingSlipUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await _get_or_404(db, slip_id)
    if data.firm_id is not None:
        await _assert_firm_exists(db, data.firm_id)
    return await crud.update(db, obj, data)


@router.delete("/{slip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_loading_slip(slip_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, slip_id)
    await crud.soft_delete(db, obj)
