import pytest

pytestmark = pytest.mark.integration


def test_firms_seeded_by_migration(client):
    res = client.get("/api/firms")
    assert res.status_code == 200
    names = {f["name"] for f in res.json()}
    assert names == {
        "Sri Krishna Transport Company",
        "Shivsakti Transport Company",
        "Shivam Transport Company",
    }
