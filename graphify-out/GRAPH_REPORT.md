# Graph Report - transport-system  (2026-09-26)

## Corpus Check
- 150 files · ~45,013 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1034 nodes · 2706 edges · 89 communities (47 shown, 42 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 132 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8e6d329d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bilties.py
- Firm
- sqlalchemy
- buildQuery
- bilti-form-drawer.tsx
- truck_owner_payments.py
- FastAPI Backend
- bilti-print-view.tsx
- UUID
- truckOwners.ts
- routers/reports.py
- rupees
- loading-slip-form-drawer.tsx
- agent-ledger-page.tsx
- Page
- Actor
- test_schemas.py
- package.json
- compilerOptions
- loading_slips.py
- dependencies
- conftest.py
- agents.ts
- get_firm_id
- test_migration_backfill.py
- get
- utils.py
- pagination.py
- agent_payments.py
- deploy
- agents.py
- sqlalchemy_ext_asyncio
- receipts.py
- main
- receipts.ts
- truck_owners.py
- Testcontainers Real Postgres Testing
- SPA root div mount
- devDependencies
- types.ts
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
- client.ts
- AsyncCombobox component
- Session-Scoped Test Client Fixture
- main.py
- schemas/bilti.py
- vehicles.ts
- BaseModel
- field_validator
- gr-report-tab.tsx
- agentPayments.ts
- scripts
- vite.config.ts
- tailwindcss
- AsyncSession
- BiltiCreate
- BiltiUpdate
- date
- get
- agent-ledger-print-view.tsx
- truck-owner-ledger-print-view.tsx

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

## Communities (89 total, 42 thin omitted)

### Community 0 - "bilties.py"
Cohesion: 0.13
Nodes (36): Actor, app_crud, app_models_bilti, app_models_firm, app_models_loading_slip, app_schemas_bilti, create(), get() (+28 more)

### Community 1 - "Firm"
Cohesion: 0.20
Nodes (16): AsyncSession, update(), Firm, Base, TimestampMixin, UUIDPKMixin, list_firms(), AsyncSession (+8 more)

### Community 2 - "sqlalchemy"
Cohesion: 0.07
Nodes (37): alembic, app_models_agent, app_models_base, app_models_truck_owner, app_models_vehicle, do_run_migrations(), run_migrations_online(), get_settings() (+29 more)

### Community 3 - "buildQuery"
Cohesion: 0.32
Nodes (7): BiltiListParams, toQuery(), useBiltiSearch(), buildQuery(), BiltiCreateInput, BiltiPrint, BiltiUpdateInput

### Community 4 - "bilti-form-drawer.tsx"
Cohesion: 0.11
Nodes (26): fetchNextBiltiNo(), useCreateBilti(), useUpdateBilti(), AsyncCombobox(), AppShell(), NAV_ITEMS, frontend_src_components_ui_dropdown_menu_dropdownmenu, DropdownMenuContent (+18 more)

### Community 5 - "truck_owner_payments.py"
Cohesion: 0.20
Nodes (19): app_models_truck_owner_payment, app_schemas_truck_owner_payment, create(), get(), list_(), AsyncSession, TruckOwnerPaymentCreate, UUID (+11 more)

### Community 6 - "FastAPI Backend"
Cohesion: 0.08
Nodes (40): alembic dependency, asyncpg dependency, fastapi dependency, pydantic v2 dependency, sqlalchemy dependency, uvicorn dependency, Docker Compose backend service, Docker Compose db service (postgres:16) (+32 more)

### Community 7 - "bilti-print-view.tsx"
Cohesion: 0.15
Nodes (16): useBilti(), useBiltiPrint(), useFirms(), useLoadingSlip(), useReceipt(), Firm, GstPaidBy, Field() (+8 more)

### Community 8 - "UUID"
Cohesion: 0.15
Nodes (21): AgentRead, AgentPaymentBase, AgentPaymentCreate, AgentPaymentRead, BaseModel, field_validator, Shared shape for the Agent/Truck-Owner Ledger Statement PDF (Reports + PDF…, LoadingSlipRead (+13 more)

### Community 9 - "truckOwners.ts"
Cohesion: 0.19
Nodes (13): useLookupSearch(), TruckOwnerListParams, useTruckOwnerBalance(), useTruckOwnerList(), useTruckOwnerSearch(), useUpdateTruckOwner(), TruckOwner, TruckOwnerBalance (+5 more)

### Community 10 - "routers/reports.py"
Cohesion: 0.19
Nodes (24): _date_range(), day_book(), gst_report(), outstanding_summary(), pending_loading_slips(), AsyncSession, date, get (+16 more)

### Community 11 - "rupees"
Cohesion: 0.12
Nodes (21): useDayBook(), useOutstandingSummary(), useReceivables(), useVehicleActivity(), frontend_src_components_ui_tabs_tabs, TabsContent(), TabsList(), TabsTrigger() (+13 more)

### Community 12 - "loading-slip-form-drawer.tsx"
Cohesion: 0.11
Nodes (24): useAgentSearch(), ApiError, useUpdateFirm(), useUploadFirmLogo(), useCreateLoadingSlip(), useUpdateLoadingSlip(), useCreateReceipt(), Field() (+16 more)

### Community 13 - "agent-ledger-page.tsx"
Cohesion: 0.10
Nodes (42): useCreateAgentPayment(), useAgentBalance(), useBiltiList(), useDeleteBilti(), useDeleteLoadingSlip(), useDeleteReceipt(), usePendingLoadingSlips(), useCreateTruckOwnerPayment() (+34 more)

### Community 14 - "Page"
Cohesion: 0.36
Nodes (10): Page, BaseModel, _get_or_404(), get_vehicle(), list_vehicles(), AsyncSession, get, UUID (+2 more)

### Community 16 - "test_schemas.py"
Cohesion: 0.08
Nodes (31): app_schemas_loading_slip, BiltiBase, BiltiCreate, BiltiUpdate, BaseModel, field_validator, ReceiptBase, ReceiptCreate (+23 more)

### Community 17 - "package.json"
Cohesion: 0.10
Nodes (20): name, private, type, version, autoprefixer, class-variance-authority, clsx, postcss (+12 more)

### Community 18 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+11 more)

### Community 19 - "loading_slips.py"
Cohesion: 0.11
Nodes (37): ActorTrackedMixin, get_or_create_by_name(), create(), get(), list_(), AsyncSession, date, UUID (+29 more)

### Community 20 - "dependencies"
Cohesion: 0.11
Nodes (19): dependencies, class-variance-authority, clsx, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-dropdown-menu, @radix-ui/react-label (+11 more)

### Community 21 - "conftest.py"
Cohesion: 0.11
Nodes (10): pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, _run_migrations_to(), Walks the actual documented business workflow end to end against the running…, test_full_workflow(), Config, os (+2 more)

### Community 22 - "agents.ts"
Cohesion: 0.27
Nodes (9): AgentListParams, useAgentList(), useUpdateAgent(), Agent, AgentBalance, AgentStatement, AgentUpdateInput, AgentsAdminTab() (+1 more)

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
Cohesion: 0.14
Nodes (21): get(), get_or_create_by_name(), list_(), AsyncSession, UUID, get(), list_(), AsyncSession (+13 more)

### Community 29 - "agent_payments.py"
Cohesion: 0.20
Nodes (19): app_models_agent_payment, app_schemas_agent_payment, create(), get(), list_(), AgentPaymentCreate, AsyncSession, UUID (+11 more)

### Community 30 - "deploy"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 31 - "agents.py"
Cohesion: 0.21
Nodes (21): get(), list_(), AsyncSession, UUID, update(), agent_balance(), agent_statement(), get_agent() (+13 more)

### Community 32 - "sqlalchemy_ext_asyncio"
Cohesion: 0.25
Nodes (8): Actor, get_current_actor(), get_db(), AsyncSession, Stub auth dependency. No auth is enforced yet. This is the single place a…, collections_abc, dataclasses, sqlalchemy_ext_asyncio

### Community 33 - "receipts.py"
Cohesion: 0.20
Nodes (19): app_models_receipt, app_schemas_receipt, create(), get(), list_(), AsyncSession, ReceiptCreate, UUID (+11 more)

### Community 34 - "main"
Cohesion: 0.22
Nodes (15): d(), delete(), log(), main(), create_bilti(), loading_slip(), mk_bilti(), patch() (+7 more)

### Community 35 - "receipts.ts"
Cohesion: 0.40
Nodes (5): ReceiptListParams, toQuery(), useReceiptList(), Receipt, ReceiptCreateInput

### Community 36 - "truck_owners.py"
Cohesion: 0.32
Nodes (15): update(), _get_or_404(), get_truck_owner(), list_truck_owners(), AsyncSession, get, UUID, Chronological freight/advance/payment ledger with a running balance, for the… (+7 more)

### Community 37 - "Testcontainers Real Postgres Testing"
Cohesion: 0.67
Nodes (3): pytest dev dependency, testcontainers postgres dev dependency, Testcontainers Real Postgres Testing

### Community 39 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 40 - "types.ts"
Cohesion: 0.18
Nodes (15): LoadingSlipListParams, toQuery(), useLoadingSlipList(), DateRangeParams, DayBookEntry, DayBookReport, GoodsItem, GstReportRow (+7 more)

### Community 67 - "client.ts"
Cohesion: 0.21
Nodes (10): api, Page, request(), toQuery(), TruckOwnerPaymentListParams, useTruckOwnerPaymentList(), TruckOwnerPayment, TruckOwnerPaymentCreateInput (+2 more)

### Community 72 - "main.py"
Cohesion: 0.17
Nodes (11): app_routers, healthz(), get, Client-side routes (e.g. /bilti/<id>/edit) don't correspond to a real file on…, service_worker_kill_switch(), SPAStaticFiles, fastapi, fastapi_middleware_cors (+3 more)

### Community 73 - "schemas/bilti.py"
Cohesion: 0.21
Nodes (9): app_schemas_agent, app_schemas_truck_owner, app_schemas_vehicle, _BiltiChargeFieldsMixin, BiltiPrint, BiltiRead, Shared by Read/Print: the components that make up the paper GR's…, Printable view — freight_difference is deliberately excluded. FD (Freight… (+1 more)

### Community 74 - "vehicles.ts"
Cohesion: 0.43
Nodes (6): Vehicle, VehicleUpdateInput, useUpdateVehicle(), useVehicleList(), VehicleListParams, VehiclesAdminTab()

### Community 77 - "gr-report-tab.tsx"
Cohesion: 0.12
Nodes (19): useGstReport(), Button, ButtonProps, buttonVariants, csvCell(), downloadCsv(), DateRangeFilter(), DateRangeFilterProps (+11 more)

### Community 78 - "agentPayments.ts"
Cohesion: 0.33
Nodes (5): AgentPaymentListParams, toQuery(), useAgentPaymentList(), AgentPayment, AgentPaymentCreateInput

### Community 79 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

### Community 80 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_path, vite, @vitejs/plugin-react

### Community 87 - "agent-ledger-print-view.tsx"
Cohesion: 0.38
Nodes (3): useAgent(), useAgentStatement(), AgentLedgerPrintView()

### Community 88 - "truck-owner-ledger-print-view.tsx"
Cohesion: 0.38
Nodes (3): useTruckOwner(), useTruckOwnerStatement(), TruckOwnerLedgerPrintView()

## Knowledge Gaps
- **131 isolated node(s):** `LedgerStatementLine`, `DayBookEntry`, `FormValues`, `EMPTY`, `FIELD_NAMES` (+126 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 351 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `bilti-form-drawer.tsx` to `bilti-print-view.tsx`, `truckOwners.ts`, `vehicles.ts`, `rupees`, `loading-slip-form-drawer.tsx`, `gr-report-tab.tsx`, `agent-ledger-page.tsx`, `package.json`, `agents.ts`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `sqlalchemy` to `main.py`, `test_migration_backfill.py`, `main`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `Firm` connect `Firm` to `receipts.py`, `sqlalchemy`, `truck_owner_payments.py`, `loading_slips.py`, `agent_payments.py`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **What connects `LedgerStatementLine`, `DayBookEntry`, `FormValues` to the rest of the system?**
  _131 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `bilties.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1251778093883357 - nodes in this community are weakly interconnected._
- **Should `sqlalchemy` be split into smaller, more focused modules?**
  _Cohesion score 0.06848425835767608 - nodes in this community are weakly interconnected._
- **Should `bilti-form-drawer.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._