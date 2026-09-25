# Graph Report - transport-system  (2026-09-26)

## Corpus Check
- 149 files · ~44,070 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1028 nodes · 2697 edges · 79 communities (37 shown, 42 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 132 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a06b9bee`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bilties.py
- main.py
- sqlalchemy
- bilti-form-drawer.tsx
- loading-slip-form-drawer.tsx
- truck_owner_payments.py
- FastAPI Backend
- agents.py
- types.ts
- routers/reports.py
- App.tsx
- firm-setup-tab.tsx
- useSelectedFirm
- crud/vehicle.py
- Actor
- test_schemas.py
- package.json
- compilerOptions
- loading_slips.py
- dependencies
- conftest.py
- agent-ledger-page.tsx
- get_firm_id
- test_migration_backfill.py
- get
- utils.py
- pagination.py
- agent_payments.py
- deploy
- sqlalchemy_ext_asyncio
- receipts.py
- buildQuery
- Testcontainers Real Postgres Testing
- SPA root div mount
- devDependencies
- formatDate
- test_reports.py
- delete
- post
- patch
- delete
- patch
- post
- patch
- delete
- patch
- post
- delete
- post
- delete
- post
- patch
- patch
- AsyncCombobox component
- Session-Scoped Test Client Fixture
- BaseModel
- field_validator
- gr-report-tab.tsx
- status-badge.tsx
- scripts
- vite.config.ts
- tailwindcss
- AsyncSession
- BiltiCreate
- BiltiUpdate
- date
- get

## God Nodes (most connected - your core abstractions)
1. `rupees()` - 37 edges
2. `buildQuery()` - 31 edges
3. `react` - 31 edges
4. `useSelectedFirm()` - 29 edges
5. `cn()` - 25 edges
6. `get_firm_id()` - 24 edges
7. `formatDate()` - 23 edges
8. `react-router-dom` - 21 edges
9. `Firm` - 19 edges
10. `apply_sort()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `can(action, resource) permissions helper` --semantically_similar_to--> `Auth Stub Pattern`  [INFERRED] [semantically similar]
  frontend/README.md → README.md
- `test_loading_slip_requires_non_blank_fields()` --calls--> `LoadingSlipCreate`  [INFERRED]
  backend/tests/unit/test_schemas.py → backend/app/schemas/loading_slip.py
- `test_full_workflow()` --calls--> `create_loading_slip()`  [INFERRED]
  backend/tests/e2e/test_business_flow.py → backend/app/routers/loading_slips.py
- `test_pending_loading_slips_excludes_slips_with_a_bilti()` --calls--> `create_loading_slip()`  [INFERRED]
  backend/tests/integration/test_reports.py → backend/app/routers/loading_slips.py
- `test_blank_required_field_returns_422()` --calls--> `get_firm_id()`  [INFERRED]
  backend/tests/integration/test_loading_slips.py → backend/tests/conftest.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **End-to-end freight workflow** — readme_loading_slips_table, readme_bilties_table, readme_agent_payments_table, readme_truck_owner_payments_table, readme_receipts_table, readme_workflow [EXTRACTED 1.00]
- **Docker Compose full-stack local dev** — docker_compose_yml_db_service, docker_compose_yml_backend_service, docker_compose_yml_media_volume, readme_postgresql, readme_fastapi_backend [EXTRACTED 1.00]
- **Auth stub seam across backend and frontend** — readme_auth_stub, frontend_readme_permissions_helper, readme_fastapi_backend, readme_react_frontend [INFERRED 0.95]

## Communities (79 total, 42 thin omitted)

### Community 0 - "bilties.py"
Cohesion: 0.14
Nodes (33): Actor, app_models_firm, app_models_loading_slip, create(), get(), list_(), AsyncSession, BiltiCreate (+25 more)

### Community 1 - "main.py"
Cohesion: 0.07
Nodes (44): app_routers, AsyncSession, update(), get_db(), AsyncSession, healthz(), get, Client-side routes (e.g. /bilti/<id>/edit) don't correspond to a real file on… (+36 more)

### Community 2 - "sqlalchemy"
Cohesion: 0.06
Nodes (47): ActorTrackedMixin, alembic, app_models_agent, app_models_base, app_models_truck_owner, app_models_vehicle, do_run_migrations(), run_migrations_online() (+39 more)

### Community 3 - "bilti-form-drawer.tsx"
Cohesion: 0.14
Nodes (18): useAgentSearch(), BiltiListParams, fetchNextBiltiNo(), useBilti(), useBiltiSearch(), useCreateBilti(), useUpdateBilti(), useLookupSearch() (+10 more)

### Community 4 - "loading-slip-form-drawer.tsx"
Cohesion: 0.10
Nodes (35): useCreateLoadingSlip(), useUpdateLoadingSlip(), AsyncCombobox(), DataTableProps, Field(), Section(), AppShell(), NAV_ITEMS (+27 more)

### Community 5 - "truck_owner_payments.py"
Cohesion: 0.20
Nodes (19): app_models_truck_owner_payment, app_schemas_truck_owner_payment, create(), get(), list_(), AsyncSession, TruckOwnerPaymentCreate, UUID (+11 more)

### Community 6 - "FastAPI Backend"
Cohesion: 0.08
Nodes (40): alembic dependency, asyncpg dependency, fastapi dependency, pydantic v2 dependency, sqlalchemy dependency, uvicorn dependency, Docker Compose backend service, Docker Compose db service (postgres:16) (+32 more)

### Community 8 - "agents.py"
Cohesion: 0.06
Nodes (67): app_schemas_agent, app_schemas_truck_owner, app_schemas_vehicle, agent_balance(), agent_statement(), get_agent(), _get_or_404(), list_agents() (+59 more)

### Community 9 - "types.ts"
Cohesion: 0.11
Nodes (29): DateRangeParams, toQuery(), TruckOwnerPaymentListParams, useCreateTruckOwnerPayment(), useTruckOwnerPaymentList(), TruckOwnerListParams, useTruckOwnerBalance(), useTruckOwnerList() (+21 more)

### Community 10 - "routers/reports.py"
Cohesion: 0.16
Nodes (27): app_models_agent_payment, app_models_bilti, app_models_receipt, _date_range(), day_book(), gst_report(), outstanding_summary(), pending_loading_slips() (+19 more)

### Community 11 - "App.tsx"
Cohesion: 0.05
Nodes (55): useAgent(), useAgentStatement(), useBiltiPrint(), useFirms(), useLoadingSlip(), useReceipt(), useDayBook(), useGstReport() (+47 more)

### Community 12 - "firm-setup-tab.tsx"
Cohesion: 0.14
Nodes (17): AgentPaymentListParams, toQuery(), useAgentPaymentList(), api, ApiError, Page, request(), useUpdateFirm() (+9 more)

### Community 13 - "useSelectedFirm"
Cohesion: 0.17
Nodes (14): toQuery(), useBiltiList(), useDeleteBilti(), Firm, PrintDocumentProps, AgentLedgerPage(), BiltiListPage(), SORT_MAP (+6 more)

### Community 14 - "crud/vehicle.py"
Cohesion: 0.23
Nodes (15): app_crud, get(), list_(), AsyncSession, UUID, VehicleUpdate, update(), _get_or_404() (+7 more)

### Community 16 - "test_schemas.py"
Cohesion: 0.10
Nodes (28): app_schemas_bilti, app_schemas_loading_slip, BiltiCreate, BaseModel, field_validator, ReceiptBase, ReceiptCreate, ReceiptRead (+20 more)

### Community 17 - "package.json"
Cohesion: 0.10
Nodes (20): name, private, type, version, autoprefixer, class-variance-authority, clsx, postcss (+12 more)

### Community 18 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+11 more)

### Community 19 - "loading_slips.py"
Cohesion: 0.20
Nodes (24): get_or_create_by_name(), create(), get(), list_(), AsyncSession, date, UUID, soft_delete() (+16 more)

### Community 20 - "dependencies"
Cohesion: 0.11
Nodes (19): dependencies, class-variance-authority, clsx, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-dropdown-menu, @radix-ui/react-label (+11 more)

### Community 21 - "conftest.py"
Cohesion: 0.11
Nodes (10): pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, _run_migrations_to(), Walks the actual documented business workflow end to end against the running…, test_full_workflow(), Config, os (+2 more)

### Community 22 - "agent-ledger-page.tsx"
Cohesion: 0.16
Nodes (18): useCreateAgentPayment(), AgentListParams, useAgentBalance(), useAgentList(), useUpdateAgent(), Agent, AgentBalance, AgentStatement (+10 more)

### Community 23 - "get_firm_id"
Cohesion: 0.17
Nodes (28): get_firm_id(), The first seeded firm's id (`firms` is seeded by migration 0001)., Dalali is stored but excluded from grand_total. topay = grand_total - advance., Multi-consignor stored as newline-separated text; list and print round-trip…, GET /bilties/next-no returns the next available numeric bilti_no for the firm., next-no returns max+1 when numeric bilti_nos already exist for the firm., agent_name is required since user feedback #6. Omitting or nulling it must…, test_agent_name_is_required_at_api_level() (+20 more)

### Community 24 - "test_migration_backfill.py"
Cohesion: 0.21
Nodes (13): asyncio, asyncpg, _fetch_backfilled(), _fetch_vehicle_backfilled(), _insert_legacy_bilti(), _insert_legacy_vehicle_bilti(), Regression test for the 0001 -> 0002 backfill specifically. Builds a…, Same regression, for the 0002 -> 0003 vehicle_no -> vehicles backfill. (+5 more)

### Community 27 - "utils.py"
Cohesion: 0.27
Nodes (7): factory_name is the mill/factory where goods are loaded or delivered., test_blank_required_field_returns_422(), test_create_get_list_loading_slip(), test_factory_name_stored_and_returned(), test_update_and_soft_delete(), create_loading_slip(), Small factories for integration tests. Tests share one Postgres…

### Community 28 - "pagination.py"
Cohesion: 0.17
Nodes (16): get(), get_or_create_by_name(), list_(), AsyncSession, UUID, update(), apply_sort(), paginate() (+8 more)

### Community 29 - "agent_payments.py"
Cohesion: 0.21
Nodes (18): app_schemas_agent_payment, create(), get(), list_(), AgentPaymentCreate, AsyncSession, UUID, soft_delete() (+10 more)

### Community 30 - "deploy"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 32 - "sqlalchemy_ext_asyncio"
Cohesion: 0.21
Nodes (11): get(), list_(), AsyncSession, UUID, update(), Actor, get_current_actor(), Stub auth dependency. No auth is enforced yet. This is the single place a… (+3 more)

### Community 33 - "receipts.py"
Cohesion: 0.19
Nodes (20): app_schemas_receipt, create(), get(), list_(), AsyncSession, ReceiptCreate, UUID, soft_delete() (+12 more)

### Community 35 - "buildQuery"
Cohesion: 0.27
Nodes (10): buildQuery(), ReceiptListParams, toQuery(), useCreateReceipt(), useDeleteReceipt(), useReceiptList(), Receipt, ReceiptCreateInput (+2 more)

### Community 37 - "Testcontainers Real Postgres Testing"
Cohesion: 0.67
Nodes (3): pytest dev dependency, testcontainers postgres dev dependency, Testcontainers Real Postgres Testing

### Community 39 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 40 - "formatDate"
Cohesion: 0.27
Nodes (9): LoadingSlipListParams, toQuery(), useDeleteLoadingSlip(), useLoadingSlipList(), LoadingSlipCreateInput, LoadingSlipUpdateInput, formatDate(), LoadingSlipListPage() (+1 more)

### Community 77 - "gr-report-tab.tsx"
Cohesion: 0.16
Nodes (13): Bilti, Vehicle, VehicleUpdateInput, useUpdateVehicle(), useVehicleList(), VehicleListParams, VehiclesAdminTab(), CSV_COLS (+5 more)

### Community 78 - "status-badge.tsx"
Cohesion: 0.40
Nodes (4): BiltiStatus, COLOR, LABEL, StatusBadge()

### Community 79 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

### Community 80 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_path, vite, @vitejs/plugin-react

## Knowledge Gaps
- **130 isolated node(s):** `Filters`, `EMPTY`, `CSV_COLS`, `FormValues`, `AgentPaymentListParams` (+125 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 347 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `dependencies` connect `dependencies` to `package.json`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `react` connect `loading-slip-form-drawer.tsx` to `bilti-form-drawer.tsx`, `buildQuery`, `formatDate`, `types.ts`, `App.tsx`, `firm-setup-tab.tsx`, `gr-report-tab.tsx`, `useSelectedFirm`, `package.json`, `agent-ledger-page.tsx`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `create_truck_owner_payment()` connect `truck_owner_payments.py` to `bilties.py`, `main.py`, `pagination.py`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **What connects `Filters`, `EMPTY`, `CSV_COLS` to the rest of the system?**
  _130 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `bilties.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13781512605042018 - nodes in this community are weakly interconnected._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06636500754147813 - nodes in this community are weakly interconnected._
- **Should `sqlalchemy` be split into smaller, more focused modules?**
  _Cohesion score 0.06046511627906977 - nodes in this community are weakly interconnected._