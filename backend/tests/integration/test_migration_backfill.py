"""Regression test for the 0001 -> 0002 backfill specifically.

Builds a *separate*, isolated database at revision 0001 (the pre-normalized
schema, where bilti.agent/bilti.truck_owner were free text), inserts a
legacy-shaped row directly with raw SQL the way real pre-migration data would
look, then upgrades to 0002 and asserts the backfill created the right
agents/truck_owners rows and re-pointed the bilti at them by FK - not just
that the migration runs without error.

This uses its own container (not the session-wide one from conftest.py,
which is already at `head`) because it needs to observe an intermediate
schema state.
"""
import asyncio
import os
from pathlib import Path

import asyncpg
import pytest
from sqlalchemy.engine.url import make_url
from testcontainers.postgres import PostgresContainer

pytestmark = pytest.mark.integration

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


def _upgrade_to(alembic_url: str, revision: str) -> None:
    from alembic import command
    from alembic.config import Config

    from app.config import get_settings

    previous = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = alembic_url
    get_settings.cache_clear()
    try:
        cfg = Config(str(BACKEND_DIR / "alembic.ini"))
        cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
        command.upgrade(cfg, revision)
    finally:
        if previous is not None:
            os.environ["DATABASE_URL"] = previous
        else:
            os.environ.pop("DATABASE_URL", None)
        get_settings.cache_clear()


async def _insert_legacy_bilti(asyncpg_dsn: str) -> None:
    conn = await asyncpg.connect(asyncpg_dsn)
    try:
        firm_id = await conn.fetchval("SELECT id FROM firms LIMIT 1")
        await conn.execute(
            """
            INSERT INTO bilties (
                id, firm_id, bilti_no, bilti_date, consignor, consignee,
                from_location, to_location, vehicle_no, truck_owner, agent,
                goods_description, weight, freight
            ) VALUES (
                gen_random_uuid(), $1, 'LEGACY-1', '2026-01-01', 'C1', 'C2',
                'X', 'Y', 'MP01AA0001', 'Legacy Owner', '  Legacy Agent  ',
                'Goods', '1 ton', 1000
            )
            """,
            firm_id,
        )
    finally:
        await conn.close()


async def _fetch_backfilled(asyncpg_dsn: str):
    conn = await asyncpg.connect(asyncpg_dsn)
    try:
        row = await conn.fetchrow(
            """
            SELECT a.name AS agent_name, t.name AS owner_name
            FROM bilties b
            JOIN agents a ON a.id = b.agent_id
            JOIN truck_owners t ON t.id = b.truck_owner_id
            WHERE b.bilti_no = 'LEGACY-1'
            """
        )
        cols = await conn.fetch(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'bilties'"
        )
        return row, {c["column_name"] for c in cols}
    finally:
        await conn.close()


def test_backfill_normalizes_legacy_free_text_agent_and_owner():
    # Deliberately a *sync* test: alembic's env.py calls asyncio.run()
    # internally (see backend/alembic/env.py), which raises
    # "asyncio.run() cannot be called from a running event loop" if this
    # test were `async def` under pytest-asyncio's own loop. The asyncpg
    # calls below get their own fresh loop via asyncio.run() instead.
    with PostgresContainer("postgres:16") as pg:
        url = make_url(pg.get_connection_url())
        # render_as_string(hide_password=False): str(URL) masks the password
        # as "***" by default, which would silently break these connections.
        alembic_url = url.set(drivername="postgresql+asyncpg").render_as_string(
            hide_password=False
        )
        asyncpg_dsn = url.set(drivername="postgresql").render_as_string(hide_password=False)

        _upgrade_to(alembic_url, "0001")
        asyncio.run(_insert_legacy_bilti(asyncpg_dsn))
        _upgrade_to(alembic_url, "0002")
        row, col_names = asyncio.run(_fetch_backfilled(asyncpg_dsn))

        assert row is not None, "backfill did not link the legacy bilti to agents/truck_owners"
        # trimmed, matching the backfill's `trim(agent)` / `trim(truck_owner)`
        assert row["agent_name"] == "Legacy Agent"
        assert row["owner_name"] == "Legacy Owner"

        # old free-text columns are gone
        assert "agent" not in col_names
        assert "truck_owner" not in col_names
        assert "agent_id" in col_names
        assert "truck_owner_id" in col_names
