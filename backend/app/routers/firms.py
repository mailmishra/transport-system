import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import firm as crud
from app.deps import get_db
from app.models.firm import Firm
from app.schemas.firm import FirmRead, FirmUpdate

router = APIRouter(prefix="/firms", tags=["firms"])

# Local-disk storage: fine for this system's single-deployment shape (see
# 0004_firm_letterhead migration / Reports+PDF plan). On a host with an
# ephemeral filesystem, MEDIA_DIR needs a mounted volume to survive
# redeploys -- out of scope for this change.
MEDIA_DIR = Path(__file__).resolve().parent.parent.parent / "media" / "logos"
ALLOWED_LOGO_TYPES = {"image/png": ".png", "image/jpeg": ".jpg", "image/svg+xml": ".svg", "image/webp": ".webp"}
MAX_LOGO_BYTES = 2 * 1024 * 1024


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


@router.post("/{firm_id}/logo", response_model=FirmRead)
async def upload_firm_logo(
    firm_id: uuid.UUID, file: UploadFile, db: AsyncSession = Depends(get_db)
) -> Firm:
    obj = await db.get(Firm, firm_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Firm not found")

    ext = ALLOWED_LOGO_TYPES.get(file.content_type or "")
    if ext is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Logo must be a PNG, JPEG, WebP, or SVG image",
        )
    body = await file.read()
    if len(body) > MAX_LOGO_BYTES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Logo must be under 2MB"
        )

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    dest = MEDIA_DIR / f"{firm_id}{ext}"
    dest.write_bytes(body)

    obj.logo_url = f"/media/logos/{firm_id}{ext}"
    await db.commit()
    await db.refresh(obj)
    return obj
