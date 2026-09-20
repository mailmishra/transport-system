import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.truck_owner import TruckOwnerRead


class TruckOwnerPaymentBase(BaseModel):
    firm_id: uuid.UUID
    truck_owner_id: uuid.UUID
    bilti_id: uuid.UUID | None = None
    amount: Decimal = Field(gt=0)
    payment_date: date
    mode: str | None = Field(default=None, max_length=50)
    remarks: str | None = Field(default=None, max_length=300)

    @field_validator("mode", "remarks")
    @classmethod
    def blank_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


class TruckOwnerPaymentCreate(TruckOwnerPaymentBase):
    pass


class TruckOwnerPaymentRead(TruckOwnerPaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    truck_owner: TruckOwnerRead
    created_at: datetime
    updated_at: datetime
