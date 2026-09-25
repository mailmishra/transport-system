# Graph Report - transport-system  (2026-09-26)

## Corpus Check
- 148 files · ~42,888 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1011 nodes · 2655 edges · 75 communities (35 shown, 40 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 134 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3867ee3b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- UUID
- agent_payments.py
- sqlalchemy
- types.ts
- loading-slip-form-drawer.tsx
- truck_owner_payments.py
- FastAPI Backend
- reports.ts
- pagination.py
- agent-ledger-page.tsx
- routers/reports.py
- App.tsx
- firm-setup-tab.tsx
- bilti-form-drawer.tsx
- receipts.py
- Actor
- AsyncSession
- package.json
- compilerOptions
- loading_slips.py
- dependencies
- conftest.py
- date
- get_firm_id
- test_migration_backfill.py
- get
- utils.py
- devDependencies
- UUID
- deploy
- test_schemas.py
- schemas/bilti.py
- loading-slip-list-page.tsx
- scripts
- vite.config.ts
- Testcontainers Real Postgres Testing
- SPA root div mount
- tailwindcss
- Settings
- crud/bilti.py
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
- schemas/receipt.py
- AsyncCombobox component
- Session-Scoped Test Client Fixture
- schemas/vehicle.py
- BaseModel
- field_validator

## God Nodes (most connected - your core abstractions)
1. `rupees()` - 35 edges
2. `buildQuery()` - 31 edges
3. `react` - 30 edges
4. `useSelectedFirm()` - 29 edges
5. `cn()` - 25 edges
6. `get_firm_id()` - 24 edges
7. `formatDate()` - 21 edges
8. `react-router-dom` - 21 edges
9. `apply_sort()` - 20 edges
10. `paginate()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `can(action, resource) permissions helper` --semantically_similar_to--> `Auth Stub Pattern`  [INFERRED] [semantically similar]
  frontend/README.md → README.md
- `test_blank_required_field_returns_422()` --calls--> `get_firm_id()`  [INFERRED]
  backend/tests/integration/test_loading_slips.py → backend/tests/conftest.py
- `test_loading_slip_requires_non_blank_fields()` --calls--> `LoadingSlipCreate`  [INFERRED]
  backend/tests/unit/test_schemas.py → backend/app/schemas/loading_slip.py
- `test_pending_loading_slips_excludes_slips_with_a_bilti()` --calls--> `create_loading_slip()`  [INFERRED]
  backend/tests/integration/test_reports.py → backend/app/routers/loading_slips.py
- `pytest dev dependency` --references--> `Testcontainers Real Postgres Testing`  [INFERRED]
  backend/requirements-dev.txt → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **End-to-end freight workflow** — readme_loading_slips_table, readme_bilties_table, readme_agent_payments_table, readme_truck_owner_payments_table, readme_receipts_table, readme_workflow [EXTRACTED 1.00]
- **Docker Compose full-stack local dev** — docker_compose_yml_db_service, docker_compose_yml_backend_service, docker_compose_yml_media_volume, readme_postgresql, readme_fastapi_backend [EXTRACTED 1.00]
- **Auth stub seam across backend and frontend** — readme_auth_stub, frontend_readme_permissions_helper, readme_fastapi_backend, readme_react_frontend [INFERRED 0.95]

## Communities (75 total, 40 thin omitted)

### Community 0 - "UUID"
Cohesion: 0.22
Nodes (21): Actor, app_models_firm, app_models_loading_slip, AsyncSession, _assert_firm_exists(), _assert_loading_slip_exists(), create_bilti(), delete_bilti() (+13 more)

### Community 1 - "agent_payments.py"
Cohesion: 0.10
Nodes (36): app_models_agent_payment, app_schemas_agent_payment, create(), get(), list_(), AgentPaymentCreate, AsyncSession, UUID (+28 more)

### Community 2 - "sqlalchemy"
Cohesion: 0.09
Nodes (30): alembic, app_models_agent, app_models_base, app_models_truck_owner, app_models_vehicle, do_run_migrations(), run_migrations_online(), get_settings() (+22 more)

### Community 3 - "types.ts"
Cohesion: 0.07
Nodes (50): AgentPaymentListParams, toQuery(), useAgentPaymentList(), AgentListParams, useAgentSearch(), api, buildQuery(), Page (+42 more)

### Community 4 - "loading-slip-form-drawer.tsx"
Cohesion: 0.09
Nodes (37): AsyncCombobox(), Field(), Section(), NAV_ITEMS, Button, ButtonProps, buttonVariants, frontend_src_components_ui_dropdown_menu_dropdownmenu (+29 more)

### Community 5 - "truck_owner_payments.py"
Cohesion: 0.20
Nodes (19): app_models_truck_owner_payment, app_schemas_truck_owner_payment, create(), get(), list_(), AsyncSession, TruckOwnerPaymentCreate, UUID (+11 more)

### Community 6 - "FastAPI Backend"
Cohesion: 0.08
Nodes (40): alembic dependency, asyncpg dependency, fastapi dependency, pydantic v2 dependency, sqlalchemy dependency, uvicorn dependency, Docker Compose backend service, Docker Compose db service (postgres:16) (+32 more)

### Community 7 - "reports.ts"
Cohesion: 0.09
Nodes (33): DateRangeParams, useDayBook(), useGstReport(), useOutstandingSummary(), usePendingLoadingSlips(), useReceivables(), useVehicleActivity(), DayBookReport (+25 more)

### Community 8 - "pagination.py"
Cohesion: 0.06
Nodes (66): app_models_bilti, get(), get_or_create_by_name(), list_(), AsyncSession, UUID, update(), get() (+58 more)

### Community 9 - "agent-ledger-page.tsx"
Cohesion: 0.13
Nodes (29): useCreateAgentPayment(), useAgentBalance(), useAgentList(), useUpdateAgent(), useCreateTruckOwnerPayment(), useTruckOwnerBalance(), useTruckOwnerList(), useUpdateTruckOwner() (+21 more)

### Community 10 - "routers/reports.py"
Cohesion: 0.10
Nodes (35): app_routers, healthz(), get, Client-side routes (e.g. /bilti/<id>/edit) don't correspond to a real file on…, service_worker_kill_switch(), SPAStaticFiles, _date_range(), day_book() (+27 more)

### Community 11 - "App.tsx"
Cohesion: 0.10
Nodes (29): useAgent(), useAgentStatement(), useBiltiPrint(), useLoadingSlip(), useReceipt(), useTruckOwner(), useTruckOwnerStatement(), GstPaidBy (+21 more)

### Community 12 - "firm-setup-tab.tsx"
Cohesion: 0.20
Nodes (13): ApiError, useFirms(), useUpdateFirm(), useUploadFirmLogo(), Firm, PrintDocumentProps, EMPTY_VALUES, FirmSetupTab() (+5 more)

### Community 13 - "bilti-form-drawer.tsx"
Cohesion: 0.13
Nodes (17): BiltiListParams, fetchNextBiltiNo(), toQuery(), useBilti(), useBiltiList(), useBiltiSearch(), useCreateBilti(), useDeleteBilti() (+9 more)

### Community 14 - "receipts.py"
Cohesion: 0.10
Nodes (35): app_models_receipt, app_schemas_receipt, create(), get(), list_(), AsyncSession, ReceiptCreate, UUID (+27 more)

### Community 17 - "package.json"
Cohesion: 0.12
Nodes (16): name, private, type, version, autoprefixer, postcss, @radix-ui/react-checkbox, @radix-ui/react-dialog (+8 more)

### Community 18 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+11 more)

### Community 19 - "loading_slips.py"
Cohesion: 0.06
Nodes (60): ActorTrackedMixin, app_crud, AsyncSession, update(), create(), get(), list_(), AsyncSession (+52 more)

### Community 20 - "dependencies"
Cohesion: 0.11
Nodes (19): dependencies, class-variance-authority, clsx, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-dropdown-menu, @radix-ui/react-label (+11 more)

### Community 21 - "conftest.py"
Cohesion: 0.12
Nodes (10): pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, _run_migrations_to(), Walks the actual documented business workflow end to end against the running…, test_pending_loading_slips_excludes_slips_with_a_bilti(), Config, os (+2 more)

### Community 23 - "get_firm_id"
Cohesion: 0.17
Nodes (28): get_firm_id(), The first seeded firm's id (`firms` is seeded by migration 0001)., Dalali is included in grand_total (user feedback #7) but not shown on print., Multi-consignor stored as newline-separated text; list and print round-trip…, GET /bilties/next-no returns the next available numeric bilti_no for the firm., next-no returns max+1 when numeric bilti_nos already exist for the firm., agent_name is required since user feedback #6. Omitting or nulling it must…, test_agent_name_is_required_at_api_level() (+20 more)

### Community 24 - "test_migration_backfill.py"
Cohesion: 0.21
Nodes (13): asyncio, asyncpg, _fetch_backfilled(), _fetch_vehicle_backfilled(), _insert_legacy_bilti(), _insert_legacy_vehicle_bilti(), Regression test for the 0001 -> 0002 backfill specifically. Builds a…, Same regression, for the 0002 -> 0003 vehicle_no -> vehicles backfill. (+5 more)

### Community 27 - "utils.py"
Cohesion: 0.27
Nodes (7): factory_name is the mill/factory where goods are loaded or delivered., test_blank_required_field_returns_422(), test_create_get_list_loading_slip(), test_factory_name_stored_and_returned(), test_update_and_soft_delete(), create_loading_slip(), Small factories for integration tests. Tests share one Postgres…

### Community 28 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 30 - "deploy"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 31 - "test_schemas.py"
Cohesion: 0.16
Nodes (21): app_schemas_bilti, app_schemas_loading_slip, BiltiCreate, _bilti_payload(), Pydantic validation - no DB needed., factory_name added for loading slip (mill/factory where goods are loaded or…, agent_name became required (user feedback #6). Blank or missing must be…, weight_per_bag defaults absent and accepts a positive decimal. (+13 more)

### Community 33 - "schemas/bilti.py"
Cohesion: 0.15
Nodes (12): app_schemas_agent, app_schemas_truck_owner, app_schemas_vehicle, BiltiBase, _BiltiChargeFieldsMixin, BiltiPrint, BiltiRead, Shared by Read/Print: the components that make up the paper GR's… (+4 more)

### Community 34 - "loading-slip-list-page.tsx"
Cohesion: 0.22
Nodes (12): LoadingSlipListParams, toQuery(), useCreateLoadingSlip(), useDeleteLoadingSlip(), useLoadingSlipList(), useUpdateLoadingSlip(), LoadingSlip, LoadingSlipCreateInput (+4 more)

### Community 35 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

### Community 36 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_path, vite, @vitejs/plugin-react

### Community 37 - "Testcontainers Real Postgres Testing"
Cohesion: 0.67
Nodes (3): pytest dev dependency, testcontainers postgres dev dependency, Testcontainers Real Postgres Testing

### Community 40 - "Settings"
Cohesion: 0.24
Nodes (9): field_validator, Settings, No DB needed - Settings is a plain Pydantic model., test_already_asyncpg_scheme_is_left_alone(), test_cors_origin_list_empty_by_default(), test_cors_origin_list_splits_and_strips(), test_plain_postgres_scheme_gets_asyncpg_driver(), test_postgresql_scheme_gets_asyncpg_driver() (+1 more)

### Community 41 - "crud/bilti.py"
Cohesion: 0.33
Nodes (11): create(), get(), list_(), AsyncSession, date, UUID, soft_delete(), update() (+3 more)

### Community 67 - "schemas/receipt.py"
Cohesion: 0.27
Nodes (7): BaseModel, field_validator, ReceiptBase, ReceiptCreate, ReceiptRead, test_receipt_amount_must_be_positive(), test_receipt_blank_remarks_becomes_none()

### Community 72 - "schemas/vehicle.py"
Cohesion: 0.67
Nodes (3): BaseModel, VehicleRead, VehicleUpdate

## Knowledge Gaps
- **127 isolated node(s):** `TruckOwnerPaymentListParams`, `PaymentFormValues`, `ReceiptListParams`, `AgentListParams`, `BiltiListParams` (+122 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 337 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `sqlalchemy` to `Settings`, `agent_payments.py`, `routers/reports.py`, `test_migration_backfill.py`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `Firm` connect `loading_slips.py` to `agent_payments.py`, `sqlalchemy`, `truck_owner_payments.py`, `receipts.py`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `react` connect `loading-slip-form-drawer.tsx` to `loading-slip-list-page.tsx`, `types.ts`, `reports.ts`, `agent-ledger-page.tsx`, `App.tsx`, `firm-setup-tab.tsx`, `bilti-form-drawer.tsx`, `package.json`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `TruckOwnerPaymentListParams`, `PaymentFormValues`, `ReceiptListParams` to the rest of the system?**
  _127 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `agent_payments.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09634146341463415 - nodes in this community are weakly interconnected._
- **Should `sqlalchemy` be split into smaller, more focused modules?**
  _Cohesion score 0.09230769230769231 - nodes in this community are weakly interconnected._
- **Should `types.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.06861239119303636 - nodes in this community are weakly interconnected._