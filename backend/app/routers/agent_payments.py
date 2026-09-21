import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import agent as agent_crud
from app.crud import agent_payment as crud
from app.deps import Actor, get_current_actor, get_db
from app.models.firm import Firm
from app.pagination import DEFAULT_LIMIT, Page
from app.schemas.agent_payment import AgentPaymentCreate, AgentPaymentRead

router = APIRouter(prefix="/agent-payments", tags=["agent-payments"])


async def _get_or_404(db: AsyncSession, payment_id: uuid.UUID):
    obj = await crud.get(db, payment_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent payment not found")
    return obj


@router.post("", response_model=AgentPaymentRead, status_code=status.HTTP_201_CREATED)
async def create_agent_payment(
    data: AgentPaymentCreate,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(get_current_actor),
):
    if await db.get(Firm, data.firm_id) is None:
        raise HTTPException(status_code=422, detail=f"firm_id {data.firm_id} does not exist")
    if await agent_crud.get(db, data.agent_id) is None:
        raise HTTPException(status_code=422, detail=f"agent_id {data.agent_id} does not exist")
    return await crud.create(db, data, created_by=actor.id)


@router.get("", response_model=Page[AgentPaymentRead])
async def list_agent_payments(
    firm_id: uuid.UUID | None = None,
    agent_id: uuid.UUID | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
    db: AsyncSession = Depends(get_db),
):
    items, total, page, limit = await crud.list_(
        db, firm_id=firm_id, agent_id=agent_id, sort=sort, page=page, limit=limit
    )
    return Page(items=items, total=total, page=page, limit=limit)


@router.get("/{payment_id}", response_model=AgentPaymentRead)
async def get_agent_payment(payment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, payment_id)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_payment(payment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, payment_id)
    await crud.soft_delete(db, obj)
