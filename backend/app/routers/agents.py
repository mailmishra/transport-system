import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import agent as crud
from app.deps import get_db
from app.models.agent_payment import AgentPayment
from app.models.bilti import Bilti
from app.pagination import DEFAULT_LIMIT, Page
from app.schemas.agent import AgentBalance, AgentRead, AgentStatement, AgentUpdate
from app.schemas.ledger_statement import LedgerStatementLine

router = APIRouter(prefix="/agents", tags=["agents"])


async def _get_or_404(db: AsyncSession, agent_id: uuid.UUID):
    obj = await crud.get(db, agent_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return obj


@router.get("", response_model=Page[AgentRead])
async def list_agents(
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


@router.get("/{agent_id}", response_model=AgentRead)
async def get_agent(agent_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await _get_or_404(db, agent_id)


@router.patch("/{agent_id}", response_model=AgentRead)
async def update_agent(agent_id: uuid.UUID, data: AgentUpdate, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, agent_id)
    return await crud.update(db, obj, data)


@router.get("/{agent_id}/balance", response_model=AgentBalance)
async def agent_balance(agent_id: uuid.UUID, firm_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    obj = await _get_or_404(db, agent_id)

    accrued_stmt = select(func.coalesce(func.sum(Bilti.dalali + Bilti.freight_difference), 0)).where(
        Bilti.agent_id == agent_id, Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False)
    )
    total_accrued: Decimal = (await db.execute(accrued_stmt)).scalar_one()

    paid_stmt = select(func.coalesce(func.sum(AgentPayment.amount), 0)).where(
        AgentPayment.agent_id == agent_id,
        AgentPayment.firm_id == firm_id,
        AgentPayment.is_deleted.is_(False),
    )
    total_paid: Decimal = (await db.execute(paid_stmt)).scalar_one()

    return AgentBalance(
        agent=obj,
        firm_id=firm_id,
        total_accrued=total_accrued,
        total_paid=total_paid,
        balance=total_accrued - total_paid,
    )


@router.get("/{agent_id}/statement", response_model=AgentStatement)
async def agent_statement(agent_id: uuid.UUID, firm_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Chronological accrual+payment ledger with a running balance, for the
    Ledger Statement PDF (components/print/print-document.tsx). Pulls every
    matching row rather than paging through the generic bilti/payment list
    endpoints (capped at pagination.MAX_LIMIT) -- a statement must be
    complete, not a page of one.
    """
    obj = await _get_or_404(db, agent_id)

    bilti_stmt = (
        select(Bilti)
        .where(Bilti.agent_id == agent_id, Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False))
        .order_by(Bilti.bilti_date)
    )
    bilties = (await db.execute(bilti_stmt)).scalars().all()

    payment_stmt = (
        select(AgentPayment)
        .where(
            AgentPayment.agent_id == agent_id,
            AgentPayment.firm_id == firm_id,
            AgentPayment.is_deleted.is_(False),
        )
        .order_by(AgentPayment.payment_date)
    )
    payments = (await db.execute(payment_stmt)).scalars().all()

    entries = [
        (
            b.bilti_date,
            f"Bilti {b.bilti_no} — Dalali/FD",
            b.bilti_no,
            b.dalali + b.freight_difference,
            Decimal("0"),
        )
        for b in bilties
    ] + [
        (
            p.payment_date,
            f"Payment{f' ({p.mode})' if p.mode else ''}",
            p.remarks,
            Decimal("0"),
            p.amount,
        )
        for p in payments
    ]
    entries.sort(key=lambda e: e[0])

    running = Decimal("0")
    lines: list[LedgerStatementLine] = []
    total_accrued = Decimal("0")
    total_paid = Decimal("0")
    for entry_date, particulars, reference, debit, credit in entries:
        running += debit - credit
        total_accrued += debit
        total_paid += credit
        lines.append(
            LedgerStatementLine(
                date=entry_date, particulars=particulars, reference=reference,
                debit=debit, credit=credit, balance=running,
            )
        )

    return AgentStatement(
        agent=obj,
        firm_id=firm_id,
        lines=lines,
        total_accrued=total_accrued,
        total_paid=total_paid,
        closing_balance=running,
    )
