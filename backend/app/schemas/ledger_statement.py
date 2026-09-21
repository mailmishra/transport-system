"""Shared shape for the Agent/Truck-Owner Ledger Statement PDF (Reports +
PDF template plan, Part 1c). One merged, chronological, running-balance
view over the same rows agent_balance()/truck_owner_balance() already sum
-- computed here rather than client-side, same rule as those endpoints.
"""
import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class LedgerStatementLine(BaseModel):
    date: date
    particulars: str
    reference: str | None
    debit: Decimal
    credit: Decimal
    balance: Decimal
