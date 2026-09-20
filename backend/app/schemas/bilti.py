import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

_TEXT_FIELDS = (
    "bilti_no",
    "consignor",
    "consignee",
    "from_location",
    "to_location",
    "vehicle_no",
    "truck_owner",
    "goods_description",
    "weight",
)


class BiltiBase(BaseModel):
    firm_id: uuid.UUID
    loading_slip_id: uuid.UUID | None = None
    bilti_no: str = Field(min_length=1, max_length=50)
    bilti_date: date
    consignor: str = Field(min_length=1, max_length=200)
    consignee: str = Field(min_length=1, max_length=200)
    from_location: str = Field(min_length=1, max_length=200)
    to_location: str = Field(min_length=1, max_length=200)
    vehicle_no: str = Field(min_length=1, max_length=50)
    truck_owner: str = Field(min_length=1, max_length=200)
    agent: str | None = Field(default=None, max_length=200)
    goods_description: str = Field(min_length=1, max_length=300)
    weight: str = Field(min_length=1, max_length=100)
    freight: Decimal = Field(gt=0)
    dalali: Decimal = Field(default=Decimal("0"), ge=0)
    advance_to_owner: Decimal = Field(default=Decimal("0"), ge=0)
    freight_difference: Decimal = Field(default=Decimal("0"), ge=0)

    @field_validator(*_TEXT_FIELDS)
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @field_validator("agent")
    @classmethod
    def blank_agent_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


class BiltiCreate(BiltiBase):
    pass


class BiltiUpdate(BaseModel):
    firm_id: uuid.UUID | None = None
    loading_slip_id: uuid.UUID | None = None
    bilti_no: str | None = Field(default=None, min_length=1, max_length=50)
    bilti_date: date | None = None
    consignor: str | None = Field(default=None, min_length=1, max_length=200)
    consignee: str | None = Field(default=None, min_length=1, max_length=200)
    from_location: str | None = Field(default=None, min_length=1, max_length=200)
    to_location: str | None = Field(default=None, min_length=1, max_length=200)
    vehicle_no: str | None = Field(default=None, min_length=1, max_length=50)
    truck_owner: str | None = Field(default=None, min_length=1, max_length=200)
    agent: str | None = Field(default=None, max_length=200)
    goods_description: str | None = Field(default=None, min_length=1, max_length=300)
    weight: str | None = Field(default=None, min_length=1, max_length=100)
    freight: Decimal | None = Field(default=None, gt=0)
    dalali: Decimal | None = Field(default=None, ge=0)
    advance_to_owner: Decimal | None = Field(default=None, ge=0)
    freight_difference: Decimal | None = Field(default=None, ge=0)


class BiltiRead(BiltiBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class BiltiPrint(BaseModel):
    """Printable view — freight_difference is deliberately excluded.

    FD (Freight Difference) must never appear on the printed Bilti even
    though it's stored and used in the Agent/Dalal Ledger.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    firm_id: uuid.UUID
    bilti_no: str
    bilti_date: date
    consignor: str
    consignee: str
    from_location: str
    to_location: str
    vehicle_no: str
    truck_owner: str
    agent: str | None
    goods_description: str
    weight: str
    freight: Decimal
    dalali: Decimal
    advance_to_owner: Decimal
