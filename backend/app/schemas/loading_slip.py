import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.agent import AgentRead
from app.schemas.truck_owner import TruckOwnerRead
from app.schemas.vehicle import VehicleRead


class LoadingSlipBase(BaseModel):
    firm_id: uuid.UUID
    slip_date: date
    # Free text in, normalized to vehicles/truck_owners/agents rows via
    # get-or-create in the CRUD layer (see app/crud/loading_slip.py) --
    # same dropdown-with-manual-fallback pattern as Bilti/GR.
    vehicle_no: str = Field(min_length=1, max_length=50)
    truck_owner_name: str | None = Field(default=None, max_length=200)
    agent_name: str | None = Field(default=None, max_length=200)
    loading_point: str = Field(min_length=1, max_length=200)
    destination: str = Field(min_length=1, max_length=200)
    goods_description: str = Field(min_length=1, max_length=300)
    quantity_weight: str = Field(min_length=1, max_length=100)
    package_count: str | None = Field(default=None, max_length=50)
    advance_amount: Decimal = Field(default=Decimal("0"), ge=0)
    advance_note: str | None = Field(default=None, max_length=500)

    @field_validator(
        "vehicle_no", "loading_point", "destination", "goods_description", "quantity_weight"
    )
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @field_validator("truck_owner_name", "agent_name")
    @classmethod
    def blank_optional_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


class LoadingSlipCreate(LoadingSlipBase):
    pass


class LoadingSlipUpdate(BaseModel):
    firm_id: uuid.UUID | None = None
    slip_date: date | None = None
    vehicle_no: str | None = Field(default=None, min_length=1, max_length=50)
    truck_owner_name: str | None = Field(default=None, max_length=200)
    agent_name: str | None = Field(default=None, max_length=200)
    loading_point: str | None = Field(default=None, min_length=1, max_length=200)
    destination: str | None = Field(default=None, min_length=1, max_length=200)
    goods_description: str | None = Field(default=None, min_length=1, max_length=300)
    quantity_weight: str | None = Field(default=None, min_length=1, max_length=100)
    package_count: str | None = Field(default=None, max_length=50)
    advance_amount: Decimal | None = Field(default=None, ge=0)
    advance_note: str | None = Field(default=None, max_length=500)


class LoadingSlipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    firm_id: uuid.UUID
    slip_date: date
    vehicle: VehicleRead
    truck_owner: TruckOwnerRead | None
    agent: AgentRead | None
    loading_point: str
    destination: str
    goods_description: str
    quantity_weight: str
    package_count: str | None
    advance_amount: Decimal
    advance_note: str | None
    created_at: datetime
    updated_at: datetime
