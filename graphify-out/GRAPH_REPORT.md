# Graph Report - transport-system  (2026-09-21)

## Corpus Check
- Corpus is ~15,298 words - fits in a single context window. You may not need a graph.

## Summary
- 506 nodes · 1364 edges · 39 communities (18 shown, 21 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 106 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Bilti/Loading Slip Schemas
- Loading Slip API & Firm Deps
- Bilti/Ledger Integration Tests
- Frontend App (index.html) & README
- DB Base Models & Engine Setup
- Migration & Config Tests
- Bilti CRUD & Router
- Loading Slip & Vehicle Models
- Agent Model & Router
- Truck Owner Model & Router
- Agent Payments
- Truck Owner Payments
- Receipts
- Alembic Migrations (0001-0003)
- README Business Docs
- Railway Deployment Config
- PWA Manifest
- Concept Prototype README
- Docker Compose (Local Dev)
- Backend Requirements
- Backend Requirements
- Dev Requirements
- Dev Requirements
- Backend Requirements
- Backend Requirements
- Backend Requirements
- Concept Prototype Notes
- Concept Prototype Notes
- Concept Prototype Notes
- Concept Prototype Notes
- Concept Prototype Notes
- README Fragment

## God Nodes (most connected - your core abstractions)
1. `get_firm_id()` - 34 edges
2. `unique()` - 26 edges
3. `create_bilti()` - 26 edges
4. `Base` - 21 edges
5. `Bilti` - 20 edges
6. `Firm` - 20 edges
7. `UUIDPKMixin` - 19 edges
8. `TimestampMixin` - 19 edges
9. `LoadingSlip` - 19 edges
10. `Agent` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Ledger Balances Computed, Not Stored` --semantically_similar_to--> `agentLedger()`  [INFERRED] [semantically similar]
  README.md → concept/index.html
- `Ledger Balances Computed, Not Stored` --semantically_similar_to--> `ownerLedger()`  [INFERRED] [semantically similar]
  README.md → concept/index.html
- `grand_total / topay Computed Fields` --semantically_similar_to--> `updateBiltiTotals()`  [INFERRED] [semantically similar]
  README.md → concept/index.html
- `truck_owners Table` --shares_data_with--> `ownerLedger()`  [INFERRED]
  README.md → concept/index.html
- `loading_slips Table` --shares_data_with--> `addLoading()`  [INFERRED]
  README.md → concept/index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Documented Transport Workflow (Loading Slip to Reports)** — concept_readme_loading_slip, concept_readme_bilti_gr, concept_readme_agent_dalal_ledger, concept_readme_truck_owner_ledger, concept_readme_final_receipt, concept_readme_reports [EXTRACTED 1.00]
- **Documented Transport Workflow Screens** — readme_workflow, concept_index_loadingform, concept_index_biltiform, concept_index_agentledger, concept_index_ownerledger, concept_index_receiptform [INFERRED 0.85]
- **Reports Dispatch Pattern** — concept_index_reports, concept_index_reportfirmwise, concept_index_reportbiltiwise, concept_index_reportparty, concept_index_reportagent, concept_index_reportfd, concept_index_reportowner, concept_index_reportlorry, concept_index_reportadvance, concept_index_reportreceipt, concept_index_reportoutstanding, concept_index_reportdaybook [EXTRACTED 1.00]
- **Fetch API Wrapper Functions** — concept_index_apirequest, concept_index_apiget, concept_index_apipost, concept_index_apipatch, concept_index_apidelete [EXTRACTED 1.00]

## Communities (39 total, 21 thin omitted)

### Community 0 - "Bilti/Loading Slip Schemas"
Cohesion: 0.07
Nodes (49): AgentRead, AgentPaymentBase, AgentPaymentRead, BaseModel, field_validator, BiltiBase, _BiltiChargeFieldsMixin, BiltiCreate (+41 more)

### Community 1 - "Loading Slip API & Firm Deps"
Cohesion: 0.09
Nodes (45): AsyncSession, update(), Actor, get_current_actor(), get_db(), AsyncSession, Stub auth dependency. No auth is enforced yet. This is the single place a…, healthz() (+37 more)

### Community 2 - "Bilti/Ledger Integration Tests"
Cohesion: 0.10
Nodes (44): client(), get_firm_id(), pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, The first seeded firm's id (`firms` is seeded by migration 0001)., One TestClient (one background portal thread, one event loop, one DB engine)…, _run_migrations_to() (+36 more)

### Community 3 - "Frontend App (index.html) & README"
Cohesion: 0.05
Nodes (42): addAgentPayment(), addBilti(), addLoading(), addOwnerPayment(), addReceipt(), agentLedger(), apiGet(), apiPatch() (+34 more)

### Community 4 - "DB Base Models & Engine Setup"
Cohesion: 0.32
Nodes (20): do_run_migrations(), run_migrations_online(), Base, Agent, AgentPayment, ActorTrackedMixin, SoftDeleteMixin, TimestampMixin (+12 more)

### Community 5 - "Migration & Config Tests"
Cohesion: 0.09
Nodes (27): asyncio, asyncpg, get_settings(), field_validator, Settings, _fetch_backfilled(), _fetch_vehicle_backfilled(), _insert_legacy_bilti() (+19 more)

### Community 6 - "Bilti CRUD & Router"
Cohesion: 0.21
Nodes (24): get_or_create_by_name(), create(), get(), list_(), AsyncSession, UUID, soft_delete(), update() (+16 more)

### Community 7 - "Loading Slip & Vehicle Models"
Cohesion: 0.15
Nodes (24): create(), get(), list_(), AsyncSession, date, UUID, soft_delete(), update() (+16 more)

### Community 8 - "Agent Model & Router"
Cohesion: 0.25
Nodes (17): get(), list_(), AsyncSession, UUID, update(), agent_balance(), get_agent(), _get_or_404() (+9 more)

### Community 9 - "Truck Owner Model & Router"
Cohesion: 0.25
Nodes (17): get(), list_(), AsyncSession, UUID, update(), _get_or_404(), get_truck_owner(), list_truck_owners() (+9 more)

### Community 10 - "Agent Payments"
Cohesion: 0.24
Nodes (15): create(), get(), list_(), AsyncSession, UUID, soft_delete(), delete_agent_payment(), get_agent_payment() (+7 more)

### Community 11 - "Truck Owner Payments"
Cohesion: 0.24
Nodes (15): create(), get(), list_(), AsyncSession, UUID, soft_delete(), delete_truck_owner_payment(), _get_or_404() (+7 more)

### Community 12 - "Receipts"
Cohesion: 0.26
Nodes (14): create(), get(), list_(), AsyncSession, UUID, soft_delete(), delete_receipt(), _get_or_404() (+6 more)

### Community 13 - "Alembic Migrations (0001-0003)"
Cohesion: 0.23
Nodes (3): alembic, sqlalchemy_dialects, typing

### Community 14 - "README Business Docs"
Cohesion: 0.18
Nodes (11): concept/index.html (Single-File PWA Frontend), Single-Service FastAPI+Static Architecture, FastAPI Backend (backend/app), Railway Deployment (single service + managed Postgres), concept/index.html Frontend PWA, No Auth Yet — Deliberate, Stubbed for Future Supabase Auth, No Browser/UI Test — API Layer Is Where Logic Lives, Session-Scoped client Fixture (avoids anyio/asyncpg portal bug) (+3 more)

### Community 15 - "Railway Deployment Config"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 16 - "PWA Manifest"
Cohesion: 0.25
Nodes (7): background_color, display, icons, name, short_name, start_url, theme_color

### Community 17 - "Concept Prototype README"
Cohesion: 0.29
Nodes (8): Agent/Dalal Ledger (workflow step), Bilti / GR (workflow step), Dalali (brokerage fee, visible on Bilti), Final Receipt (workflow step), FD - Freight Difference (hidden accounting field), Loading Slip (workflow step), Reports (workflow step), Truck Owner Ledger (workflow step)

## Knowledge Gaps
- **38 isolated node(s):** `name`, `short_name`, `start_url`, `display`, `background_color` (+33 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 126 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_db()` connect `Loading Slip API & Firm Deps` to `Agent Model & Router`, `Truck Owner Model & Router`, `Bilti/Ledger Integration Tests`, `Bilti CRUD & Router`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `Migration & Config Tests` to `Loading Slip API & Firm Deps`, `DB Base Models & Engine Setup`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Firm` connect `Loading Slip API & Firm Deps` to `DB Base Models & Engine Setup`, `Bilti CRUD & Router`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `name`, `short_name`, `start_url` to the rest of the system?**
  _38 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Bilti/Loading Slip Schemas` be split into smaller, more focused modules?**
  _Cohesion score 0.06606990622335891 - nodes in this community are weakly interconnected._
- **Should `Loading Slip API & Firm Deps` be split into smaller, more focused modules?**
  _Cohesion score 0.08646616541353383 - nodes in this community are weakly interconnected._
- **Should `Bilti/Ledger Integration Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.10168350168350168 - nodes in this community are weakly interconnected._