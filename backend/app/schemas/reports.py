"""Response shapes for backend/app/routers/reports.py. Every report is
computed in SQL against firm-scoped, date-ranged rows -- never a full
table fetch aggregated in Python/JS -- per the Reports + PDF template
plan's "aggregation endpoints, not client-side JS" rule (see the existing
precedent: agent_balance()/truck_owner_balance() in routers/agents.py and
routers/truck_owners.py).
"""
import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class DayBookEntry(BaseModel):
    date: date
    kind: str  # "receipt" | "agent_payment" | "truck_owner_payment"
    particulars: str
    reference: str | None
    inflow: Decimal
    outflow: Decimal


class DayBookReport(BaseModel):
    firm_id: uuid.UUID
    date_from: date | None
    date_to: date | None
    entries: list[DayBookEntry]
    total_inflow: Decimal
    total_outflow: Decimal
    net: Decimal


class OutstandingSummary(BaseModel):
    firm_id: uuid.UUID
    total_receivable: Decimal  # sum of bilti (grand_total - advance_to_owner)
    total_received: Decimal  # sum of receipts
    net_receivable: Decimal
    total_agent_payable: Decimal  # sum over agents of (accrued - paid), floored at 0 per agent
    total_truck_owner_payable: Decimal  # sum over truck owners of (freight - advance - paid), floored at 0


class GstReportRow(BaseModel):
    gst_paid_by: str | None
    bilti_count: int
    total_freight: Decimal
    total_grand_total: Decimal


class VehicleActivityRow(BaseModel):
    vehicle_id: uuid.UUID
    vehicle_no: str
    trip_count: int
    total_freight: Decimal


class ReceivableRow(BaseModel):
    bilti_id: uuid.UUID
    bilti_no: str
    bilti_date: date
    consignor: str
    consignee: str
    topay: Decimal
    received: Decimal
    outstanding: Decimal
    days_outstanding: int
