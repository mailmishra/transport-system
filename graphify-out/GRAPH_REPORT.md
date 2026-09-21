# Graph Report - transport-system  (2026-09-21)

## Corpus Check
- 1 files · ~16,074 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 526 nodes · 1402 edges · 48 communities (26 shown, 22 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.94)
- Token cost: 84,490 input · 0 output

## Community Hubs (Navigation)
- Pydantic Schema Layer
- Backend Test Setup
- Bilti CRUD Layer
- Agent Payment & Firm CRUD
- DB Models & Migration Runner
- Loading Slip CRUD/Router
- Receipt CRUD/Router
- Vehicle CRUD & App Entry
- Agent CRUD/Router
- Truck Owner CRUD/Router
- Truck Owner Payment CRUD/Router
- Migration Backfill Regression Tests
- Settings & Config Tests
- Concept App: Bilti/Loading Create Flow
- Concept App: Reports Suite
- Alembic Migration Scripts
- Concept App: Form Validation & API Client
- Ledger Screens & Get-or-Create Testing Strategy
- Railway Deploy Config
- Concept App: Print/Letterhead Views
- Hidden Freight Difference (FD) Feature
- PWA Manifest
- Business Workflow Steps
- Concept App: Screen Router & Datalists
- System Architecture Overview
- Concept App: Owner Payments
- Docker Compose Services
- Alembic Migrations (concept node)
- asyncpg dependency
- pytest dependency
- testcontainers dependency
- FastAPI dependency
- Pydantic v2 dependency
- async SQLAlchemy 2.0 dependency
- Prototype SPA (legacy concept)
- LocalStorage Limitation Note
- Shivam Transport Company (seed firm)
- Shivsakti Transport Company (seed firm)
- Sri Krishna Transport Company (seed firm)
- PWA Starter Manifest Note
- firms DB table

## God Nodes (most connected - your core abstractions)
1. `get_firm_id()` - 34 edges
2. `create_bilti()` - 26 edges
3. `unique()` - 26 edges
4. `Base` - 21 edges
5. `Firm` - 20 edges
6. `Bilti` - 20 edges
7. `TimestampMixin` - 19 edges
8. `UUIDPKMixin` - 19 edges
9. `LoadingSlip` - 19 edges
10. `Agent` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Ledger Balances Computed, Not Stored` --semantically_similar_to--> `Agent / Dalal Ledger screen`  [INFERRED] [semantically similar]
  README.md → concept/index.html
- `grand_total / topay Computed Fields` --semantically_similar_to--> `updateBiltiTotals()`  [INFERRED] [semantically similar]
  README.md → concept/index.html
- `Ledger Balances Computed, Not Stored` --semantically_similar_to--> `Truck Owner Ledger screen`  [INFERRED] [semantically similar]
  README.md → concept/index.html
- `agent_payments Table` --shares_data_with--> `addAgentPayment()`  [INFERRED]
  README.md → concept/index.html
- `agents Table` --shares_data_with--> `Agent / Dalal Ledger screen`  [INFERRED]
  README.md → concept/index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Documented Transport Workflow (Loading Slip to Reports)** — concept_readme_loading_slip, concept_readme_bilti_gr, concept_readme_agent_dalal_ledger, concept_readme_truck_owner_ledger, concept_readme_final_receipt, concept_readme_reports [EXTRACTED 1.00]
- **Firm-scoped create-and-print form submission pattern** — concept_index_addloading, concept_index_addbilti, concept_index_addagentpayment, concept_index_addownerpayment, concept_index_addreceipt, concept_index_savefirmdetails [INFERRED 0.85]
- **Fetch-then-render printable letterhead document pattern** — concept_index_printloadingslip, concept_index_printbilti, concept_index_printreceipt, concept_index_loadingslipprintview, concept_index_biltiprintview, concept_index_receiptprintview [INFERRED 0.85]
- **REPORTS registry driving pluggable report views** — concept_index_reports, concept_index_showreport, concept_index_reporttable, concept_index_reportfirmwise, concept_index_reportbiltiwise, concept_index_reportparty, concept_index_reportagent, concept_index_reportfd, concept_index_reportowner, concept_index_reportlorry, concept_index_reportadvance, concept_index_reportreceipt, concept_index_reportoutstanding, concept_index_reportdaybook [EXTRACTED 1.00]

## Communities (48 total, 22 thin omitted)

### Community 0 - "Pydantic Schema Layer"
Cohesion: 0.08
Nodes (42): AgentRead, AgentPaymentBase, AgentPaymentRead, BaseModel, field_validator, BiltiBase, _BiltiChargeFieldsMixin, BiltiCreate (+34 more)

### Community 1 - "Backend Test Setup"
Cohesion: 0.12
Nodes (41): get_firm_id(), pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, The first seeded firm's id (`firms` is seeded by migration 0001)., _run_migrations_to(), Walks the actual documented business workflow end to end against the running…, test_full_workflow() (+33 more)

### Community 2 - "Bilti CRUD Layer"
Cohesion: 0.12
Nodes (34): get_or_create_by_name(), create(), get(), list_(), AsyncSession, UUID, soft_delete(), update() (+26 more)

### Community 3 - "Agent Payment & Firm CRUD"
Cohesion: 0.12
Nodes (30): create(), get(), list_(), AsyncSession, UUID, soft_delete(), AsyncSession, update() (+22 more)

### Community 4 - "DB Models & Migration Runner"
Cohesion: 0.31
Nodes (21): do_run_migrations(), run_migrations_online(), get_settings(), Base, Agent, AgentPayment, ActorTrackedMixin, SoftDeleteMixin (+13 more)

### Community 5 - "Loading Slip CRUD/Router"
Cohesion: 0.18
Nodes (25): create(), get(), list_(), AsyncSession, date, UUID, soft_delete(), update() (+17 more)

### Community 6 - "Receipt CRUD/Router"
Cohesion: 0.17
Nodes (21): create(), get(), list_(), AsyncSession, UUID, soft_delete(), create_receipt(), delete_receipt() (+13 more)

### Community 7 - "Vehicle CRUD & App Entry"
Cohesion: 0.15
Nodes (20): get(), list_(), AsyncSession, UUID, update(), healthz(), get, _get_or_404() (+12 more)

### Community 8 - "Agent CRUD/Router"
Cohesion: 0.25
Nodes (17): get(), list_(), AsyncSession, UUID, update(), agent_balance(), get_agent(), _get_or_404() (+9 more)

### Community 9 - "Truck Owner CRUD/Router"
Cohesion: 0.25
Nodes (17): get(), list_(), AsyncSession, UUID, update(), _get_or_404(), get_truck_owner(), list_truck_owners() (+9 more)

### Community 10 - "Truck Owner Payment CRUD/Router"
Cohesion: 0.24
Nodes (17): create(), get(), list_(), AsyncSession, UUID, soft_delete(), create_truck_owner_payment(), delete_truck_owner_payment() (+9 more)

### Community 11 - "Migration Backfill Regression Tests"
Cohesion: 0.17
Nodes (15): asyncio, asyncpg, _fetch_backfilled(), _fetch_vehicle_backfilled(), _insert_legacy_bilti(), _insert_legacy_vehicle_bilti(), Regression test for the 0001 -> 0002 backfill specifically. Builds a…, Same regression, for the 0002 -> 0003 vehicle_no -> vehicles backfill. (+7 more)

### Community 12 - "Settings & Config Tests"
Cohesion: 0.19
Nodes (11): field_validator, Settings, No DB needed - Settings is a plain Pydantic model., test_already_asyncpg_scheme_is_left_alone(), test_cors_origin_list_empty_by_default(), test_cors_origin_list_splits_and_strips(), test_plain_postgres_scheme_gets_asyncpg_driver(), test_postgresql_scheme_gets_asyncpg_driver() (+3 more)

### Community 13 - "Concept App: Bilti/Loading Create Flow"
Cohesion: 0.18
Nodes (12): addBilti(), addLoading(), Backend API: /bilties, /bilties/{id}/print, Backend API: /loading-slips, Dashboard screen, Firm-scoped document/ledger inheritance, Firm Setup screen, printBilti(id) (+4 more)

### Community 14 - "Concept App: Reports Suite"
Cohesion: 0.15
Nodes (4): reportFirmWise(), reports() — Reports screen, reportTable(title, headCells, rows, colCount), showReport(id)

### Community 15 - "Alembic Migration Scripts"
Cohesion: 0.23
Nodes (3): alembic, sqlalchemy_dialects, typing

### Community 16 - "Concept App: Form Validation & API Client"
Cohesion: 0.25
Nodes (10): addAgentPayment(), Agent / Dalal Ledger screen, Backend API: PATCH /firms/{id}, apiRequest / apiGet / apiPost / apiPatch / apiDelete (API client layer), applyFormError(e, fieldMap), Inline per-field validation (design pattern), lastErrorBanner(msg), saveFirmDetails() (+2 more)

### Community 17 - "Ledger Screens & Get-or-Create Testing Strategy"
Cohesion: 0.22
Nodes (10): Truck Owner Ledger screen, agents Table, Get-or-Create Name Resolution (agent/truck_owner/vehicle), Ledger Balances Computed, Not Stored, test_migration_backfill.py Regression Guard, No Browser/UI Test — API Layer Is Where Logic Lives, Session-Scoped client Fixture (avoids anyio/asyncpg portal bug), Testing Strategy: Real Postgres via testcontainers, no mocks (+2 more)

### Community 18 - "Railway Deploy Config"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 19 - "Concept App: Print/Letterhead Views"
Cohesion: 0.32
Nodes (8): addReceipt(), Backend API: /receipts, loadingSlipPrintView(x, firm), Printable letterhead document styling (gr-doc), printLoadingSlip(id), printReceipt(id), receiptPrintView(r, bilti, firm), receipts Table

### Community 20 - "Hidden Freight Difference (FD) Feature"
Cohesion: 0.29
Nodes (8): Bilti / GR screen, biltiPrintView(b, firm), Hidden Freight Difference (FD), reportFD(), updateBiltiTotals(), GET /bilties/{id}/print (Omits FD), grand_total / topay Computed Fields, Freight Difference (FD) Hidden Field

### Community 21 - "PWA Manifest"
Cohesion: 0.25
Nodes (7): background_color, display, icons, name, short_name, start_url, theme_color

### Community 22 - "Business Workflow Steps"
Cohesion: 0.29
Nodes (8): Agent/Dalal Ledger (workflow step), Bilti / GR (workflow step), Dalali (brokerage fee, visible on Bilti), Final Receipt (workflow step), FD - Freight Difference (hidden accounting field), Loading Slip (workflow step), Reports (workflow step), Truck Owner Ledger (workflow step)

### Community 23 - "Concept App: Screen Router & Datalists"
Cohesion: 0.29
Nodes (7): Backend API: /firms, datalists(), Datalist get-or-create UX pattern, init(), Loading Slip screen, Final Receipt screen, show(name) — screen router

### Community 24 - "System Architecture Overview"
Cohesion: 0.29
Nodes (7): Single-Service FastAPI+Static Architecture, FastAPI Backend (backend/app), Railway Deployment (single service + managed Postgres), concept/index.html Frontend PWA, No Auth Yet — Deliberate, Stubbed for Future Supabase Auth, Transport System (Project), Loading Slip → Bilti/GR → Agent Ledger → Truck Owner Ledger → Final Receipt → Reports Workflow

### Community 25 - "Concept App: Owner Payments"
Cohesion: 0.40
Nodes (5): addOwnerPayment(), Backend API: /agent-payments, Backend API: /truck-owner-payments, refreshData(), truck_owner_payments Table

## Knowledge Gaps
- **45 isolated node(s):** `builder`, `dockerfilePath`, `healthcheckPath`, `healthcheckTimeout`, `restartPolicyType` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 136 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_db()` connect `Bilti CRUD Layer` to `Backend Test Setup`, `Agent Payment & Firm CRUD`, `Loading Slip CRUD/Router`, `Receipt CRUD/Router`, `Vehicle CRUD & App Entry`, `Agent CRUD/Router`, `Truck Owner CRUD/Router`, `Truck Owner Payment CRUD/Router`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `DB Models & Migration Runner` to `Migration Backfill Regression Tests`, `Settings & Config Tests`, `Vehicle CRUD & App Entry`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `Firm` connect `Agent Payment & Firm CRUD` to `Bilti CRUD Layer`, `DB Models & Migration Runner`, `Loading Slip CRUD/Router`, `Receipt CRUD/Router`, `Truck Owner Payment CRUD/Router`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **What connects `builder`, `dockerfilePath`, `healthcheckPath` to the rest of the system?**
  _45 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Pydantic Schema Layer` be split into smaller, more focused modules?**
  _Cohesion score 0.07831677381648158 - nodes in this community are weakly interconnected._
- **Should `Backend Test Setup` be split into smaller, more focused modules?**
  _Cohesion score 0.11529411764705882 - nodes in this community are weakly interconnected._
- **Should `Bilti CRUD Layer` be split into smaller, more focused modules?**
  _Cohesion score 0.12091038406827881 - nodes in this community are weakly interconnected._