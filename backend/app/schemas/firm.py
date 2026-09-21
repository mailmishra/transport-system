import uuid

from pydantic import BaseModel, ConfigDict, Field


class FirmRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    address: str | None
    phone: str | None
    email: str | None
    pan_no: str | None
    bank_account_no: str | None
    bank_name: str | None
    bank_branch: str | None
    bank_ifsc: str | None


class FirmUpdate(BaseModel):
    address: str | None = Field(default=None, max_length=300)
    phone: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=200)
    pan_no: str | None = Field(default=None, max_length=20)
    bank_account_no: str | None = Field(default=None, max_length=50)
    bank_name: str | None = Field(default=None, max_length=200)
    bank_branch: str | None = Field(default=None, max_length=200)
    bank_ifsc: str | None = Field(default=None, max_length=20)
