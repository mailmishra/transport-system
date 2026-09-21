import uuid

import pytest

from tests.conftest import get_firm_id
from tests.utils import create_bilti, unique

pytestmark = pytest.mark.integration


def test_create_bilti_resolves_agent_and_truck_owner_by_name(client):
    firm_id = get_firm_id(client)
    agent_name = unique("Suresh")
    owner_name = unique("Ramesh")
    created = create_bilti(client, firm_id, agent_name=agent_name, truck_owner_name=owner_name)

    assert created["agent"]["name"] == agent_name
    assert created["truck_owner"]["name"] == owner_name
    # freight_difference is visible on the full read
    assert "freight_difference" in created


def test_same_name_reuses_agent_case_and_whitespace_insensitively(client):
    firm_id = get_firm_id(client)
    agent_name = unique("Suresh")
    first = create_bilti(client, firm_id, agent_name=agent_name)
    second = create_bilti(client, firm_id, agent_name=f"  {agent_name.upper()}  ")
    assert first["agent"]["id"] == second["agent"]["id"]


def test_bilti_without_agent_name_has_no_agent(client):
    firm_id = get_firm_id(client)
    created = create_bilti(client, firm_id, agent_name=None)
    assert created["agent"] is None


def test_freight_must_be_positive(client):
    firm_id = get_firm_id(client)
    res = client.post(
        "/api/bilties",
        json={
            "firm_id": firm_id,
            "bilti_no": unique("B"),
            "bilti_date": "2026-01-15",
            "consignor": "A",
            "consignee": "B",
            "from_location": "C",
            "to_location": "D",
            "vehicle_no": unique("MP20"),
            "truck_owner_name": unique("Owner"),
            "goods_description": "G",
            "weight": "1",
            "freight": -5,
        },
    )
    assert res.status_code == 422


def test_duplicate_bilti_no_for_same_firm_is_rejected(client):
    firm_id = get_firm_id(client)
    bilti_no = unique("B")
    create_bilti(client, firm_id, bilti_no=bilti_no)
    res = client.post(
        "/api/bilties",
        json={
            "firm_id": firm_id,
            "bilti_no": bilti_no,
            "bilti_date": "2026-01-15",
            "consignor": "A",
            "consignee": "B",
            "from_location": "C",
            "to_location": "D",
            "vehicle_no": unique("MP20"),
            "truck_owner_name": unique("Owner"),
            "goods_description": "G",
            "weight": "1",
            "freight": 100,
        },
    )
    assert res.status_code == 409


def test_same_bilti_no_allowed_across_different_firms(client):
    firms = (client.get("/api/firms")).json()
    assert len(firms) >= 2, "seed data must have >=2 firms for this test"
    bilti_no = unique("B")
    a = create_bilti(client, firms[0]["id"], bilti_no=bilti_no)
    b = create_bilti(client, firms[1]["id"], bilti_no=bilti_no)
    assert a["id"] != b["id"]


def test_unknown_loading_slip_id_returns_422(client):
    firm_id = get_firm_id(client)
    res = client.post(
        "/api/bilties",
        json={
            "firm_id": firm_id,
            "loading_slip_id": str(uuid.uuid4()),
            "bilti_no": unique("B"),
            "bilti_date": "2026-01-15",
            "consignor": "A",
            "consignee": "B",
            "from_location": "C",
            "to_location": "D",
            "vehicle_no": unique("MP20"),
            "truck_owner_name": unique("Owner"),
            "goods_description": "G",
            "weight": "1",
            "freight": 100,
        },
    )
    assert res.status_code == 422


def test_print_view_omits_freight_difference(client):
    firm_id = get_firm_id(client)
    created = create_bilti(client, firm_id, freight_difference=750)

    full = client.get(f"/api/bilties/{created['id']}")
    assert full.json()["freight_difference"] == "750.00"

    printable = client.get(f"/api/bilties/{created['id']}/print")
    assert printable.status_code == 200
    assert "freight_difference" not in printable.json()


def test_soft_deleted_bilti_hidden_from_list_and_get(client):
    firm_id = get_firm_id(client)
    created = create_bilti(client, firm_id)
    assert (client.delete(f"/api/bilties/{created['id']}")).status_code == 204
    assert (client.get(f"/api/bilties/{created['id']}")).status_code == 404
    listed = client.get("/api/bilties", params={"firm_id": firm_id})
    assert not any(x["id"] == created["id"] for x in listed.json())


def test_grand_total_and_topay_computed_from_charge_breakdown(client):
    firm_id = get_firm_id(client)
    created = create_bilti(
        client,
        firm_id,
        freight=5000,
        other_charges=100,
        kanta_charges=50,
        bahi_charges=20,
        service_tax=30,
        hamali=260,
        p_freight=0,
        advance_to_owner=1000,
    )
    # 5000 + 100 + 50 + 20 + 30 + 260 + 0
    assert created["grand_total"] == "5460.00"
    # grand_total - advance_to_owner
    assert created["topay"] == "4460.00"

    printable = client.get(f"/api/bilties/{created['id']}/print")
    assert printable.json()["grand_total"] == "5460.00"
    assert printable.json()["topay"] == "4460.00"


def test_gst_paid_by_rejects_invalid_value(client):
    firm_id = get_firm_id(client)
    res = client.post(
        "/api/bilties",
        json={
            "firm_id": firm_id,
            "bilti_no": unique("B"),
            "bilti_date": "2026-01-15",
            "consignor": "A",
            "consignee": "B",
            "from_location": "C",
            "to_location": "D",
            "vehicle_no": unique("MP20"),
            "truck_owner_name": unique("Owner"),
            "goods_description": "G",
            "weight": "1",
            "freight": 100,
            "gst_paid_by": "nobody",
        },
    )
    assert res.status_code == 422
