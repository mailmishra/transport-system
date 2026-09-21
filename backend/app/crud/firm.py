from sqlalchemy.ext.asyncio import AsyncSession

from app.models.firm import Firm
from app.schemas.firm import FirmUpdate


async def update(db: AsyncSession, obj: Firm, data: FirmUpdate) -> Firm:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj
