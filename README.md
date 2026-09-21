# Transport System

A transport & freight accounting system for a small group of firms (Sri Krishna,
Shivsakti, and Shivam Transport Company — Katni, Madhya Pradesh), covering the
workflow:

```
Loading Slip → Bilti/GR → Agent/Dalal Ledger → Truck Owner Ledger → Final Receipt → Reports
```

The app started as a single-file offline PWA prototype (`concept/index.html`,
storing everything in `localStorage`), then grew a real FastAPI + Postgres
backend behind it. As of this pass, the prototype is being retired in favor
of a real React frontend (`frontend/`) — the reason: `concept/index.html`
rendered every "recent records" table in full on the same page as its own
create form (no pagination, sort, or search; lookups shipped as complete
preloaded lists), which stopped scaling once there was real transaction
volume. `concept/index.html` stays in the repo for reference but is no
longer built or served.

## Architecture

One deployable service: FastAPI serves both the JSON API (under `/api`) and
the built frontend SPA (`frontend/dist/`, built in a Docker stage) from the
same process, so there's no CORS to manage and nothing extra to deploy.
Postgres is a separate managed service.

```
┌───────────────────────────────────┐
│  FastAPI (backend/app)            │
│  ├─ /api/*  → JSON API            │
│  └─ /       → frontend/dist (SPA) │
└──────────────┬─────────────────────┘
               │ asyncpg
               ▼
        ┌─────────────┐
        │  PostgreSQL │
        └─────────────┘
```

- **Backend**: FastAPI, async SQLAlchemy 2.0, Alembic migrations, Pydantic v2
  validation, Postgres. Every list endpoint (`GET /api/<resource>`) is
  paginated/searchable/sortable — `?q=`, `?sort=`, `?page=`, `?limit=` — and
  returns `{items, total, page, limit}` (see `backend/app/pagination.py`).
- **Frontend**: React + TypeScript + Vite, Tailwind + shadcn/ui-pattern
  components, TanStack Query (server state) + TanStack Table (the shared
  `DataTable`). See `frontend/README.md` for the module layout and dev
  workflow. Styled to a navy `#122A42` / gold `#C89B3C` "Freight ERP" look,
  one responsive shell rather than separate desktop/mobile apps.
- **No auth yet** — deliberately. A stub `get_current_actor()` dependency
  (`backend/app/deps.py`) and nullable `created_by` columns exist on the
  backend; the frontend routes every edit/delete affordance through one
  `can(action, resource)` helper (`frontend/src/components/permissions/`)
  that returns `true` unconditionally today, so wiring Supabase auth later
  changes one function, not every screen.

## Data model

| Table | Purpose |
|---|---|
| `firms` | The 3 configured companies, plus letterhead/bank details (address, phone, email, PAN, bank a/c) printed on the GR. Seeded by migration `0001`, letterhead fields added in `0003`. |
| `loading_slips` | First step of the workflow — vehicle/truck-owner/broker, package count, and advance given at loading time. |
| `bilties` | The core freight document — the full paper GR: freight + charge breakdown (Kanta/Bahi/Service Tax/Hamali/P.Freight), dalali, advance, the hidden `freight_difference` (FD) field, GST/E-Way Bill/Invoice Value, and an optional insurance block. |
| `agents` | Normalized Agent/Dalal identities (was free text; see migration `0002`). Doubles as the "Broker" on both forms. |
| `truck_owners` | Normalized truck owner identities. |
| `vehicles` | Normalized vehicle numbers (was free text; see migration `0003`) — reused across Loading Slip, Bilti, and the Bilti's "Palti" (alternate/transship) vehicle. |
| `agent_payments` | Settlements paid out to an agent over time. |
| `truck_owner_payments` | Settlements paid to a truck owner, optionally against a specific Bilti. |
| `receipts` | Money received from a consignee against a Bilti (replaces the old client-only Final Receipt). |

Ledger balances (Agent Ledger, Truck Owner Ledger) are **not** stored — they're
computed as `accrued (from bilties) − paid (from the payments tables)`, so
there's a single source of truth for the underlying numbers. See
`GET /api/agents/{id}/balance` and `GET /api/truck-owners/{id}/balance`.

All money columns have both a Pydantic validator (fast, friendly 422s) and a
matching DB-level `CHECK` constraint (the schema holds even if something
other than this API ever writes to it). Every relationship is a real foreign
key; deleting an agent/truck owner/loading slip/bilti with ledger history
attached is blocked (`RESTRICT`) — records are soft-deleted (`is_deleted`),
never hard-deleted, since this is accounting data.

## Repo layout

```
backend/
  app/
    main.py          # FastAPI app, mounts /api + serves frontend/dist as SPA
    config.py         # env-based settings (DATABASE_URL, CORS, future Supabase)
    db.py               # async SQLAlchemy engine/session
    deps.py              # get_db(), auth stub
    pagination.py         # shared Page[T] envelope + apply_sort()/paginate()
    models/               # SQLAlchemy ORM models
    schemas/               # Pydantic request/response schemas
    crud/                    # DB access functions
    routers/                  # FastAPI route handlers, one file per resource
  alembic/
    versions/0001_init.py       # firms, loading_slips, bilties
    versions/0002_ledgers.py     # agents, truck_owners, payments, receipts
    versions/0003_paper_form_fields.py  # vehicles; full paper GR fields
  Dockerfile                        # multi-stage: builds frontend/, then Python
frontend/                             # React SPA (see frontend/README.md)
  src/
concept/                                # retired prototype, kept for reference
  index.html
docker-compose.yml                        # local dev: postgres + backend (+ built frontend)
railway.json                                # Railway build/deploy config
```

## Local development

Requires Docker (builds both the frontend and backend in one command):

```bash
docker compose up --build
```

For frontend-only iteration with hot reload, run the Vite dev server
alongside the Dockerized backend instead — see `frontend/README.md`.

This builds the backend image, starts Postgres, runs `alembic upgrade head`
(creating and seeding the schema), and serves the app on
**http://localhost:8000** — the UI at `/`, the API at `/api/*`,
`GET /healthz` for a liveness check.

Postgres is exposed on host port `5433` (not the default `5432`, to avoid
clashing with a local Postgres install) — see `docker-compose.yml`.

To run the backend outside Docker:

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # adjust DATABASE_URL to point at a running Postgres
alembic upgrade head
uvicorn app.main:app --reload
```

## API overview

All routes are under `/api`. Full interactive docs (Swagger UI) are
available at `/api/docs` when the server is running.

Every `GET /api/<resource>` list endpoint except `/firms` (a fixed 3-row
table, deliberately unpaginated) takes `?q=` (search), `?sort=` (e.g.
`-bilti_date`, whitelisted per resource in `backend/app/pagination.py`),
`?page=`, `?limit=` (max 100, default 25), and returns `{items, total,
page, limit}` rather than a bare array.

| Resource | Routes |
|---|---|
| Firms | `GET /firms`, `PATCH /firms/{id}` (letterhead/bank details) |
| Loading Slips | `POST` `GET` `GET /{id}` `PATCH /{id}` `DELETE /{id}` `/loading-slips` |
| Bilties | same CRUD on `/bilties`, plus `GET /bilties/{id}/print` (omits the hidden `freight_difference` field) |
| Agents | `GET /agents`, `GET /agents/{id}`, `PATCH /agents/{id}`, `GET /agents/{id}/balance?firm_id=` |
| Truck Owners | same shape on `/truck-owners` |
| Vehicles | `GET /vehicles`, `GET /vehicles/{id}`, `PATCH /vehicles/{id}` |
| Agent Payments | `POST` `GET` `GET /{id}` `DELETE /{id}` on `/agent-payments` |
| Truck Owner Payments | same shape on `/truck-owner-payments` |
| Receipts | same shape on `/receipts` |

`agent_name` / `truck_owner_name` / `vehicle_no` (and `palti_vehicle_no` on
Bilti) on `POST`/`PATCH` for Loading Slips and Bilties are plain strings —
the API resolves each to an `agents`/`truck_owners`/`vehicles` row by
case/whitespace-insensitive match, creating one if it doesn't exist yet. The
UI renders these as `<input list="...">` bound to a `<datalist>` of existing
values, so they behave like a dropdown while still accepting free text — the
frontend and API never have to manage those IDs directly.

`BiltiRead`/`BiltiPrint` also expose two **computed, not stored** fields —
`grand_total` (freight + all charge-breakdown fields) and `topay`
(`grand_total − advance_to_owner`) — mirroring the paper GR's own totals
box, computed the same way ledger balances are (see below).

## Deployment (Railway)

The repo deploys as a single Railway service (this app) plus Railway's
managed Postgres plugin. Config lives in `railway.json` at the repo root
(pins the Dockerfile builder, `backend/Dockerfile` as the build target, and
`/healthz` as the healthcheck path).

1. **Push this repo to GitHub** (Railway deploys from a connected repo).
2. **Provision Postgres**: in the Railway project → *New* → *Provision
   PostgreSQL*.
3. **Add the backend service**: *New* → *GitHub Repo* → select this repo.
   Leave the root directory as `/` — the Dockerfile does
   `COPY backend/ ...` and `COPY concept/ ...` as siblings, so it needs the
   repo root as build context. `railway.json` is auto-detected from there.
4. **Wire the database in**: on the backend service → *Variables* → add
   `DATABASE_URL` = `${{Postgres.DATABASE_URL}}` (Railway's reference-variable
   syntax, resolves to the Postgres service's connection string
   automatically). Leave `PORT` unset — Railway injects it and the container
   already binds to `${PORT:-8000}`. Railway's Postgres hands out a plain
   `postgresql://` URL; `app/config.py` rewrites it to `postgresql+asyncpg://`
   automatically, so no manual editing is needed.
5. **Deploy.** The container `CMD` runs `alembic upgrade head` before
   starting `uvicorn`, so the schema is created/migrated on every deploy.
   Fine for a single instance; if this ever scales to multiple replicas,
   move the migration to Railway's pre-deploy/release-command step instead
   of the container `CMD` so parallel instances don't race each other
   running migrations at the same time.
6. **Verify**: open the generated `*.up.railway.app` URL (should serve the
   UI) and `/healthz` + `/api/firms` (should respond).

CLI alternative:

```bash
railway login
railway init                 # in repo root
railway add --plugin postgresql
railway up                   # builds & deploys using railway.json
railway variables --set DATABASE_URL='${{Postgres.DATABASE_URL}}'
```

## Testing

```bash
cd backend
python3.11 -m venv .venv   # pinned deps don't have 3.14 wheels yet; use 3.11 or 3.12
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest                     # needs Docker running - spins up a real Postgres
```

`tests/` has three layers, all against a **real Postgres** (via
[testcontainers](https://testcontainers-python.readthedocs.io/), one
container for the whole session) rather than mocks — this app's entire value
is in its constraints (FKs, CHECKs, uniqueness), and a mocked DB would let
broken constraints pass silently:

- `tests/unit/` — Pydantic validators and `Settings` (the Railway
  `postgres://` → `postgresql+asyncpg://` rewrite), no DB. Run these alone
  without Docker via `SKIP_DB_TESTS=1 pytest -m "not integration and not e2e"`.
- `tests/integration/` — one file per resource (firms, loading slips,
  bilties, agents/owners/payments/receipts), covering CRUD, validation
  (422/409), FK violations, soft-delete, and — specifically —
  `test_migration_backfill.py`, which builds an isolated DB at revision
  `0001`, inserts a legacy free-text `agent`/`truck_owner` row by hand, and
  asserts the `0002` migration backfills it into `agents`/`truck_owners`
  correctly. That test caught nothing on its own, but it's the one that
  would catch a future edit to that migration silently breaking the backfill.
- `tests/e2e/test_business_flow.py` — walks the full documented workflow
  (Loading Slip → Bilti/GR → Agent Ledger → Truck Owner Ledger → Final
  Receipt) against the running app and asserts the business facts at each
  step (FD hidden from print, ledger balances net to zero after payment,
  received equals freight), not just status codes.

All 53 tests currently pass. One thing worth knowing if you touch
`tests/conftest.py`: the `client` fixture is deliberately **session-scoped** —
an earlier per-test version reproducibly broke every other test in the whole
run (an exact alternating pass/fail pattern) due to an interaction between
`anyio`'s blocking-portal thread machinery and asyncpg when a new
portal+engine got created and torn down for every test. One portal for the
whole session avoids the create/teardown cycle that triggered it.

**Not covered**: no browser/UI test — `concept/index.html` is a thin
`fetch()` layer over this same API with no independent logic, so the API
layer is where the tests live. No CI wiring yet (nothing runs these
automatically on push) — worth adding once there's a place to run them.
