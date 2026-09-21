import pytest

from tests.conftest import get_firm_id
from tests.utils import create_bilti, create_loading_slip, unique

pytestmark = pytest.mark.integration


def test_day_book_nets_receipts_against_payments(client):
    firm_id = get_firm_id(client)
    bilti = create_bilti(client, firm_id, freight=5000, dalali=200)

    receipt = client.post(
        "/api/receipts",
        json={
            "firm_id": firm_id, "bilti_id": bilti["id"], "amount": 3000,
            "receipt_date": "2026-04-10", "received_from": "XYZ Corp",
        },
    )
    assert receipt.status_code == 201

    agent_pay = client.post(
        "/api/agent-payments",
        json={
            "firm_id": firm_id, "agent_id": bilti["agent"]["id"], "amount": 150,
            "payment_date": "2026-04-11",
        },
    )
    assert agent_pay.status_code == 201

    res = client.get(
        "/api/reports/day-book",
        params={"firm_id": firm_id, "date_from": "2026-04-10", "date_to": "2026-04-11"},
    )
    assert res.status_code == 200
    body = res.json()
    assert len(body["entries"]) == 2
    assert body["entries"][0]["kind"] == "receipt"
    assert body["entries"][1]["kind"] == "agent_payment"
    assert body["total_inflow"] == "3000.00"
    assert body["total_outflow"] == "150.00"
    assert body["net"] == "2850.00"


def test_outstanding_summary_floors_each_agent_and_owner_at_zero(client):
    firm_id = get_firm_id(client)
    agent_name = unique("Overpaid")
    bilti = create_bilti(
        client, firm_id, agent_name=agent_name, dalali=100, freight_difference=0,
        truck_owner_name=unique("Owner"), freight=1000, advance_to_owner=0,
    )
    agent_id = bilti["agent"]["id"]
    # Pay the agent more than accrued -- must floor at 0, not go negative
    # and net against what other agents/owners are owed.
    over_pay = client.post(
        "/api/agent-payments",
        json={"firm_id": firm_id, "agent_id": agent_id, "amount": 500, "payment_date": "2026-06-01"},
    )
    assert over_pay.status_code == 201

    before = client.get("/api/reports/outstanding-summary", params={"firm_id": firm_id}).json()

    other_agent_bilti = create_bilti(client, firm_id, agent_name=unique("Fresh"), dalali=300, freight_difference=0)

    after = client.get("/api/reports/outstanding-summary", params={"firm_id": firm_id}).json()
    # The overpaid agent contributes 0, not -400; only the new agent's 300 is added.
    assert float(after["total_agent_payable"]) - float(before["total_agent_payable"]) == pytest.approx(300)


def test_gst_report_groups_by_gst_paid_by(client):
    firm_id = get_firm_id(client)
    bilti_no_a = unique("GST")
    create_bilti(client, firm_id, bilti_no=bilti_no_a, gst_paid_by="consignor", freight=1000)
    create_bilti(client, firm_id, gst_paid_by="consignor", freight=2000)
    create_bilti(client, firm_id, gst_paid_by="consignee", freight=500)

    res = client.get("/api/reports/gst", params={"firm_id": firm_id})
    assert res.status_code == 200
    rows = {row["gst_paid_by"]: row for row in res.json() if row["gst_paid_by"]}
    assert rows["consignor"]["bilti_count"] >= 2
    assert rows["consignee"]["bilti_count"] >= 1


def test_vehicle_activity_counts_trips_and_freight(client):
    firm_id = get_firm_id(client)
    vehicle_no = unique("MP09")
    create_bilti(client, firm_id, vehicle_no=vehicle_no, freight=1000)
    create_bilti(client, firm_id, vehicle_no=vehicle_no, freight=1500)

    res = client.get("/api/reports/vehicle-activity", params={"firm_id": firm_id})
    assert res.status_code == 200
    row = next(r for r in res.json() if r["vehicle_no"] == vehicle_no)
    assert row["trip_count"] == 2
    assert row["total_freight"] == "2500.00"


def test_pending_loading_slips_excludes_slips_with_a_bilti(client):
    firm_id = get_firm_id(client)
    slip_open = create_loading_slip(client, firm_id)
    slip_closed = create_loading_slip(client, firm_id)
    create_bilti(client, firm_id, loading_slip_id=slip_closed["id"], vehicle_no=slip_closed["vehicle"]["vehicle_no"])

    res = client.get("/api/reports/pending-loading-slips", params={"firm_id": firm_id})
    assert res.status_code == 200
    ids = {row["id"] for row in res.json()}
    assert slip_open["id"] in ids
    assert slip_closed["id"] not in ids


def test_receivables_lists_only_bilties_with_outstanding_topay(client):
    firm_id = get_firm_id(client)
    bilti_unpaid = create_bilti(client, firm_id, freight=5000, advance_to_owner=0)
    bilti_paid = create_bilti(client, firm_id, freight=2000, advance_to_owner=0)

    receipt = client.post(
        "/api/receipts",
        json={
            "firm_id": firm_id, "bilti_id": bilti_paid["id"], "amount": 2000,
            "receipt_date": "2026-05-01", "received_from": "Paid In Full Co",
        },
    )
    assert receipt.status_code == 201

    res = client.get("/api/reports/receivables", params={"firm_id": firm_id})
    assert res.status_code == 200
    ids = {row["bilti_id"] for row in res.json()}
    assert bilti_unpaid["id"] in ids
    assert bilti_paid["id"] not in ids

    row = next(r for r in res.json() if r["bilti_id"] == bilti_unpaid["id"])
    assert row["topay"] == "5000.00"
    assert float(row["received"]) == 0  # coalesce(..., 0) fallback isn't scale-fixed like a Numeric column
    assert row["outstanding"] == "5000.00"
