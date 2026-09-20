# Graph Report - transport-system  (2026-09-20)

## Corpus Check
- 65 files · ~11,323 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 438 nodes · 1159 edges · 31 communities (17 shown, 14 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 76 edges (avg confidence: 0.94)
- Token cost: 60,000 input · 11,000 output

## Community Hubs (Navigation)
- Truck Owner/Firm API & Schemas
- Test Fixtures & E2E Flow
- Receipts API
- Frontend App Logic (index.html)
- DB Models & Migration Env
- App Config & Entrypoint
- Loading Slip API
- Agent Payments API
- Bilti Creation & Get-or-Create
- Truck Owner Payments API
- Agents API
- Architecture & Deployment Overview
- Alembic Migrations
- Railway Config Fields
- PWA Manifest Fields
- Business Workflow Concepts
- Testing Strategy & Rationale
- Form Helpers (v/n)
- asyncpg Dependency
- Prototype Limitation Note
- Shivam Transport Company
- Shivsakti Transport Company
- Sri Krishna Transport Company
- Project Identity (Starter PWA)

## God Nodes (most connected - your core abstractions)
1. `get_firm_id()` - 25 edges
2. `Base` - 19 edges
3. `Bilti` - 19 edges
4. `unique()` - 19 edges
5. `create_bilti()` - 18 edges
6. `UUIDPKMixin` - 17 edges
7. `TimestampMixin` - 17 edges
8. `Firm` - 17 edges
9. `LoadingSlip` - 16 edges
10. `show` - 16 edges

## Surprising Connections (you probably didn't know these)
- `agentLedger` --semantically_similar_to--> `Ledger Balances Computed, Not Stored`  [INFERRED] [semantically similar]
  concept/index.html → README.md
- `ownerLedger` --semantically_similar_to--> `Ledger Balances Computed, Not Stored`  [INFERRED] [semantically similar]
  concept/index.html → README.md
- `concept/index.html (offline PWA → API-backed SPA)` --shares_data_with--> `Single-Service FastAPI+Postgres Architecture`  [INFERRED]
  concept/index.html → README.md
- `Single-Service FastAPI+Postgres Architecture` --references--> `Alembic migrations`  [EXTRACTED]
  README.md → backend/requirements.txt
- `Single-Service FastAPI+Postgres Architecture` --references--> `FastAPI`  [EXTRACTED]
  README.md → backend/requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Documented Transport Workflow (Loading Slip to Reports)** — concept_readme_loading_slip, concept_readme_bilti_gr, concept_readme_agent_dalal_ledger, concept_readme_truck_owner_ledger, concept_readme_final_receipt, concept_readme_reports [EXTRACTED 1.00]
- **Client-Side Payment/Receipt Recording Flow** — concept_index_addagentpayment, concept_index_addownerpayment, concept_index_addreceipt, concept_index_apipost [INFERRED 0.75]
- **Ledger/Settlement Data Model Group** — readme_bilties_table, readme_agent_payments_table, readme_truck_owner_payments_table, readme_receipts_table [INFERRED 0.85]

## Communities (31 total, 14 thin omitted)

### Community 0 - "Truck Owner/Firm API & Schemas"
Cohesion: 0.09
Nodes (37): get(), list_(), AsyncSession, UUID, update(), get_db(), AsyncSession, list_firms() (+29 more)

### Community 1 - "Test Fixtures & E2E Flow"
Cohesion: 0.11
Nodes (36): client(), get_firm_id(), pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, The first seeded firm's id (`firms` is seeded by migration 0001)., One TestClient (one background portal thread, one event loop, one DB engine)…, _run_migrations_to() (+28 more)

### Community 2 - "Receipts API"
Cohesion: 0.11
Nodes (33): create(), get(), list_(), AsyncSession, UUID, soft_delete(), create_receipt(), delete_receipt() (+25 more)

### Community 3 - "Frontend App Logic (index.html)"
Cohesion: 0.08
Nodes (39): addAgentPayment, addBilti, addLoading, addOwnerPayment, addReceipt, agentLedger, apiDelete, apiGet (+31 more)

### Community 4 - "DB Models & Migration Env"
Cohesion: 0.28
Nodes (23): do_run_migrations(), run_migrations_online(), Base, Agent, AgentPayment, ActorTrackedMixin, SoftDeleteMixin, TimestampMixin (+15 more)

### Community 5 - "App Config & Entrypoint"
Cohesion: 0.08
Nodes (28): asyncio, asyncpg, get_settings(), field_validator, Settings, healthz(), get, _fetch_backfilled() (+20 more)

### Community 6 - "Loading Slip API"
Cohesion: 0.14
Nodes (29): create(), get(), list_(), AsyncSession, date, UUID, soft_delete(), update() (+21 more)

### Community 7 - "Agent Payments API"
Cohesion: 0.15
Nodes (24): create(), get(), list_(), AsyncSession, UUID, soft_delete(), Actor, get_current_actor() (+16 more)

### Community 8 - "Bilti Creation & Get-or-Create"
Cohesion: 0.20
Nodes (24): get_or_create_by_name(), create(), get(), list_(), AsyncSession, UUID, soft_delete(), update() (+16 more)

### Community 9 - "Truck Owner Payments API"
Cohesion: 0.17
Nodes (21): create(), get(), list_(), AsyncSession, UUID, soft_delete(), create_truck_owner_payment(), delete_truck_owner_payment() (+13 more)

### Community 10 - "Agents API"
Cohesion: 0.24
Nodes (17): get(), list_(), AsyncSession, UUID, update(), agent_balance(), get_agent(), _get_or_404() (+9 more)

### Community 11 - "Architecture & Deployment Overview"
Cohesion: 0.20
Nodes (10): Alembic migrations, FastAPI, Pydantic v2, async SQLAlchemy 2.0, concept/index.html (offline PWA → API-backed SPA), docker-compose backend service (backend/Dockerfile), docker-compose db service (postgres:16), Single-Service FastAPI+Postgres Architecture (+2 more)

### Community 12 - "Alembic Migrations"
Cohesion: 0.28
Nodes (3): alembic, sqlalchemy_dialects, typing

### Community 13 - "Railway Config Fields"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 14 - "PWA Manifest Fields"
Cohesion: 0.25
Nodes (7): background_color, display, icons, name, short_name, start_url, theme_color

### Community 15 - "Business Workflow Concepts"
Cohesion: 0.29
Nodes (8): Agent/Dalal Ledger (workflow step), Bilti / GR (workflow step), Dalali (brokerage fee, visible on Bilti), Final Receipt (workflow step), FD - Freight Difference (hidden accounting field), Loading Slip (workflow step), Reports (workflow step), Truck Owner Ledger (workflow step)

### Community 16 - "Testing Strategy & Rationale"
Cohesion: 0.40
Nodes (5): pytest, testcontainers[postgres], test_migration_backfill.py (guards 0002 migration backfill), Session-Scoped client Fixture (avoids anyio/asyncpg portal teardown bug), Testing Against Real Postgres (testcontainers, no mocks)

## Knowledge Gaps
- **40 isolated node(s):** `background_color`, `display`, `icons`, `name`, `short_name` (+35 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 112 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_db()` connect `Truck Owner/Firm API & Schemas` to `Test Fixtures & E2E Flow`, `Receipts API`, `Loading Slip API`, `Agent Payments API`, `Bilti Creation & Get-or-Create`, `Truck Owner Payments API`, `Agents API`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `App Config & Entrypoint` to `DB Models & Migration Env`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `Bilti` (e.g. with `get()` and `list_()`) actually correct?**
  _`Bilti` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `background_color`, `display`, `icons` to the rest of the system?**
  _40 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Truck Owner/Firm API & Schemas` be split into smaller, more focused modules?**
  _Cohesion score 0.08792270531400966 - nodes in this community are weakly interconnected._
- **Should `Test Fixtures & E2E Flow` be split into smaller, more focused modules?**
  _Cohesion score 0.11207729468599034 - nodes in this community are weakly interconnected._
- **Should `Receipts API` be split into smaller, more focused modules?**
  _Cohesion score 0.1064102564102564 - nodes in this community are weakly interconnected._