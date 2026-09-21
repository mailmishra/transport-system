"""Reports module backend (Reports + PDF template plan, Part 2). Every
endpoint here is firm-scoped and date-ranged, and does its grouping/summing
in SQL -- see schemas/reports.py's module docstring for the rule this
follows. The Bilti-wise Register and Loading Slip Register reports have no
endpoint of their own: GET /bilties and GET /loading-slips already support
firm_id/date_from/date_to/vehicle_id/agent_id/truck_owner_id filtering
(added alongside this router) and a Reports UI can call them directly.
"""
import uuid
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db
from app.models.agent import Agent
from app.models.agent_payment import AgentPayment
from app.models.bilti import Bilti
from app.models.loading_slip import LoadingSlip
from app.models.receipt import Receipt
from app.models.truck_owner import TruckOwner
from app.models.truck_owner_payment import TruckOwnerPayment
from app.models.vehicle import Vehicle
from app.schemas.loading_slip import LoadingSlipRead
from app.schemas.reports import (
    DayBookEntry,
    DayBookReport,
    GstReportRow,
    OutstandingSummary,
    ReceivableRow,
    VehicleActivityRow,
)

router = APIRouter(prefix="/reports", tags=["reports"])


def _date_range(stmt, column, date_from: date | None, date_to: date | None):
    if date_from is not None:
        stmt = stmt.where(column >= date_from)
    if date_to is not None:
        stmt = stmt.where(column <= date_to)
    return stmt


@router.get("/day-book", response_model=DayBookReport)
async def day_book(
    firm_id: uuid.UUID,
    date_from: date | None = None,
    date_to: date | None = None,
    db: AsyncSession = Depends(get_db),
) -> DayBookReport:
    """Every cash movement in the window: receipts (money in) and
    agent/truck-owner payments (money out) -- a day book, not an accrual
    ledger (Bilti bookings themselves move no cash).
    """
    receipt_stmt = _date_range(
        select(Receipt).where(Receipt.firm_id == firm_id, Receipt.is_deleted.is_(False)),
        Receipt.receipt_date, date_from, date_to,
    ).order_by(Receipt.receipt_date)
    receipts = (await db.execute(receipt_stmt)).scalars().all()

    agent_pay_stmt = _date_range(
        select(AgentPayment).where(AgentPayment.firm_id == firm_id, AgentPayment.is_deleted.is_(False)),
        AgentPayment.payment_date, date_from, date_to,
    ).order_by(AgentPayment.payment_date)
    agent_payments = (await db.execute(agent_pay_stmt)).scalars().all()

    truck_pay_stmt = _date_range(
        select(TruckOwnerPayment).where(
            TruckOwnerPayment.firm_id == firm_id, TruckOwnerPayment.is_deleted.is_(False)
        ),
        TruckOwnerPayment.payment_date, date_from, date_to,
    ).order_by(TruckOwnerPayment.payment_date)
    truck_payments = (await db.execute(truck_pay_stmt)).scalars().all()

    entries = (
        [
            DayBookEntry(
                date=r.receipt_date, kind="receipt",
                particulars=f"Receipt from {r.received_from}", reference=r.remarks,
                inflow=r.amount, outflow=Decimal("0"),
            )
            for r in receipts
        ]
        + [
            DayBookEntry(
                date=p.payment_date, kind="agent_payment",
                particulars=f"Payment to agent {p.agent.name}", reference=p.remarks,
                inflow=Decimal("0"), outflow=p.amount,
            )
            for p in agent_payments
        ]
        + [
            DayBookEntry(
                date=p.payment_date, kind="truck_owner_payment",
                particulars=f"Payment to truck owner {p.truck_owner.name}", reference=p.remarks,
                inflow=Decimal("0"), outflow=p.amount,
            )
            for p in truck_payments
        ]
    )
    entries.sort(key=lambda e: e.date)

    total_inflow = sum((e.inflow for e in entries), Decimal("0"))
    total_outflow = sum((e.outflow for e in entries), Decimal("0"))

    return DayBookReport(
        firm_id=firm_id, date_from=date_from, date_to=date_to, entries=entries,
        total_inflow=total_inflow, total_outflow=total_outflow, net=total_inflow - total_outflow,
    )


@router.get("/outstanding-summary", response_model=OutstandingSummary)
async def outstanding_summary(firm_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> OutstandingSummary:
    """Firm-wide snapshot, not date-ranged -- "what's owed right now"."""
    receivable_stmt = select(
        func.coalesce(func.sum(Bilti.freight + Bilti.other_charges + Bilti.kanta_charges
                                + Bilti.bahi_charges + Bilti.service_tax + Bilti.hamali
                                + Bilti.p_freight - Bilti.advance_to_owner), 0)
    ).where(Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False))
    total_receivable: Decimal = (await db.execute(receivable_stmt)).scalar_one()

    received_stmt = select(func.coalesce(func.sum(Receipt.amount), 0)).where(
        Receipt.firm_id == firm_id, Receipt.is_deleted.is_(False)
    )
    total_received: Decimal = (await db.execute(received_stmt)).scalar_one()

    # Per-agent (accrued - paid), floored at 0 and summed -- an agent who's
    # been overpaid doesn't offset what's owed to a different agent.
    agent_stmt = (
        select(
            func.coalesce(func.sum(Bilti.dalali + Bilti.freight_difference), 0).label("accrued"),
            Bilti.agent_id,
        )
        .where(Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False), Bilti.agent_id.isnot(None))
        .group_by(Bilti.agent_id)
        .subquery()
    )
    agent_paid_stmt = (
        select(
            func.coalesce(func.sum(AgentPayment.amount), 0).label("paid"), AgentPayment.agent_id
        )
        .where(AgentPayment.firm_id == firm_id, AgentPayment.is_deleted.is_(False))
        .group_by(AgentPayment.agent_id)
        .subquery()
    )
    agent_rows = (
        await db.execute(
            select(agent_stmt.c.accrued, func.coalesce(agent_paid_stmt.c.paid, 0)).select_from(
                agent_stmt.outerjoin(agent_paid_stmt, agent_stmt.c.agent_id == agent_paid_stmt.c.agent_id)
            )
        )
    ).all()
    total_agent_payable = sum((max(accrued - paid, Decimal("0")) for accrued, paid in agent_rows), Decimal("0"))

    owner_stmt = (
        select(
            func.coalesce(func.sum(Bilti.freight), 0).label("freight"),
            func.coalesce(func.sum(Bilti.advance_to_owner), 0).label("advance"),
            Bilti.truck_owner_id,
        )
        .where(Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False))
        .group_by(Bilti.truck_owner_id)
        .subquery()
    )
    owner_paid_stmt = (
        select(
            func.coalesce(func.sum(TruckOwnerPayment.amount), 0).label("paid"),
            TruckOwnerPayment.truck_owner_id,
        )
        .where(TruckOwnerPayment.firm_id == firm_id, TruckOwnerPayment.is_deleted.is_(False))
        .group_by(TruckOwnerPayment.truck_owner_id)
        .subquery()
    )
    owner_rows = (
        await db.execute(
            select(
                owner_stmt.c.freight, owner_stmt.c.advance, func.coalesce(owner_paid_stmt.c.paid, 0)
            ).select_from(
                owner_stmt.outerjoin(
                    owner_paid_stmt, owner_stmt.c.truck_owner_id == owner_paid_stmt.c.truck_owner_id
                )
            )
        )
    ).all()
    total_truck_owner_payable = sum(
        (max(freight - advance - paid, Decimal("0")) for freight, advance, paid in owner_rows), Decimal("0")
    )

    return OutstandingSummary(
        firm_id=firm_id,
        total_receivable=total_receivable,
        total_received=total_received,
        net_receivable=total_receivable - total_received,
        total_agent_payable=total_agent_payable,
        total_truck_owner_payable=total_truck_owner_payable,
    )


@router.get("/gst", response_model=list[GstReportRow])
async def gst_report(
    firm_id: uuid.UUID,
    date_from: date | None = None,
    date_to: date | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[GstReportRow]:
    stmt = _date_range(
        select(
            Bilti.gst_paid_by,
            func.count(Bilti.id),
            func.coalesce(func.sum(Bilti.freight), 0),
            func.coalesce(
                func.sum(Bilti.freight + Bilti.other_charges + Bilti.kanta_charges
                          + Bilti.bahi_charges + Bilti.service_tax + Bilti.hamali + Bilti.p_freight), 0
            ),
        ).where(Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False)),
        Bilti.bilti_date, date_from, date_to,
    ).group_by(Bilti.gst_paid_by)

    rows = (await db.execute(stmt)).all()
    return [
        GstReportRow(gst_paid_by=gst_paid_by, bilti_count=count, total_freight=freight, total_grand_total=grand)
        for gst_paid_by, count, freight, grand in rows
    ]


@router.get("/vehicle-activity", response_model=list[VehicleActivityRow])
async def vehicle_activity(
    firm_id: uuid.UUID,
    date_from: date | None = None,
    date_to: date | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[VehicleActivityRow]:
    stmt = _date_range(
        select(
            Vehicle.id, Vehicle.vehicle_no, func.count(Bilti.id), func.coalesce(func.sum(Bilti.freight), 0)
        )
        .join(Bilti, Bilti.vehicle_id == Vehicle.id)
        .where(Bilti.firm_id == firm_id, Bilti.is_deleted.is_(False)),
        Bilti.bilti_date, date_from, date_to,
    ).group_by(Vehicle.id, Vehicle.vehicle_no).order_by(func.count(Bilti.id).desc())

    rows = (await db.execute(stmt)).all()
    return [
        VehicleActivityRow(vehicle_id=vid, vehicle_no=no, trip_count=count, total_freight=freight)
        for vid, no, count, freight in rows
    ]


@router.get("/pending-loading-slips", response_model=list[LoadingSlipRead])
async def pending_loading_slips(firm_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Loading slips with no Bilti/GR raised against them yet -- a dispatch
    follow-up queue, not date-ranged (a slip stays "pending" until closed).
    """
    linked_ids = select(Bilti.loading_slip_id).where(
        Bilti.loading_slip_id.isnot(None), Bilti.is_deleted.is_(False)
    )
    stmt = (
        select(LoadingSlip)
        .where(
            LoadingSlip.firm_id == firm_id,
            LoadingSlip.is_deleted.is_(False),
            LoadingSlip.id.notin_(linked_ids),
        )
        .order_by(LoadingSlip.slip_date.desc())
    )
    return (await db.execute(stmt)).scalars().all()


@router.get("/receivables", response_model=list[ReceivableRow])
async def receivables(
    firm_id: uuid.UUID, as_of: date | None = None, db: AsyncSession = Depends(get_db)
) -> list[ReceivableRow]:
    """Bilties whose to-pay amount exceeds what's been received against
    them, aged from bilti_date to `as_of` (defaults to today).
    """
    as_of = as_of or date.today()

    received_stmt = (
        select(Receipt.bilti_id, func.coalesce(func.sum(Receipt.amount), 0).label("received"))
        .where(Receipt.is_deleted.is_(False))
        .group_by(Receipt.bilti_id)
        .subquery()
    )
    topay_expr = (
        Bilti.freight + Bilti.other_charges + Bilti.kanta_charges + Bilti.bahi_charges
        + Bilti.service_tax + Bilti.hamali + Bilti.p_freight - Bilti.advance_to_owner
    )
    stmt = (
        select(Bilti, func.coalesce(received_stmt.c.received, 0))
        .outerjoin(received_stmt, received_stmt.c.bilti_id == Bilti.id)
        .where(
            Bilti.firm_id == firm_id,
            Bilti.is_deleted.is_(False),
            topay_expr > func.coalesce(received_stmt.c.received, 0),
        )
        .order_by(Bilti.bilti_date)
    )
    rows = (await db.execute(stmt)).all()

    def topay_of(b: Bilti) -> Decimal:
        # Mirrors BiltiRead.grand_total/topay (schemas/bilti.py) -- those
        # are Pydantic computed_fields on the read schema, not columns on
        # the ORM model, so the same formula is repeated here in Python
        # over the already-fetched row rather than in the SQL projection.
        grand_total = (
            b.freight + b.other_charges + b.kanta_charges + b.bahi_charges
            + b.service_tax + b.hamali + b.p_freight
        )
        return grand_total - b.advance_to_owner

    return [
        ReceivableRow(
            bilti_id=b.id, bilti_no=b.bilti_no, bilti_date=b.bilti_date,
            consignor=b.consignor, consignee=b.consignee,
            topay=topay_of(b), received=received, outstanding=topay_of(b) - received,
            days_outstanding=(as_of - b.bilti_date).days,
        )
        for b, received in rows
    ]
