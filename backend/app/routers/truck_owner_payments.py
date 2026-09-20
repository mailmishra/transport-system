import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import bilti as bilti_crud
from app.crud import truck_owner as truck_owner_crud
from app.crud import truck_owner_payment as crud
from app.deps import Actor, get_current_actor, get_db
from app.models.firm import Firm
from app.schemas.truck_owner_payment import TruckOwnerPaymentCreate, TruckOwnerPaymentRead

router = APIRouter(prefix="/truck-owner-payments", tags=["truck-owner-payments"])


async def _get_or_404(db: AsyncSession, payment_id: uuid.UUID):
    obj = await crud.get(db, payment_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Truck owner payment not found"
        )
    return obj


@router.post("", response_model=TruckOwnerPaymentRead, status_code=status.HTTP_201_CREATED)
async def create_truck_owner_payment(
    data: TruckOwnerPaymentCreate,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(get_current_actor),
):
    if await db.get(Firm, data.firm_id) is None:
        raise HTTPException(status_code=422, detail=f"firm_id {data.firm_id} does not exist")
    if await truck_owner_crud.get(db, data.truck_owner_id) is None:
        raise HTTPException(
            status_code=422, detail=f"truck_owner_id {data.truck_owner_id} does not exist"
        )
    if data.bilti_id is not None and await bilti_crud.get(db, data.bilti_id) is None:
        raise HTTPException(status_code=422, detail=f"bilti_id {data.bilti_id} does not exist")
    return await crud.create(db, data, created_by=actor.id)


@router.get("", response_model=list[TruckOwnerPaymentRead])
async def list_truck_owner_payments(
    firm_id: uuid.UUID | None = None,
    truck_owner_id: uuid.UUID | None = None,
    bilti_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_(db, firm_id=firm_id, truck_owner_id=truck_owner_id, bilti_id=bilti_id)


@router.get("/{payment_id}", response_model=TruckOwnerPaymentRead)
async def get_truck_owner_payment(payment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, payment_id)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_truck_owner_payment(payment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, payment_id)
    await crud.soft_delete(db, obj)
