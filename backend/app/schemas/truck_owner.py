import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TruckOwnerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    phone: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TruckOwnerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    phone: str | None = Field(default=None, max_length=30)
    is_active: bool | None = None


class TruckOwnerBalance(BaseModel):
    truck_owner: TruckOwnerRead
    firm_id: uuid.UUID
    total_freight: Decimal
    total_advance: Decimal
    total_paid: Decimal
    balance: Decimal
