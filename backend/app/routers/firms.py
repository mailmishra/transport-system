from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db
from app.models.firm import Firm
from app.schemas.firm import FirmRead

router = APIRouter(prefix="/firms", tags=["firms"])


@router.get("", response_model=list[FirmRead])
async def list_firms(db: AsyncSession = Depends(get_db)) -> list[Firm]:
    stmt = select(Firm).order_by(Firm.name)
    return list((await db.execute(stmt)).scalars().all())
