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


def test_agent_name_is_required_at_api_level(client):
    """agent_name is required since user feedback #6. Omitting or nulling it must return 422."""
    firm_id = get_firm_id(client)
    for bad_agent in [None, "   "]:
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
                "agent_name": bad_agent,
                "goods_description": "G",
                "weight": "1",
                "freight": 100,
            },
        )
        assert res.status_code == 422, f"expected 422 for agent_name={bad_agent!r}"


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
            "agent_name": unique("Agent"),
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
            "agent_name": unique("Agent"),
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
            "agent_name": unique("Agent"),
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
    assert not any(x["id"] == created["id"] for x in listed.json()["items"])


def test_grand_total_excludes_dalali_topay_is_net_of_advance(client):
    """Dalali is stored but excluded from grand_total. topay = grand_total - advance."""
    firm_id = get_firm_id(client)
    created = create_bilti(
        client,
        firm_id,
        freight=5000,
        dalali=200,
        other_charges=100,
        kanta_charges=50,
        bahi_charges=20,
        service_tax=30,
        hamali=260,
        p_freight=0,
        advance_to_owner=1000,
    )
    # grand_total = freight + other charges (dalali excluded)
    # 5000 + 100 + 50 + 20 + 30 + 260 + 0 = 5460
    assert created["grand_total"] == "5460.00"
    # dalali still stored and returned
    assert created["dalali"] == "200.00"
    # topay = grand_total - advance_to_owner
    assert created["topay"] == "4460.00"

    printable = client.get(f"/api/bilties/{created['id']}/print")
    assert printable.json()["grand_total"] == "5460.00"
    assert printable.json()["topay"] == "4460.00"
    assert "freight_difference" not in printable.json()


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
            "agent_name": unique("Agent"),
            "goods_description": "G",
            "weight": "1",
            "freight": 100,
            "gst_paid_by": "nobody",
        },
    )
    assert res.status_code == 422


def test_weight_per_bag_stored_and_returned(client):
    firm_id = get_firm_id(client)
    created = create_bilti(client, firm_id, weight_per_bag=0.05)
    assert created["weight_per_bag"] == "0.050"

    # omitting it gives null
    created2 = create_bilti(client, firm_id)
    assert created2["weight_per_bag"] is None


def test_consignor_accepts_multiline(client):
    """Multi-consignor stored as newline-separated text; list and print round-trip intact."""
    firm_id = get_firm_id(client)
    multi = "ABC Traders\nXYZ Mills\nPatel Roadways"
    created = create_bilti(client, firm_id, consignor=multi)
    assert created["consignor"] == multi

    # print view returns same value (rendering is front-end's job)
    printable = client.get(f"/api/bilties/{created['id']}/print").json()
    assert printable["consignor"] == multi


def test_goods_description_accepts_multiline(client):
    firm_id = get_firm_id(client)
    multi = "Cement Bags\nSteel Rods"
    created = create_bilti(client, firm_id, goods_description=multi)
    assert created["goods_description"] == multi


def test_next_bilti_no_returns_sequence(client):
    """GET /bilties/next-no returns the next available numeric bilti_no for the firm."""
    firm_id = get_firm_id(client)
    marker = unique("NextNo")
    # Create a few with numeric bilti_nos under this firm
    # Use firm-level unique marker in consignor so we can track them
    create_bilti(client, firm_id, bilti_no=unique("NNN"), consignor=marker, freight=100)

    # Create biltis with explicit numeric keys
    n_prefix = unique("NUM")
    create_bilti(client, firm_id, bilti_no=f"{n_prefix}100", freight=100)

    # next-no is per-firm; just assert it returns a non-empty string (other tests
    # may have created numeric bilti_nos already, so we can't pin the exact value)
    res = client.get("/api/bilties/next-no", params={"firm_id": firm_id})
    assert res.status_code == 200
    body = res.json()
    assert "next_no" in body
    # it must be a string representation of an integer
    assert body["next_no"].isdigit()
    # and it must be > 0
    assert int(body["next_no"]) > 0


def test_next_bilti_no_increments_past_existing(client):
    """next-no returns max+1 when numeric bilti_nos already exist for the firm."""
    firm_id = get_firm_id(client)
    # Plant a known high numeric bilti_no
    known_high = "77777"
    create_bilti(client, firm_id, bilti_no=known_high, freight=100)

    res = client.get("/api/bilties/next-no", params={"firm_id": firm_id})
    assert res.status_code == 200
    returned = int(res.json()["next_no"])
    assert returned >= 77778  # at least one past the planted value


def test_list_is_paginated_with_envelope(client):
    firm_id = get_firm_id(client)
    consignor = unique("SearchableConsignor")
    for _ in range(3):
        create_bilti(client, firm_id, consignor=consignor)

    page1 = client.get("/api/bilties", params={"firm_id": firm_id, "q": consignor, "limit": 2})
    assert page1.status_code == 200
    body = page1.json()
    assert set(body.keys()) == {"items", "total", "page", "limit"}
    assert body["total"] == 3
    assert body["page"] == 1
    assert body["limit"] == 2
    assert len(body["items"]) == 2

    page2 = client.get(
        "/api/bilties", params={"firm_id": firm_id, "q": consignor, "limit": 2, "page": 2}
    )
    assert len(page2.json()["items"]) == 1
    # no overlap between pages
    ids_p1 = {x["id"] for x in body["items"]}
    ids_p2 = {x["id"] for x in page2.json()["items"]}
    assert ids_p1.isdisjoint(ids_p2)


def test_search_q_matches_consignor_and_bilti_no(client):
    firm_id = get_firm_id(client)
    needle = unique("Vindhya")
    match_by_consignor = create_bilti(client, firm_id, consignor=needle)
    match_by_bilti_no = create_bilti(client, firm_id, bilti_no=needle)
    create_bilti(client, firm_id)  # unrelated, should not match

    found = client.get("/api/bilties", params={"firm_id": firm_id, "q": needle}).json()["items"]
    found_ids = {x["id"] for x in found}
    assert match_by_consignor["id"] in found_ids
    assert match_by_bilti_no["id"] in found_ids
    assert len(found) == 2


def test_sort_by_freight(client):
    firm_id = get_firm_id(client)
    marker = unique("SortMarker")
    low = create_bilti(client, firm_id, consignor=marker, freight=100)
    high = create_bilti(client, firm_id, consignor=marker, freight=9000)

    ascending = client.get(
        "/api/bilties", params={"firm_id": firm_id, "q": marker, "sort": "freight"}
    ).json()["items"]
    assert [x["id"] for x in ascending] == [low["id"], high["id"]]

    descending = client.get(
        "/api/bilties", params={"firm_id": firm_id, "q": marker, "sort": "-freight"}
    ).json()["items"]
    assert [x["id"] for x in descending] == [high["id"], low["id"]]
