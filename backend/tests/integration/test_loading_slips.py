import uuid

import pytest

from tests.conftest import get_firm_id
from tests.utils import create_loading_slip, unique

pytestmark = pytest.mark.integration


def test_create_get_list_loading_slip(client):
    firm_id = get_firm_id(client)
    created = create_loading_slip(client, firm_id, vehicle_no=unique("MP20"))

    got = client.get(f"/api/loading-slips/{created['id']}")
    assert got.status_code == 200
    assert got.json()["vehicle"]["vehicle_no"] == created["vehicle"]["vehicle_no"]

    listed = client.get("/api/loading-slips", params={"firm_id": firm_id})
    assert any(x["id"] == created["id"] for x in listed.json())


def test_blank_required_field_returns_422(client):
    firm_id = get_firm_id(client)
    res = client.post(
        "/api/loading-slips",
        json={
            "firm_id": firm_id,
            "slip_date": "2026-01-15",
            "vehicle_no": "",
            "loading_point": "Katni",
            "destination": "Jabalpur",
            "goods_description": "Cement",
            "quantity_weight": "10 tons",
        },
    )
    assert res.status_code == 422


def test_unknown_firm_id_returns_422(client):
    res = client.post(
        "/api/loading-slips",
        json={
            "firm_id": str(uuid.uuid4()),
            "slip_date": "2026-01-15",
            "vehicle_no": "MP20AB0001",
            "loading_point": "Katni",
            "destination": "Jabalpur",
            "goods_description": "Cement",
            "quantity_weight": "10 tons",
        },
    )
    assert res.status_code == 422


def test_update_and_soft_delete(client):
    firm_id = get_firm_id(client)
    created = create_loading_slip(client, firm_id)

    patched = client.patch(
        f"/api/loading-slips/{created['id']}", json={"destination": "Rewa"}
    )
    assert patched.status_code == 200
    assert patched.json()["destination"] == "Rewa"

    deleted = client.delete(f"/api/loading-slips/{created['id']}")
    assert deleted.status_code == 204

    # soft-deleted: gone from the list, 404 on direct get
    listed = client.get("/api/loading-slips", params={"firm_id": firm_id})
    assert not any(x["id"] == created["id"] for x in listed.json())
    assert (client.get(f"/api/loading-slips/{created['id']}")).status_code == 404
