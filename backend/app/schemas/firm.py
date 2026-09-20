import uuid

from pydantic import BaseModel, ConfigDict


class FirmRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
