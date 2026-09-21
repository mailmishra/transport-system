"""Walks the actual documented business workflow end to end against the
running app (real Postgres, real HTTP layer via ASGI - the only thing not
exercised here is the browser/JS itself, since concept/index.html is a thin
fetch() layer over this same API with no independent logic worth a browser
test):

    Loading Slip -> Bilti/GR -> Agent/Dalal Ledger -> Truck Owner Ledger
    -> Final Receipt -> Reports

Each step's assertion is phrased as the business fact it's supposed to
prove, not just "status code 200".
"""
import pytest

from tests.conftest import get_firm_id
from tests.utils import create_bilti, create_loading_slip, unique

pytestmark = pytest.mark.e2e


def test_full_workflow(client):
    firm_id = get_firm_id(client)
    agent_name = unique("Suresh Dalal")
    owner_name = unique("Ramesh Owner")

    # 1. Loading Slip: goods are booked for transport.
    slip = create_loading_slip(client, firm_id, vehicle_no="MP20AB1234")
    assert slip["vehicle"]["vehicle_no"] == "MP20AB1234"

    # 2. Bilti/GR: the freight document is raised against that Loading Slip,
    #    naming the agent who brokered it and the truck owner carrying it.
    #    Dalali (agent's cut) is visible on the Bilti; FD (freight
    #    difference) is an internal-only accounting field.
    bilti = create_bilti(
        client,
        firm_id,
        loading_slip_id=slip["id"],
        vehicle_no="MP20AB1234",
        agent_name=agent_name,
        truck_owner_name=owner_name,
        freight=15000,
        dalali=500,
        advance_to_owner=2000,
        freight_difference=750,
    )
    assert bilti["loading_slip_id"] == slip["id"]

    # The printed Bilti must never reveal FD, even though it's on the record.
    printable = (client.get(f"/api/bilties/{bilti['id']}/print")).json()
    assert "freight_difference" not in printable

    # 3. Agent/Dalal Ledger: the firm owes the agent dalali + FD until paid.
    agent_id = bilti["agent"]["id"]
    balance_before = (
        client.get(f"/api/agents/{agent_id}/balance", params={"firm_id": firm_id})
    ).json()
    assert balance_before["balance"] == "1250.00"  # 500 dalali + 750 FD, nothing paid yet

    client.post(
        "/api/agent-payments",
        json={
            "firm_id": firm_id,
            "agent_id": agent_id,
            "amount": 1250,
            "payment_date": "2026-01-20",
            "mode": "cash",
        },
    )
    balance_after = (
        client.get(f"/api/agents/{agent_id}/balance", params={"firm_id": firm_id})
    ).json()
    assert balance_after["balance"] == "0.00"  # fully settled

    # 4. Truck Owner Ledger: freight owed to the owner, minus the advance
    #    already given at Bilti time, minus any further settlement.
    owner_id = bilti["truck_owner"]["id"]
    owner_balance_before = (
        client.get(f"/api/truck-owners/{owner_id}/balance", params={"firm_id": firm_id})
    ).json()
    assert owner_balance_before["balance"] == "13000.00"  # 15000 freight - 2000 advance

    client.post(
        "/api/truck-owner-payments",
        json={
            "firm_id": firm_id,
            "truck_owner_id": owner_id,
            "bilti_id": bilti["id"],
            "amount": 13000,
            "payment_date": "2026-01-21",
            "mode": "bank",
        },
    )
    owner_balance_after = (
        client.get(f"/api/truck-owners/{owner_id}/balance", params={"firm_id": firm_id})
    ).json()
    assert owner_balance_after["balance"] == "0.00"

    # 5. Final Receipt: the consignee pays the firm for the freight.
    client.post(
        "/api/receipts",
        json={
            "firm_id": firm_id,
            "bilti_id": bilti["id"],
            "amount": 15000,
            "receipt_date": "2026-01-22",
            "received_from": bilti["consignee"],
        },
    )
    receipts_for_bilti = (
        client.get("/api/receipts", params={"bilti_id": bilti["id"]})
    ).json()
    assert sum(float(r["amount"]) for r in receipts_for_bilti) == 15000.0

    # 6. Reports: this Bilti's freight is now fully received for the firm.
    #    (Reports itself is computed client-side from these same endpoints -
    #    the receipts+bilties data proven correct above is exactly what it
    #    aggregates, so there's no separate reports endpoint to hit here.)
    all_bilties = (client.get("/api/bilties", params={"firm_id": firm_id})).json()
    all_receipts = (client.get("/api/receipts", params={"firm_id": firm_id})).json()
    firm_freight = sum(float(b["freight"]) for b in all_bilties if b["id"] == bilti["id"])
    firm_received = sum(float(r["amount"]) for r in all_receipts if r["bilti_id"] == bilti["id"])
    assert firm_freight == firm_received == 15000.0
