import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from app.schemas.agent import AgentRead
from app.schemas.truck_owner import TruckOwnerRead
from app.schemas.vehicle import VehicleRead

_TEXT_FIELDS = (
    "bilti_no",
    "consignor",
    "consignee",
    "from_location",
    "to_location",
    "vehicle_no",
    "truck_owner_name",
    "agent_name",
    "goods_description",
    "weight",
)

_GST_PAID_BY_VALUES = {"consignor", "consignee", "transporter", "exempted"}


class BiltiBase(BaseModel):
    firm_id: uuid.UUID
    loading_slip_id: uuid.UUID | None = None
    bilti_no: str = Field(min_length=1, max_length=50)
    bilti_date: date
    consignor: str = Field(min_length=1)
    consignee: str = Field(min_length=1)
    from_location: str = Field(min_length=1, max_length=200)
    to_location: str = Field(min_length=1, max_length=200)
    # Free text in, normalized to vehicles/agents/truck_owners rows via
    # get-or-create in the CRUD layer (see app/crud/bilti.py) — keeps the
    # simple-text-input UX (dropdown-with-manual-fallback on the frontend)
    # while the DB stores a real FK.
    vehicle_no: str = Field(min_length=1, max_length=50)
    palti_vehicle_no: str | None = Field(default=None, max_length=50)
    truck_owner_name: str = Field(min_length=1, max_length=200)
    agent_name: str = Field(min_length=1, max_length=200)
    goods_description: str = Field(min_length=1)
    weight: str = Field(min_length=1, max_length=100)
    weight_per_bag: Decimal | None = Field(default=None, ge=0)
    charged_weight: str | None = Field(default=None, max_length=100)
    package_count: str | None = Field(default=None, max_length=50)
    package_unit: str | None = Field(default=None, max_length=50)
    freight: Decimal = Field(gt=0)
    freight_rate: Decimal | None = Field(default=None, ge=0)
    dalali: Decimal = Field(default=Decimal("0"), ge=0)
    advance_to_owner: Decimal = Field(default=Decimal("0"), ge=0)
    freight_difference: Decimal = Field(default=Decimal("0"), ge=0)
    other_charges: Decimal = Field(default=Decimal("0"), ge=0)
    kanta_charges: Decimal = Field(default=Decimal("0"), ge=0)
    bahi_charges: Decimal = Field(default=Decimal("0"), ge=0)
    service_tax: Decimal = Field(default=Decimal("0"), ge=0)
    hamali: Decimal = Field(default=Decimal("0"), ge=0)
    p_freight: Decimal = Field(default=Decimal("0"), ge=0)
    gst_paid_by: str | None = Field(default=None, max_length=20)
    eway_bill_no: str | None = Field(default=None, max_length=50)
    invoice_value: Decimal | None = Field(default=None, ge=0)
    insured: bool | None = None
    insurance_company: str | None = Field(default=None, max_length=200)
    insurance_policy_no: str | None = Field(default=None, max_length=100)
    insurance_amount: Decimal | None = Field(default=None, ge=0)
    insurance_date: date | None = None
    insurance_risk: str | None = Field(default=None, max_length=200)
    # Separate from agent_name/the Agent-Dalal ledger on purpose -- the
    # insurance company's agent is an unrelated party.
    insurance_agent_name: str | None = Field(default=None, max_length=200)
    goods_value_declared: Decimal | None = Field(default=None, ge=0)
    remark: str | None = Field(default=None, max_length=500)

    @field_validator(*_TEXT_FIELDS)
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @field_validator("palti_vehicle_no")
    @classmethod
    def blank_optional_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("gst_paid_by")
    @classmethod
    def valid_gst_paid_by(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().lower()
        if not v:
            return None
        if v not in _GST_PAID_BY_VALUES:
            raise ValueError(f"must be one of {sorted(_GST_PAID_BY_VALUES)}")
        return v


class BiltiCreate(BiltiBase):
    pass


class BiltiUpdate(BaseModel):
    firm_id: uuid.UUID | None = None
    loading_slip_id: uuid.UUID | None = None
    bilti_no: str | None = Field(default=None, min_length=1, max_length=50)
    bilti_date: date | None = None
    consignor: str | None = Field(default=None, min_length=1)
    consignee: str | None = Field(default=None, min_length=1)
    from_location: str | None = Field(default=None, min_length=1, max_length=200)
    to_location: str | None = Field(default=None, min_length=1, max_length=200)
    vehicle_no: str | None = Field(default=None, min_length=1, max_length=50)
    palti_vehicle_no: str | None = Field(default=None, max_length=50)
    truck_owner_name: str | None = Field(default=None, min_length=1, max_length=200)
    agent_name: str | None = Field(default=None, max_length=200)
    goods_description: str | None = Field(default=None, min_length=1)
    weight: str | None = Field(default=None, min_length=1, max_length=100)
    weight_per_bag: Decimal | None = Field(default=None, ge=0)
    charged_weight: str | None = Field(default=None, max_length=100)
    package_count: str | None = Field(default=None, max_length=50)
    package_unit: str | None = Field(default=None, max_length=50)
    freight: Decimal | None = Field(default=None, gt=0)
    freight_rate: Decimal | None = Field(default=None, ge=0)
    dalali: Decimal | None = Field(default=None, ge=0)
    advance_to_owner: Decimal | None = Field(default=None, ge=0)
    freight_difference: Decimal | None = Field(default=None, ge=0)
    other_charges: Decimal | None = Field(default=None, ge=0)
    kanta_charges: Decimal | None = Field(default=None, ge=0)
    bahi_charges: Decimal | None = Field(default=None, ge=0)
    service_tax: Decimal | None = Field(default=None, ge=0)
    hamali: Decimal | None = Field(default=None, ge=0)
    p_freight: Decimal | None = Field(default=None, ge=0)
    gst_paid_by: str | None = Field(default=None, max_length=20)
    eway_bill_no: str | None = Field(default=None, max_length=50)
    invoice_value: Decimal | None = Field(default=None, ge=0)
    insured: bool | None = None
    insurance_company: str | None = Field(default=None, max_length=200)
    insurance_policy_no: str | None = Field(default=None, max_length=100)
    insurance_amount: Decimal | None = Field(default=None, ge=0)
    insurance_date: date | None = None
    insurance_risk: str | None = Field(default=None, max_length=200)
    insurance_agent_name: str | None = Field(default=None, max_length=200)
    goods_value_declared: Decimal | None = Field(default=None, ge=0)
    remark: str | None = Field(default=None, max_length=500)


class _BiltiChargeFieldsMixin(BaseModel):
    """Shared by Read/Print: the components that make up the paper GR's
    TOTAL/G.TOTAL/GRAND TOTAL/TOPAY boxes.

    Those totals are never stored -- computed here, same "compute, don't
    duplicate" approach already used for ledger balances (see README).
    Dalali is captured but excluded from grand_total (stored only).
    """

    freight: Decimal
    dalali: Decimal
    other_charges: Decimal
    kanta_charges: Decimal
    bahi_charges: Decimal
    service_tax: Decimal
    hamali: Decimal
    p_freight: Decimal
    advance_to_owner: Decimal

    @computed_field  # type: ignore[prop-decorator]
    @property
    def grand_total(self) -> Decimal:
        return (
            self.freight
            + self.other_charges
            + self.kanta_charges
            + self.bahi_charges
            + self.service_tax
            + self.hamali
            + self.p_freight
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def topay(self) -> Decimal:
        return self.grand_total - self.advance_to_owner


class BiltiRead(_BiltiChargeFieldsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    firm_id: uuid.UUID
    loading_slip_id: uuid.UUID | None
    bilti_no: str
    bilti_date: date
    consignor: str
    consignee: str
    from_location: str
    to_location: str
    vehicle: VehicleRead
    palti_vehicle: VehicleRead | None
    truck_owner: TruckOwnerRead
    agent: AgentRead | None
    goods_description: str
    weight: str
    weight_per_bag: Decimal | None
    charged_weight: str | None
    package_count: str | None
    package_unit: str | None
    freight_rate: Decimal | None
    freight_difference: Decimal
    gst_paid_by: str | None
    eway_bill_no: str | None
    invoice_value: Decimal | None
    insured: bool | None
    insurance_company: str | None
    insurance_policy_no: str | None
    insurance_amount: Decimal | None
    insurance_date: date | None
    insurance_risk: str | None
    insurance_agent_name: str | None
    goods_value_declared: Decimal | None
    remark: str | None
    created_at: datetime
    updated_at: datetime


class BiltiPrint(_BiltiChargeFieldsMixin):
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
    vehicle: VehicleRead
    palti_vehicle: VehicleRead | None
    truck_owner: TruckOwnerRead
    agent: AgentRead | None
    goods_description: str
    weight: str
    weight_per_bag: Decimal | None
    charged_weight: str | None
    package_count: str | None
    package_unit: str | None
    freight_rate: Decimal | None
    gst_paid_by: str | None
    eway_bill_no: str | None
    invoice_value: Decimal | None
    insured: bool | None
    insurance_company: str | None
    insurance_policy_no: str | None
    insurance_amount: Decimal | None
    insurance_date: date | None
    insurance_risk: str | None
    insurance_agent_name: str | None
    goods_value_declared: Decimal | None
    remark: str | None
