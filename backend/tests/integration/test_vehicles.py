import pytest

from tests.conftest import get_firm_id
from tests.utils import create_bilti, unique

pytestmark = pytest.mark.integration


def test_create_bilti_resolves_vehicle_by_no(client):
    firm_id = get_firm_id(client)
    vehicle_no = unique("MP20")
    created = create_bilti(client, firm_id, vehicle_no=vehicle_no)

    assert created["vehicle"]["vehicle_no"] == vehicle_no
    assert created["vehicle"]["is_active"] is True


def test_same_vehicle_no_reuses_row_case_and_whitespace_insensitively(client):
    firm_id = get_firm_id(client)
    vehicle_no = unique("MP20")
    first = create_bilti(client, firm_id, vehicle_no=vehicle_no)
    second = create_bilti(client, firm_id, vehicle_no=f"  {vehicle_no.lower()}  ")
    assert first["vehicle"]["id"] == second["vehicle"]["id"]


def test_bilti_with_palti_vehicle_no(client):
    firm_id = get_firm_id(client)
    palti_no = unique("UP65")
    created = create_bilti(client, firm_id, palti_vehicle_no=palti_no)
    assert created["palti_vehicle"]["vehicle_no"] == palti_no


def test_bilti_without_palti_vehicle_no_is_none(client):
    firm_id = get_firm_id(client)
    created = create_bilti(client, firm_id)
    assert created["palti_vehicle"] is None


def test_vehicle_appears_in_list_and_get(client):
    firm_id = get_firm_id(client)
    vehicle_no = unique("MP20")
    created = create_bilti(client, firm_id, vehicle_no=vehicle_no)
    vehicle_id = created["vehicle"]["id"]

    listed = client.get("/api/vehicles")
    assert any(v["id"] == vehicle_id for v in listed.json())

    got = client.get(f"/api/vehicles/{vehicle_id}")
    assert got.status_code == 200
    assert got.json()["vehicle_no"] == vehicle_no


def test_vehicle_can_be_renamed_via_patch(client):
    firm_id = get_firm_id(client)
    created = create_bilti(client, firm_id, vehicle_no=unique("MP20"))
    vehicle_id = created["vehicle"]["id"]

    renamed = client.patch(f"/api/vehicles/{vehicle_id}", json={"vehicle_no": "MP20ZZ9999"})
    assert renamed.status_code == 200
    assert renamed.json()["vehicle_no"] == "MP20ZZ9999"

    # the existing bilti's vehicle reference follows the rename.
    fetched = client.get(f"/api/bilties/{created['id']}")
    assert fetched.json()["vehicle"]["vehicle_no"] == "MP20ZZ9999"
