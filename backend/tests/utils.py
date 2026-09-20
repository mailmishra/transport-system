"""Small factories for integration tests.

Tests share one Postgres container/schema for the whole session (see
conftest.py) rather than rolling back a transaction per test, since the app
manages its own sessions per request and transparent rollback wrapping isn't
worth the plumbing here. So: never assert *global* counts (other tests'
data is present), and always give unique natural keys (bilti_no, vehicle_no)
via `unique()` to avoid unique-constraint collisions between tests.
"""
import uuid


def unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_loading_slip(client, firm_id: str, **overrides) -> dict:
    payload = {
        "firm_id": firm_id,
        "slip_date": "2026-01-15",
        "vehicle_no": unique("MP20"),
        "loading_point": "Katni",
        "destination": "Jabalpur",
        "goods_description": "Cement",
        "quantity_weight": "10 tons",
    }
    payload.update(overrides)
    res = client.post("/api/loading-slips", json=payload)
    res.raise_for_status()
    return res.json()


def create_bilti(client, firm_id: str, **overrides) -> dict:
    payload = {
        "firm_id": firm_id,
        "bilti_no": unique("B"),
        "bilti_date": "2026-01-15",
        "consignor": "ABC Traders",
        "consignee": "XYZ Corp",
        "from_location": "Katni",
        "to_location": "Jabalpur",
        "vehicle_no": unique("MP20"),
        "truck_owner_name": unique("Owner"),
        "agent_name": unique("Agent"),
        "goods_description": "Cement",
        "weight": "10 tons",
        "freight": 15000,
        "dalali": 500,
        "advance_to_owner": 2000,
        "freight_difference": 750,
    }
    payload.update(overrides)
    res = client.post("/api/bilties", json=payload)
    res.raise_for_status()
    return res.json()
