import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VehicleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vehicle_no: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class VehicleUpdate(BaseModel):
    vehicle_no: str | None = Field(default=None, min_length=1, max_length=50)
    is_active: bool | None = None
