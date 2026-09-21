import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import vehicle as crud
from app.deps import get_db
from app.schemas.vehicle import VehicleRead, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


async def _get_or_404(db: AsyncSession, vehicle_id: uuid.UUID):
    obj = await crud.get(db, vehicle_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return obj


@router.get("", response_model=list[VehicleRead])
async def list_vehicles(active_only: bool = False, db: AsyncSession = Depends(get_db)):
    return await crud.list_(db, active_only=active_only)


@router.get("/{vehicle_id}", response_model=VehicleRead)
async def get_vehicle(vehicle_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, vehicle_id)


@router.patch("/{vehicle_id}", response_model=VehicleRead)
async def update_vehicle(
    vehicle_id: uuid.UUID, data: VehicleUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await _get_or_404(db, vehicle_id)
    return await crud.update(db, obj, data)
