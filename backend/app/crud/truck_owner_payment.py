import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.truck_owner_payment import TruckOwnerPayment
from app.schemas.truck_owner_payment import TruckOwnerPaymentCreate


async def create(
    db: AsyncSession, data: TruckOwnerPaymentCreate, created_by: str | None
) -> TruckOwnerPayment:
    obj = TruckOwnerPayment(**data.model_dump(), created_by=created_by)
    db.add(obj)
    await db.commit()
    await db.refresh(obj, attribute_names=["truck_owner"])
    return obj


async def get(db: AsyncSession, payment_id: uuid.UUID) -> TruckOwnerPayment | None:
    stmt = select(TruckOwnerPayment).where(
        TruckOwnerPayment.id == payment_id, TruckOwnerPayment.is_deleted.is_(False)
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def list_(
    db: AsyncSession,
    firm_id: uuid.UUID | None = None,
    truck_owner_id: uuid.UUID | None = None,
    bilti_id: uuid.UUID | None = None,
) -> list[TruckOwnerPayment]:
    stmt = select(TruckOwnerPayment).where(TruckOwnerPayment.is_deleted.is_(False))
    if firm_id is not None:
        stmt = stmt.where(TruckOwnerPayment.firm_id == firm_id)
    if truck_owner_id is not None:
        stmt = stmt.where(TruckOwnerPayment.truck_owner_id == truck_owner_id)
    if bilti_id is not None:
        stmt = stmt.where(TruckOwnerPayment.bilti_id == bilti_id)
    stmt = stmt.order_by(TruckOwnerPayment.payment_date.desc(), TruckOwnerPayment.created_at.desc())
    return list((await db.execute(stmt)).scalars().all())


async def soft_delete(db: AsyncSession, obj: TruckOwnerPayment) -> None:
    obj.is_deleted = True
    await db.commit()
