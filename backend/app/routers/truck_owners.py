import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import truck_owner as crud
from app.deps import get_db
from app.models.bilti import Bilti
from app.models.truck_owner_payment import TruckOwnerPayment
from app.pagination import DEFAULT_LIMIT, Page
from app.schemas.ledger_statement import LedgerStatementLine
from app.schemas.truck_owner import (
    TruckOwnerBalance,
    TruckOwnerRead,
    TruckOwnerStatement,
    TruckOwnerUpdate,
)

router = APIRouter(prefix="/truck-owners", tags=["truck-owners"])


async def _get_or_404(db: AsyncSession, truck_owner_id: uuid.UUID):
    obj = await crud.get(db, truck_owner_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Truck owner not found")
    return obj


@router.get("", response_model=Page[TruckOwnerRead])
async def list_truck_owners(
    active_only: bool = False,
    q: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = DEFAULT_LIMIT,
    db: AsyncSession = Depends(get_db),
):
    items, total, page, limit = await crud.list_(
        db, active_only=active_only, q=q, sort=sort, page=page, limit=limit
    )
    return Page(items=items, total=total, page=page, limit=limit)


@router.get("/{truck_owner_id}", response_model=TruckOwnerRead)
async def get_truck_owner(truck_owner_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, truck_owner_id)


@router.patch("/{truck_owner_id}", response_model=TruckOwnerRead)
async def update_truck_owner(
    truck_owner_id: uuid.UUID, data: TruckOwnerUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await _get_or_404(db, truck_owner_id)
    return await crud.update(db, obj, data)


@router.get("/{truck_owner_id}/balance", response_model=TruckOwnerBalance)
async def truck_owner_balance(
    truck_owner_id: uuid.UUID, firm_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    obj = await _get_or_404(db, truck_owner_id)

    freight_stmt = select(func.coalesce(func.sum(Bilti.freight), 0)).where(
        Bilti.truck_owner_id == truck_owner_id, Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False)
    )
    total_freight: Decimal = (await db.execute(freight_stmt)).scalar_one()

    advance_stmt = select(func.coalesce(func.sum(Bilti.advance_to_owner), 0)).where(
        Bilti.truck_owner_id == truck_owner_id, Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False)
    )
    total_advance: Decimal = (await db.execute(advance_stmt)).scalar_one()

    paid_stmt = select(func.coalesce(func.sum(TruckOwnerPayment.amount), 0)).where(
        TruckOwnerPayment.truck_owner_id == truck_owner_id,
        TruckOwnerPayment.firm_id == firm_id,
        TruckOwnerPayment.is_deleted.is_(False),
    )
    total_paid: Decimal = (await db.execute(paid_stmt)).scalar_one()

    return TruckOwnerBalance(
        truck_owner=obj,
        firm_id=firm_id,
        total_freight=total_freight,
        total_advance=total_advance,
        total_paid=total_paid,
        balance=total_freight - total_advance - total_paid,
    )


@router.get("/{truck_owner_id}/statement", response_model=TruckOwnerStatement)
async def truck_owner_statement(
    truck_owner_id: uuid.UUID, firm_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    """Chronological freight/advance/payment ledger with a running balance,
    for the Ledger Statement PDF. Same "pull every row, don't page" rule as
    agent_statement() -- see that endpoint's docstring.
    """
    obj = await _get_or_404(db, truck_owner_id)

    bilti_stmt = (
        select(Bilti)
        .where(
            Bilti.truck_owner_id == truck_owner_id, Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False)
        )
        .order_by(Bilti.bilti_date)
    )
    bilties = (await db.execute(bilti_stmt)).scalars().all()

    payment_stmt = (
        select(TruckOwnerPayment)
        .where(
            TruckOwnerPayment.truck_owner_id == truck_owner_id,
            TruckOwnerPayment.firm_id == firm_id,
            TruckOwnerPayment.is_deleted.is_(False),
        )
        .order_by(TruckOwnerPayment.payment_date)
    )
    payments = (await db.execute(payment_stmt)).scalars().all()

    entries = [
        ("bilti", b.bilti_date, f"Bilti {b.bilti_no} — Freight", b.bilti_no, b.freight, b.advance_to_owner)
        for b in bilties
    ] + [
        (
            "payment",
            p.payment_date,
            f"Payment{f' ({p.mode})' if p.mode else ''}",
            p.remarks,
            Decimal("0"),
            p.amount,
        )
        for p in payments
    ]
    entries.sort(key=lambda e: e[1])

    running = Decimal("0")
    lines: list[LedgerStatementLine] = []
    total_freight = Decimal("0")
    total_advance = Decimal("0")
    total_paid = Decimal("0")
    for kind, entry_date, particulars, reference, debit, credit in entries:
        running += debit - credit
        total_freight += debit
        if kind == "bilti":
            total_advance += credit
        else:
            total_paid += credit
        lines.append(
            LedgerStatementLine(
                date=entry_date, particulars=particulars, reference=reference,
                debit=debit, credit=credit, balance=running,
            )
        )

    return TruckOwnerStatement(
        truck_owner=obj,
        firm_id=firm_id,
        lines=lines,
        total_freight=total_freight,
        total_advance=total_advance,
        total_paid=total_paid,
        closing_balance=running,
    )
