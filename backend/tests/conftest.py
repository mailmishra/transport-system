"""Session-wide test setup.

A single real Postgres container (via testcontainers) backs the whole test
session, migrated to `head` once. We deliberately do NOT mock the database --
this app's entire value is in its constraints (FKs, CHECKs, uniqueness), and
a mocked DB would let broken constraints pass silently.

Ordering matters here: `app.db` creates its SQLAlchemy engine from
`get_settings().database_url` at *import time*, and pytest imports test
modules (which import `app.main`) during collection, before any fixture
runs. So the container has to start and DATABASE_URL has to be set in
`pytest_configure`, which pytest guarantees runs before collection -- a
regular fixture would be too late.

Tests are plain sync functions using Starlette's TestClient rather than an
async client. TestClient runs the whole app on one dedicated background
thread with a single persistent event loop for its entire lifetime, which
sidesteps a real problem we hit with an async client + pytest-asyncio: the
DB engine's asyncpg connection pool binds to whatever loop first ran a
query, and pytest-asyncio's per-test loops (or async fixture chains landing
on a different loop than the test) caused intermittent
"Future attached to a different loop" failures. One stable loop for the
whole client's life avoids the class of bug entirely.
"""
import os
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parent.parent


def _run_migrations_to(revision: str = "head") -> None:
    from alembic import command
    from alembic.config import Config

    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    command.upgrade(cfg, revision)


def pytest_configure(config: pytest.Config) -> None:
    if os.environ.get("SKIP_DB_TESTS"):
        # Lets `pytest -m "not integration and not e2e"` run without Docker.
        return

    from sqlalchemy.engine.url import make_url
    from testcontainers.postgres import PostgresContainer

    container = PostgresContainer("postgres:16")
    container.start()
    config._pg_container = container  # stashed for pytest_unconfigure

    async_url = make_url(container.get_connection_url()).set(drivername="postgresql+asyncpg")
    # render_as_string(hide_password=False): str(URL) masks the password as
    # "***" by default (a safety feature for logging) - using that literally
    # as the connection string breaks every connection with InvalidPasswordError.
    os.environ["DATABASE_URL"] = async_url.render_as_string(hide_password=False)

    _run_migrations_to("head")


def pytest_unconfigure(config: pytest.Config) -> None:
    container = getattr(config, "_pg_container", None)
    if container is not None:
        container.stop()


@pytest.fixture(scope="session")
def client():
    """One TestClient (one background portal thread, one event loop, one DB
    engine) for the whole test session.

    Earlier versions of this fixture created a fresh TestClient/engine per
    test. That reproducibly broke every *other* test in the entire run
    (regardless of file, an exact alternating pattern across the whole
    session) with `asyncpg...RuntimeError: ... attached to a different
    loop`. It wasn't pytest-asyncio's loop scoping (switching to sync
    TestClient didn't fix it) or a garbage-collection race (disposing the
    engine explicitly through the portal before teardown didn't fix it
    either) - both point at anyio's blocking-portal thread machinery
    recycling something asyncpg keeps thread-affine state in, across
    successive portal create/teardown cycles. One portal for the session
    avoids create/teardown cycles entirely, which is also consistent with
    the rest of this suite already sharing one Postgres schema across tests
    rather than isolating per test.
    """
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    from starlette.testclient import TestClient

    from app.deps import get_db
    from app.main import app

    engine = create_async_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
    session_local = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with session_local() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app, base_url="http://test") as tc:
            yield tc
    finally:
        app.dependency_overrides.pop(get_db, None)


def get_firm_id(client) -> str:
    """The first seeded firm's id (`firms` is seeded by migration 0001)."""
    firms = client.get("/api/firms").json()
    return firms[0]["id"]
