import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import firm as crud
from app.deps import get_db
from app.models.firm import Firm
from app.schemas.firm import FirmRead, FirmUpdate

router = APIRouter(prefix="/firms", tags=["firms"])


@router.get("", response_model=list[FirmRead])
async def list_firms(db: AsyncSession = Depends(get_db)) -> list[Firm]:
    stmt = select(Firm).order_by(Firm.name)
    return list((await db.execute(stmt)).scalars().all())


@router.patch("/{firm_id}", response_model=FirmRead)
async def update_firm(firm_id: uuid.UUID, data: FirmUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Firm, firm_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Firm not found")
    return await crud.update(db, obj, data)
