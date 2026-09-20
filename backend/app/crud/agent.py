import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent
from app.schemas.agent import AgentUpdate


async def get_or_create_by_name(db: AsyncSession, name: str) -> Agent:
    name = name.strip()
    stmt = select(Agent).where(func.lower(Agent.name) == name.lower())
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing is not None:
        return existing
    obj = Agent(name=name)
    db.add(obj)
    await db.flush()
    return obj


async def get(db: AsyncSession, agent_id: uuid.UUID) -> Agent | None:
    return await db.get(Agent, agent_id)


async def list_(db: AsyncSession, active_only: bool = False) -> list[Agent]:
    stmt = select(Agent).order_by(Agent.name)
    if active_only:
        stmt = stmt.where(Agent.is_active.is_(True))
    return list((await db.execute(stmt)).scalars().all())


async def update(db: AsyncSession, obj: Agent, data: AgentUpdate) -> Agent:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj
