import uuid

import pytest

from tests.conftest import get_firm_id
from tests.utils import create_bilti, unique

pytestmark = pytest.mark.integration


def test_agent_balance_is_accrued_minus_paid(client):
    firm_id = get_firm_id(client)
    agent_name = unique("Suresh")
    b1 = create_bilti(client, firm_id, agent_name=agent_name, dalali=500, freight_difference=250)
    b2 = create_bilti(client, firm_id, agent_name=agent_name, dalali=300, freight_difference=0)
    agent_id = b1["agent"]["id"]
    assert b2["agent"]["id"] == agent_id  # same agent, reused by name

    pay = client.post(
        "/api/agent-payments",
        json={
            "firm_id": firm_id,
            "agent_id": agent_id,
            "amount": 400,
            "payment_date": "2026-01-16",
            "mode": "cash",
        },
    )
    assert pay.status_code == 201
    assert pay.json()["agent"]["name"] == agent_name

    balance = client.get(f"/api/agents/{agent_id}/balance", params={"firm_id": firm_id})
    assert balance.status_code == 200
    body = balance.json()
    # accrued = (500+250) + (300+0) = 1050; paid = 400; balance = 650
    assert body["total_accrued"] == "1050.00"
    assert body["total_paid"] == "400.00"
    assert body["balance"] == "650.00"


def test_agent_payment_amount_must_be_positive(client):
    firm_id = get_firm_id(client)
    bilti = create_bilti(client, firm_id, agent_name=unique("Agent"))
    res = client.post(
        "/api/agent-payments",
        json={
            "firm_id": firm_id,
            "agent_id": bilti["agent"]["id"],
            "amount": 0,
            "payment_date": "2026-01-16",
        },
    )
    assert res.status_code == 422


def test_agent_payment_rejects_unknown_agent(client):
    firm_id = get_firm_id(client)
    res = client.post(
        "/api/agent-payments",
        json={
            "firm_id": firm_id,
            "agent_id": str(uuid.uuid4()),
            "amount": 100,
            "payment_date": "2026-01-16",
        },
    )
    assert res.status_code == 422


def test_truck_owner_balance_is_freight_minus_advance_minus_paid(client):
    firm_id = get_firm_id(client)
    owner_name = unique("Ramesh")
    bilti = create_bilti(
        client, firm_id, truck_owner_name=owner_name, freight=15000, advance_to_owner=2000
    )
    owner_id = bilti["truck_owner"]["id"]

    pay = client.post(
        "/api/truck-owner-payments",
        json={
            "firm_id": firm_id,
            "truck_owner_id": owner_id,
            "bilti_id": bilti["id"],
            "amount": 1000,
            "payment_date": "2026-01-16",
            "mode": "bank",
        },
    )
    assert pay.status_code == 201

    balance = client.get(f"/api/truck-owners/{owner_id}/balance", params={"firm_id": firm_id})
    body = balance.json()
    assert body["total_freight"] == "15000.00"
    assert body["total_advance"] == "2000.00"
    assert body["total_paid"] == "1000.00"
    assert body["balance"] == "12000.00"  # 15000 - 2000 - 1000


def test_receipt_requires_existing_bilti(client):
    firm_id = get_firm_id(client)
    res = client.post(
        "/api/receipts",
        json={
            "firm_id": firm_id,
            "bilti_id": str(uuid.uuid4()),
            "amount": 500,
            "receipt_date": "2026-01-16",
            "received_from": "XYZ Corp",
        },
    )
    assert res.status_code == 422


def test_receipt_create_and_list_by_bilti(client):
    firm_id = get_firm_id(client)
    bilti = create_bilti(client, firm_id, freight=5000)
    created = client.post(
        "/api/receipts",
        json={
            "firm_id": firm_id,
            "bilti_id": bilti["id"],
            "amount": 5000,
            "receipt_date": "2026-01-16",
            "received_from": "XYZ Corp",
        },
    )
    assert created.status_code == 201

    listed = client.get("/api/receipts", params={"bilti_id": bilti["id"]})
    assert len(listed.json()) == 1
    assert listed.json()[0]["amount"] == "5000.00"


def test_agent_and_truck_owner_can_be_renamed_via_patch(client):
    firm_id = get_firm_id(client)
    bilti = create_bilti(client, firm_id, agent_name=unique("Agent"))
    agent_id = bilti["agent"]["id"]

    renamed = client.patch(f"/api/agents/{agent_id}", json={"name": "Corrected Name"})
    assert renamed.status_code == 200
    assert renamed.json()["name"] == "Corrected Name"

    # the existing bilti's agent reference follows the rename - single
    # source of truth, no need to touch bilti rows.
    fetched = client.get(f"/api/bilties/{bilti['id']}")
    assert fetched.json()["agent"]["name"] == "Corrected Name"
