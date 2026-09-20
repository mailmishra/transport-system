import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReceiptBase(BaseModel):
    firm_id: uuid.UUID
    bilti_id: uuid.UUID
    amount: Decimal = Field(gt=0)
    receipt_date: date
    received_from: str = Field(min_length=1, max_length=200)
    remarks: str | None = Field(default=None, max_length=300)

    @field_validator("received_from")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @field_validator("remarks")
    @classmethod
    def blank_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
