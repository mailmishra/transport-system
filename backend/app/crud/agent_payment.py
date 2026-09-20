import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent_payment import AgentPayment
from app.schemas.agent_payment import AgentPaymentCreate


async def create(db: AsyncSession, data: AgentPaymentCreate, created_by: str | None) -> AgentPayment:
    obj = AgentPayment(**data.model_dump(), created_by=created_by)
    db.add(obj)
    await db.commit()
    await db.refresh(obj, attribute_names=["agent"])
    return obj


async def get(db: AsyncSession, payment_id: uuid.UUID) -> AgentPayment | None:
    stmt = select(AgentPayment).where(
        AgentPayment.id == payment_id, AgentPayment.is_deleted.is_(False)
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def list_(
    db: AsyncSession, firm_id: uuid.UUID | None = None, agent_id: uuid.UUID | None = None
) -> list[AgentPayment]:
    stmt = select(AgentPayment).where(AgentPayment.is_deleted.is_(False))
    if firm_id is not None:
        stmt = stmt.where(AgentPayment.firm_id == firm_id)
    if agent_id is not None:
        stmt = stmt.where(AgentPayment.agent_id == agent_id)
    stmt = stmt.order_by(AgentPayment.payment_date.desc(), AgentPayment.created_at.desc())
    return list((await db.execute(stmt)).scalars().all())


async def soft_delete(db: AsyncSession, obj: AgentPayment) -> None:
    obj.is_deleted = True
    await db.commit()
