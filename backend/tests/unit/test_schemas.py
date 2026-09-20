"""Pydantic validation - no DB needed."""
import uuid

import pytest
from pydantic import ValidationError

from app.schemas.bilti import BiltiCreate
from app.schemas.loading_slip import LoadingSlipCreate
from app.schemas.receipt import ReceiptCreate

FIRM_ID = uuid.uuid4()


def _bilti_payload(**overrides):
    payload = dict(
        firm_id=FIRM_ID,
        bilti_no="B-1",
        bilti_date="2026-01-15",
        consignor="ABC",
        consignee="XYZ",
        from_location="Katni",
        to_location="Jabalpur",
        vehicle_no="MP20AB1234",
        truck_owner_name="Ramesh",
        agent_name="Suresh",
        goods_description="Cement",
        weight="10 tons",
        freight=15000,
    )
    payload.update(overrides)
    return payload


def test_bilti_create_accepts_valid_payload():
    b = BiltiCreate(**_bilti_payload())
    assert b.freight == 15000
    assert b.dalali == 0  # default


def test_bilti_freight_must_be_positive():
    with pytest.raises(ValidationError):
        BiltiCreate(**_bilti_payload(freight=0))
    with pytest.raises(ValidationError):
        BiltiCreate(**_bilti_payload(freight=-100))


def test_bilti_dalali_cannot_be_negative():
    with pytest.raises(ValidationError):
        BiltiCreate(**_bilti_payload(dalali=-1))


@pytest.mark.parametrize(
    "field", ["bilti_no", "consignor", "vehicle_no", "truck_owner_name", "goods_description"]
)
def test_bilti_required_text_fields_reject_blank(field):
    with pytest.raises(ValidationError):
        BiltiCreate(**_bilti_payload(**{field: "   "}))


def test_bilti_blank_agent_name_becomes_none():
    b = BiltiCreate(**_bilti_payload(agent_name="   "))
    assert b.agent_name is None


def test_bilti_missing_agent_name_is_fine():
    payload = _bilti_payload()
    del payload["agent_name"]
    b = BiltiCreate(**payload)
    assert b.agent_name is None


def test_loading_slip_requires_non_blank_fields():
    base = dict(
        firm_id=FIRM_ID,
        slip_date="2026-01-15",
        vehicle_no="MP20AB1234",
        loading_point="Katni",
        destination="Jabalpur",
        goods_description="Cement",
        quantity_weight="10 tons",
    )
    LoadingSlipCreate(**base)  # valid, should not raise
    with pytest.raises(ValidationError):
        LoadingSlipCreate(**{**base, "vehicle_no": ""})


def test_receipt_amount_must_be_positive():
    base = dict(
        firm_id=FIRM_ID,
        bilti_id=uuid.uuid4(),
        receipt_date="2026-01-15",
        received_from="XYZ Corp",
    )
    ReceiptCreate(**base, amount=100)  # valid
    with pytest.raises(ValidationError):
        ReceiptCreate(**base, amount=0)


def test_receipt_blank_remarks_becomes_none():
    r = ReceiptCreate(
        firm_id=FIRM_ID,
        bilti_id=uuid.uuid4(),
        receipt_date="2026-01-15",
        received_from="XYZ Corp",
        amount=100,
        remarks="   ",
    )
    assert r.remarks is None
