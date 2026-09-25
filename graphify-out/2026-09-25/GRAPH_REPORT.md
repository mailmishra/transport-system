# Graph Report - transport-system  (2026-09-25)

## Corpus Check
- 114 files · ~41,718 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 969 nodes · 2581 edges · 74 communities (34 shown, 40 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 76 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Bilti CRUD & Models
- Agent & Session CRUD
- DB Migrations
- Frontend API Hooks
- UI Components & Forms
- Backend Routers & Alembic Env
- Python Dependencies
- Report Query Hooks
- Data Fetch Hooks
- Pagination & List Hooks
- Agent & TruckOwner Models
- Bilti API Client
- HTTP Client & Firm API
- Vehicle CRUD Stack
- Agent Payment Stack
- Receipt Stack
- Truck Owner Payment Stack
- Frontend Package Config
- TypeScript Config
- Firm CRUD
- Frontend UI Libraries
- Test DB Fixtures
- Loading Slip & Ledger Hooks
- Migration & Asyncpg Tests
- Router Pagination
- Loading Slip Tests
- Dev Build Tools
- Receipt API Client
- Railway Deploy Config
- Report Tests
- Auth Stub
- Business Flow Tests
- Misc 35
- Misc 36
- Misc 37
- Misc 38
- Misc 39
- Misc 40
- Misc 41
- Misc 44
- Misc 45
- Misc 46
- Misc 47
- Misc 48
- Misc 49
- Misc 50
- Misc 52
- Misc 53
- Misc 54
- Misc 55
- Misc 56
- Misc 57
- Misc 58
- Misc 59
- Misc 60
- Misc 67
- Misc 69
- Misc 71
- Misc 72
- Misc 73

## God Nodes (most connected - your core abstractions)
1. `rupees()` - 35 edges
2. `buildQuery()` - 31 edges
3. `react` - 30 edges
4. `useSelectedFirm()` - 29 edges
5. `cn()` - 25 edges
6. `react-router-dom` - 21 edges
7. `Firm` - 21 edges
8. `formatDate()` - 21 edges
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
- **Auth stub seam across backend and frontend** — readme_auth_stub, frontend_readme_permissions_helper, readme_fastapi_backend, readme_react_frontend [INFERRED 0.95]
- **Docker Compose full-stack local dev** — docker_compose_yml_db_service, docker_compose_yml_backend_service, docker_compose_yml_media_volume, readme_postgresql, readme_fastapi_backend [EXTRACTED 1.00]

## Communities (74 total, 40 thin omitted)

### Community 0 - "Bilti CRUD & Models"
Cohesion: 0.06
Nodes (75): ActorTrackedMixin, app_models_bilti, get_or_create_by_name(), create(), get(), list_(), AsyncSession, date (+67 more)

### Community 1 - "Agent & Session CRUD"
Cohesion: 0.07
Nodes (61): get(), list_(), AsyncSession, UUID, update(), get(), list_(), AsyncSession (+53 more)

### Community 2 - "DB Migrations"
Cohesion: 0.11
Nodes (30): alembic, app_models_base, Base, Agent, AgentPayment, ActorTrackedMixin, SoftDeleteMixin, TimestampMixin (+22 more)

### Community 3 - "Frontend API Hooks"
Cohesion: 0.08
Nodes (46): AgentPaymentListParams, AgentListParams, useAgentBalance(), useAgentSearch(), api, buildQuery(), Page, LoadingSlipListParams (+38 more)

### Community 4 - "UI Components & Forms"
Cohesion: 0.09
Nodes (39): useCreateReceipt(), AsyncCombobox(), AsyncComboboxProps, Field(), Section(), NAV_ITEMS, Button, ButtonProps (+31 more)

### Community 5 - "Backend Routers & Alembic Env"
Cohesion: 0.07
Nodes (37): app_routers, do_run_migrations(), run_migrations_online(), get_settings(), field_validator, Settings, healthz(), get (+29 more)

### Community 6 - "Python Dependencies"
Cohesion: 0.08
Nodes (40): alembic dependency, asyncpg dependency, fastapi dependency, pydantic v2 dependency, sqlalchemy dependency, uvicorn dependency, Docker Compose backend service, Docker Compose db service (postgres:16) (+32 more)

### Community 7 - "Report Query Hooks"
Cohesion: 0.10
Nodes (25): useDayBook(), useGstReport(), useOutstandingSummary(), usePendingLoadingSlips(), useVehicleActivity(), frontend_src_components_ui_tabs_tabs, TabsContent(), TabsList() (+17 more)

### Community 8 - "Data Fetch Hooks"
Cohesion: 0.12
Nodes (21): useAgent(), useAgentStatement(), useBilti(), useBiltiPrint(), useFirms(), useLoadingSlip(), useReceipt(), GstPaidBy (+13 more)

### Community 9 - "Pagination & List Hooks"
Cohesion: 0.13
Nodes (27): toQuery(), useAgentPaymentList(), useCreateAgentPayment(), useAgentList(), useUpdateAgent(), useCreateTruckOwnerPayment(), useTruckOwnerBalance(), useTruckOwnerList() (+19 more)

### Community 10 - "Agent & TruckOwner Models"
Cohesion: 0.17
Nodes (26): app_models_agent, app_models_truck_owner, _date_range(), day_book(), gst_report(), outstanding_summary(), pending_loading_slips(), AsyncSession (+18 more)

### Community 11 - "Bilti API Client"
Cohesion: 0.13
Nodes (23): BiltiListParams, toQuery(), useBiltiList(), useBiltiSearch(), useCreateBilti(), useDeleteBilti(), useUpdateBilti(), useCreateLoadingSlip() (+15 more)

### Community 12 - "HTTP Client & Firm API"
Cohesion: 0.13
Nodes (17): ApiError, request(), useUpdateFirm(), useUploadFirmLogo(), Firm, App(), PrintDocumentProps, frontend_src_index (+9 more)

### Community 13 - "Vehicle CRUD Stack"
Cohesion: 0.18
Nodes (19): app_crud, app_models_vehicle, app_schemas_vehicle, get(), list_(), AsyncSession, UUID, VehicleUpdate (+11 more)

### Community 14 - "Agent Payment Stack"
Cohesion: 0.14
Nodes (19): app_models_agent_payment, app_schemas_agent_payment, create(), get(), list_(), AgentPaymentCreate, AsyncSession, UUID (+11 more)

### Community 15 - "Receipt Stack"
Cohesion: 0.20
Nodes (19): app_models_receipt, app_schemas_receipt, create(), get(), list_(), AsyncSession, ReceiptCreate, UUID (+11 more)

### Community 16 - "Truck Owner Payment Stack"
Cohesion: 0.20
Nodes (19): app_models_truck_owner_payment, app_schemas_truck_owner_payment, create(), get(), list_(), AsyncSession, TruckOwnerPaymentCreate, UUID (+11 more)

### Community 17 - "Frontend Package Config"
Cohesion: 0.10
Nodes (20): name, private, type, version, autoprefixer, class-variance-authority, clsx, postcss (+12 more)

### Community 18 - "TypeScript Config"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+11 more)

### Community 19 - "Firm CRUD"
Cohesion: 0.20
Nodes (16): AsyncSession, update(), Firm, Base, TimestampMixin, UUIDPKMixin, list_firms(), AsyncSession (+8 more)

### Community 20 - "Frontend UI Libraries"
Cohesion: 0.11
Nodes (19): dependencies, class-variance-authority, clsx, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-dropdown-menu, @radix-ui/react-label (+11 more)

### Community 21 - "Test DB Fixtures"
Cohesion: 0.15
Nodes (14): get_db(), AsyncSession, client(), get_firm_id(), pytest_configure(), pytest_unconfigure(), Session-wide test setup. A single real Postgres container (via testcontainers)…, The first seeded firm's id (`firms` is seeded by migration 0001). (+6 more)

### Community 22 - "Loading Slip & Ledger Hooks"
Cohesion: 0.21
Nodes (9): useDeleteLoadingSlip(), useReceivables(), useTruckOwner(), useTruckOwnerStatement(), formatDate(), LoadingSlipListPage(), SORT_MAP, ReceivablesTab() (+1 more)

### Community 24 - "Migration & Asyncpg Tests"
Cohesion: 0.21
Nodes (13): asyncio, asyncpg, _fetch_backfilled(), _fetch_vehicle_backfilled(), _insert_legacy_bilti(), _insert_legacy_vehicle_bilti(), Regression test for the 0001 -> 0002 backfill specifically. Builds a…, Same regression, for the 0002 -> 0003 vehicle_no -> vehicles backfill. (+5 more)

### Community 25 - "Router Pagination"
Cohesion: 0.31
Nodes (12): Page, BaseModel, create_agent_payment(), delete_agent_payment(), get_agent_payment(), _get_or_404(), list_agent_payments(), Actor (+4 more)

### Community 27 - "Loading Slip Tests"
Cohesion: 0.24
Nodes (6): test_create_get_list_loading_slip(), test_update_and_soft_delete(), create_bilti(), create_loading_slip(), Small factories for integration tests. Tests share one Postgres…, unique()

### Community 28 - "Dev Build Tools"
Cohesion: 0.20
Nodes (10): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 29 - "Receipt API Client"
Cohesion: 0.33
Nodes (8): ReceiptListParams, toQuery(), useDeleteReceipt(), useReceiptList(), Receipt, ReceiptCreateInput, ReceiptListPage(), SORT_MAP

### Community 30 - "Railway Deploy Config"
Cohesion: 0.22
Nodes (8): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyType, $schema

### Community 33 - "Auth Stub"
Cohesion: 0.40
Nodes (5): Actor, get_current_actor(), Stub auth dependency. No auth is enforced yet. This is the single place a…, collections_abc, dataclasses

### Community 34 - "Business Flow Tests"
Cohesion: 0.33
Nodes (3): Walks the actual documented business workflow end to end against the running…, test_full_workflow(), pytest

### Community 35 - "Misc 35"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

### Community 36 - "Misc 36"
Cohesion: 0.50
Nodes (3): ref_path, vite, @vitejs/plugin-react

### Community 37 - "Misc 37"
Cohesion: 0.67
Nodes (3): pytest dev dependency, testcontainers postgres dev dependency, Testcontainers Real Postgres Testing

## Knowledge Gaps
- **127 isolated node(s):** `builder`, `dockerfilePath`, `healthcheckPath`, `healthcheckTimeout`, `restartPolicyType` (+122 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 324 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `UI Components & Forms` to `Frontend API Hooks`, `Report Query Hooks`, `Data Fetch Hooks`, `Pagination & List Hooks`, `Bilti API Client`, `HTTP Client & Firm API`, `Frontend Package Config`, `Loading Slip & Ledger Hooks`, `Receipt API Client`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `dependencies` connect `Frontend UI Libraries` to `Frontend Package Config`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `Firm` connect `Firm CRUD` to `Bilti CRUD & Models`, `DB Migrations`, `Receipt Stack`, `Truck Owner Payment Stack`, `Router Pagination`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **What connects `builder`, `dockerfilePath`, `healthcheckPath` to the rest of the system?**
  _127 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Bilti CRUD & Models` be split into smaller, more focused modules?**
  _Cohesion score 0.05658263305322129 - nodes in this community are weakly interconnected._
- **Should `Agent & Session CRUD` be split into smaller, more focused modules?**
  _Cohesion score 0.06526315789473684 - nodes in this community are weakly interconnected._
- **Should `DB Migrations` be split into smaller, more focused modules?**
  _Cohesion score 0.11475409836065574 - nodes in this community are weakly interconnected._