# Graph Report - transport-system  (2026-09-25)

## Corpus Check
- 147 files · ~41,913 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 974 nodes · 2569 edges · 77 communities (40 shown, 37 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b5bc8fe5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bilties.py
- agents.py
- sqlalchemy
- types.ts
- bilti-form-drawer.tsx
- seed_demo_data.py
- FastAPI Backend
- rupees
- truck_owners.py
- agent-ledger-page.tsx
- routers/reports.py
- App.tsx
- firm-setup-tab.tsx
- crud/vehicle.py
- pagination.py
- Page
- truck_owner_payments.py
- package.json
- compilerOptions
- Firm
- dependencies
- conftest.py
- cn
- test_migration_backfill.py
- agent_payments.py
- utils.py
- devDependencies
- crud/loading_slip.py
- deploy
- test_reports.py
- sqlalchemy_ext_asyncio
- pytest
- scripts
- vite.config.ts
- Testcontainers Real Postgres Testing
- SPA root div mount
- tailwindcss
- crud/bilti.py
- main.py
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
- Bilti
- AsyncCombobox component
- Session-Scoped Test Client Fixture
- loading_slips.py
- crud/agent_payment.py
- crud/truck_owner_payment.py
- BaseModel
- field_validator

## God Nodes (most connected - your core abstractions)
1. `rupees()` - 35 edges
2. `buildQuery()` - 31 edges
3. `react` - 30 edges
4. `useSelectedFirm()` - 29 edges
5. `cn()` - 25 edges
6. `Firm` - 21 edges
7. `formatDate()` - 21 edges
8. `react-router-dom` - 21 edges
9. `apply_sort()` - 20 edges
10. `paginate()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `can(action, resource) permissions helper` --semantically_similar_to--> `Auth Stub Pattern`  [INFERRED] [semantically similar]
  frontend/README.md → README.md
- `test_full_workflow()` --calls--> `create_loading_slip()`  [INFERRED]
  backend/tests/e2e/test_business_flow.py → backend/app/routers/loading_slips.py
- `test_create_get_list_loading_slip()` --calls--> `create_loading_slip()`  [INFERRED]
  backend/tests/integration/test_loading_slips.py → backend/app/routers/loading_slips.py
- `test_update_and_soft_delete()` --calls--> `create_loading_slip()`  [INFERRED]
  backend/tests/integration/test_loading_slips.py → backend/app/routers/loading_slips.py
- `test_pending_loading_slips_excludes_slips_with_a_bilti()` --calls--> `create_loading_slip()`  [INFERRED]
  backend/tests/integration/test_reports.py → backend/app/routers/loading_slips.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **End-to-end freight workflow** — readme_loading_slips_table, readme_bilties_table, readme_agent_payments_table, readme_truck_owner_payments_table, readme_receipts_table, readme_workflow [EXTRACTED 1.00]
- **Docker Compose full-stack local dev** — docker_compose_yml_db_service, docker_compose_yml_backend_service, docker_compose_yml_media_volume, readme_postgresql, readme_fastapi_backend [EXTRACTED 1.00]
- **Auth stub seam across backend and frontend** — readme_auth_stub, frontend_readme_permissions_helper, readme_fastapi_backend, readme_react_frontend [INFERRED 0.95]

## Communities (77 total, 37 thin omitted)

### Community 0 - "bilties.py"
Cohesion: 0.07
Nodes (49): app_schemas_agent, app_schemas_truck_owner, app_schemas_vehicle, _assert_firm_exists(), _assert_loading_slip_exists(), create_bilti(), delete_bilti(), get_bilti() (+41 more)

### Community 1 - "agents.py"
Cohesion: 0.14
Nodes (28): app_models_bilti, get(), list_(), AsyncSession, UUID, update(), agent_balance(), agent_statement() (+20 more)

### Community 2 - "sqlalchemy"
Cohesion: 0.10
Nodes (29): alembic, app_models_agent, app_models_base, app_models_truck_owner, app_models_vehicle, do_run_migrations(), run_migrations_online(), Base (+21 more)

### Community 3 - "types.ts"
Cohesion: 0.06
Nodes (65): AgentPaymentListParams, toQuery(), useAgentPaymentList(), AgentListParams, useAgentBalance(), useAgentList(), useAgentSearch(), useAgentStatement() (+57 more)

### Community 4 - "bilti-form-drawer.tsx"
Cohesion: 0.11
Nodes (25): useBilti(), useCreateBilti(), useUpdateBilti(), useCreateLoadingSlip(), useUpdateLoadingSlip(), ReceiptCreateInput, Field(), Section() (+17 more)

### Community 5 - "seed_demo_data.py"
Cohesion: 0.12
Nodes (24): get_settings(), field_validator, Settings, d(), delete(), log(), main(), create_bilti() (+16 more)

### Community 6 - "FastAPI Backend"
Cohesion: 0.08
Nodes (40): alembic dependency, asyncpg dependency, fastapi dependency, pydantic v2 dependency, sqlalchemy dependency, uvicorn dependency, Docker Compose backend service, Docker Compose db service (postgres:16) (+32 more)

### Community 7 - "rupees"
Cohesion: 0.10
Nodes (32): DateRangeParams, useDayBook(), useGstReport(), useOutstandingSummary(), usePendingLoadingSlips(), useReceivables(), useVehicleActivity(), LoadingSlip (+24 more)

### Community 8 - "truck_owners.py"
Cohesion: 0.16
Nodes (25): get(), list_(), AsyncSession, UUID, update(), _get_or_404(), get_truck_owner(), list_truck_owners() (+17 more)

### Community 9 - "agent-ledger-page.tsx"
Cohesion: 0.13
Nodes (35): useCreateAgentPayment(), useUpdateAgent(), useBiltiList(), useDeleteBilti(), useDeleteLoadingSlip(), useDeleteReceipt(), useCreateTruckOwnerPayment(), Agent (+27 more)

### Community 10 - "routers/reports.py"
Cohesion: 0.19
Nodes (24): _date_range(), day_book(), gst_report(), outstanding_summary(), pending_loading_slips(), AsyncSession, date, get (+16 more)

### Community 11 - "App.tsx"
Cohesion: 0.13
Nodes (13): useAgent(), useCreateReceipt(), useTruckOwner(), App(), AdminPage(), AgentLedgerPage(), AgentLedgerPrintView(), DashboardPage() (+5 more)

### Community 12 - "firm-setup-tab.tsx"
Cohesion: 0.09
Nodes (29): useBiltiPrint(), ApiError, request(), useFirms(), useUpdateFirm(), useUploadFirmLogo(), useLoadingSlip(), useReceipt() (+21 more)

### Community 13 - "crud/vehicle.py"
Cohesion: 0.25
Nodes (14): get(), list_(), AsyncSession, UUID, VehicleUpdate, update(), _get_or_404(), get_vehicle() (+6 more)

### Community 14 - "pagination.py"
Cohesion: 0.14
Nodes (19): app_models_receipt, app_schemas_receipt, create(), get(), list_(), AsyncSession, ReceiptCreate, UUID (+11 more)

### Community 15 - "Page"
Cohesion: 0.31
Nodes (12): Page, BaseModel, create_receipt(), delete_receipt(), _get_or_404(), get_receipt(), list_receipts(), Actor (+4 more)

### Community 16 - "truck_owner_payments.py"
Cohesion: 0.38
Nodes (10): create_truck_owner_payment(), delete_truck_owner_payment(), _get_or_404(), get_truck_owner_payment(), list_truck_owner_payments(), Actor, AsyncSession, get (+2 more)

### Community 17 - "package.json"
Cohesion: 0.11
Nodes (18): name, private, type, version, autoprefixer, class-variance-authority, clsx, postcss (+10 more)

### Community 18 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+11 more)

### Community 19 - "Firm"
Cohesion: 0.20
Nodes (16): AsyncSession, update(), Firm, Base, TimestampMixin, UUIDPKMixin, list_firms(), AsyncSession (+8 more)

### Community 20 - "dependencies"
Cohesion: 0.11
Nodes (19): dependencies, class-variance-authority, clsx, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-dropdown-menu, @radix-ui/react-label (+11 more)

### Community 21 - "conftest.py"
Cohesion: 0.15
Nodes (14): get_db(), AsyncSession, client(), get_firm_id(), pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, The first seeded firm's id (`firms` is seeded by migration 0001). (+6 more)

### Community 22 - "cn"
Cohesion: 0.14
Nodes (18): AsyncCombobox(), AsyncComboboxProps, AppShell(), NAV_ITEMS, frontend_src_components_ui_dropdown_menu_dropdownmenu, DropdownMenuContent, DropdownMenuItem, frontend_src_components_ui_dropdown_menu_dropdownmenutrigger (+10 more)

### Community 24 - "test_migration_backfill.py"
Cohesion: 0.21
Nodes (13): asyncio, asyncpg, _fetch_backfilled(), _fetch_vehicle_backfilled(), _insert_legacy_bilti(), _insert_legacy_vehicle_bilti(), Regression test for the 0001 -> 0002 backfill specifically. Builds a…, Same regression, for the 0002 -> 0003 vehicle_no -> vehicles backfill. (+5 more)

### Community 25 - "agent_payments.py"
Cohesion: 0.38
Nodes (10): create_agent_payment(), delete_agent_payment(), get_agent_payment(), _get_or_404(), list_agent_payments(), Actor, AgentPaymentCreate, AsyncSession (+2 more)

### Community 27 - "utils.py"
Cohesion: 0.24
Nodes (6): test_create_get_list_loading_slip(), test_update_and_soft_delete(), create_bilti(), create_loading_slip(), Small factories for integration tests. Tests share one Postgres…, unique()

### Community 28 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 29 - "crud/loading_slip.py"
Cohesion: 0.18
Nodes (17): create(), get(), list_(), AsyncSession, date, UUID, soft_delete(), update() (+9 more)

### Community 30 - "deploy"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 33 - "sqlalchemy_ext_asyncio"
Cohesion: 0.33
Nodes (6): Actor, get_current_actor(), Stub auth dependency. No auth is enforced yet. This is the single place a…, collections_abc, dataclasses, sqlalchemy_ext_asyncio

### Community 34 - "pytest"
Cohesion: 0.33
Nodes (3): Walks the actual documented business workflow end to end against the running…, test_full_workflow(), pytest

### Community 35 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

### Community 36 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_path, vite, @vitejs/plugin-react

### Community 37 - "Testcontainers Real Postgres Testing"
Cohesion: 0.67
Nodes (3): pytest dev dependency, testcontainers postgres dev dependency, Testcontainers Real Postgres Testing

### Community 40 - "crud/bilti.py"
Cohesion: 0.27
Nodes (13): app_crud, get_or_create_by_name(), create(), get(), list_(), AsyncSession, date, UUID (+5 more)

### Community 41 - "main.py"
Cohesion: 0.17
Nodes (11): app_routers, healthz(), get, Client-side routes (e.g. /bilti/<id>/edit) don't correspond to a real file on…, service_worker_kill_switch(), SPAStaticFiles, fastapi, fastapi_middleware_cors (+3 more)

### Community 67 - "Bilti"
Cohesion: 0.33
Nodes (6): ActorTrackedMixin, Bilti, Base, SoftDeleteMixin, TimestampMixin, UUIDPKMixin

### Community 72 - "loading_slips.py"
Cohesion: 0.38
Nodes (12): _assert_firm_exists(), create_loading_slip(), delete_loading_slip(), get_loading_slip(), _get_or_404(), list_loading_slips(), Actor, AsyncSession (+4 more)

### Community 73 - "crud/agent_payment.py"
Cohesion: 0.31
Nodes (9): app_models_agent_payment, app_schemas_agent_payment, create(), get(), list_(), AgentPaymentCreate, AsyncSession, UUID (+1 more)

### Community 74 - "crud/truck_owner_payment.py"
Cohesion: 0.31
Nodes (9): app_models_truck_owner_payment, app_schemas_truck_owner_payment, create(), get(), list_(), AsyncSession, TruckOwnerPaymentCreate, UUID (+1 more)

## Knowledge Gaps
- **127 isolated node(s):** `LedgerStatementLine`, `DayBookEntry`, `FormValues`, `EMPTY`, `FIELD_NAMES` (+122 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 326 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `agent-ledger-page.tsx` to `types.ts`, `bilti-form-drawer.tsx`, `rupees`, `firm-setup-tab.tsx`, `package.json`, `cn`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `package.json`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `Firm` connect `Firm` to `bilties.py`, `sqlalchemy`, `loading_slips.py`, `Page`, `truck_owner_payments.py`, `agent_payments.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **What connects `LedgerStatementLine`, `DayBookEntry`, `FormValues` to the rest of the system?**
  _127 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `bilties.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06557377049180328 - nodes in this community are weakly interconnected._
- **Should `agents.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14204545454545456 - nodes in this community are weakly interconnected._
- **Should `sqlalchemy` be split into smaller, more focused modules?**
  _Cohesion score 0.1047065044949762 - nodes in this community are weakly interconnected._