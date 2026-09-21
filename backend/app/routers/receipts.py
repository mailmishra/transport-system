import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import bilti as bilti_crud
from app.crud import receipt as crud
from app.deps import Actor, get_current_actor, get_db
from app.models.firm import Firm
from app.pagination import DEFAULT_LIMIT, Page
from app.schemas.receipt import ReceiptCreate, ReceiptRead

router = APIRouter(prefix="/receipts", tags=["receipts"])


async def _get_or_404(db: AsyncSession, receipt_id: uuid.UUID):
    obj = await crud.get(db, receipt_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return obj


@router.post("", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED)
async def create_receipt(
    data: ReceiptCreate,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(get_current_actor),
):
    if await db.get(Firm, data.firm_id) is None:
        raise HTTPException(status_code=422, detail=f"firm_id {data.firm_id} does not exist")
    if await bilti_crud.get(db, data.bilti_id) is None:
        raise HTTPException(status_code=422, detail=f"bilti_id {data.bilti_id} does not exist")
    return await crud.create(db, data, created_by=actor.id)


@router.get("", response_model=Page[ReceiptRead])
async def list_receipts(
    firm_id: uuid.UUID | None = None,
    bilti_id: uuid.UUID | None = None,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
    db: AsyncSession = Depends(get_db),
):
    items, total, page, limit = await crud.list_(
        db, firm_id=firm_id, bilti_id=bilti_id, q=q, sort=sort, page=page, limit=limit
    )
    return Page(items=items, total=total, page=page, limit=limit)


@router.get("/{receipt_id}", response_model=ReceiptRead)
async def get_receipt(receipt_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, receipt_id)


@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_receipt(receipt_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, receipt_id)
    await crud.soft_delete(db, obj)
