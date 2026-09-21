import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import vehicle as crud
from app.deps import get_db
from app.pagination import DEFAULT_LIMIT, Page
from app.schemas.vehicle import VehicleRead, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


async def _get_or_404(db: AsyncSession, vehicle_id: uuid.UUID):
    obj = await crud.get(db, vehicle_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return obj


@router.get("", response_model=Page[VehicleRead])
async def list_vehicles(
    active_only: bool = False,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
    db: AsyncSession = Depends(get_db),
):
    items, total, page, limit = await crud.list_(
        db, active_only=active_only, q=q, sort=sort, page=page, limit=limit
    )
    return Page(items=items, total=total, page=page, limit=limit)


@router.get("/{vehicle_id}", response_model=VehicleRead)
async def get_vehicle(vehicle_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, vehicle_id)


@router.patch("/{vehicle_id}", response_model=VehicleRead)
async def update_vehicle(
    vehicle_id: uuid.UUID, data: VehicleUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await _get_or_404(db, vehicle_id)
    return await crud.update(db, obj, data)
