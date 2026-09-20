import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LoadingSlipBase(BaseModel):
    firm_id: uuid.UUID
    slip_date: date
    vehicle_no: str = Field(min_length=1, max_length=50)
    loading_point: str = Field(min_length=1, max_length=200)
    destination: str = Field(min_length=1, max_length=200)
    goods_description: str = Field(min_length=1, max_length=300)
    quantity_weight: str = Field(min_length=1, max_length=100)

    @field_validator(
        "vehicle_no", "loading_point", "destination", "goods_description", "quantity_weight"
    )
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v


class LoadingSlipCreate(LoadingSlipBase):
    pass


class LoadingSlipUpdate(BaseModel):
    firm_id: uuid.UUID | None = None
    slip_date: date | None = None
    vehicle_no: str | None = Field(default=None, min_length=1, max_length=50)
    loading_point: str | None = Field(default=None, min_length=1, max_length=200)
    destination: str | None = Field(default=None, min_length=1, max_length=200)
    goods_description: str | None = Field(default=None, min_length=1, max_length=300)
    quantity_weight: str | None = Field(default=None, min_length=1, max_length=100)


class LoadingSlipRead(LoadingSlipBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
