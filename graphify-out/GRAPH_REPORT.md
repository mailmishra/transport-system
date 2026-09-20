# Graph Report - transport-system  (2026-09-19)

## Corpus Check
- Corpus is ~630 words - fits in a single context window. You may not need a graph.

## Summary
- 39 nodes · 46 edges · 7 communities (5 shown, 2 thin omitted)
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.94)
- Token cost: 45,000 input · 9,000 output

## Community Hubs (Navigation)
- Ledger & Accounting Flow
- Navigation & Reporting
- PWA Manifest Config
- Bilti / Loading Slip Forms
- Configured Transport Firms
- Project Overview

## God Nodes (most connected - your core abstractions)
1. `show(name)` - 11 edges
2. `state (localStorage-backed app state object)` - 7 edges
3. `Bilti / GR (workflow step)` - 5 edges
4. `Agent/Dalal Ledger (workflow step)` - 4 edges
5. `Truck Owner Ledger (workflow step)` - 3 edges
6. `Final Receipt (workflow step)` - 3 edges
7. `FD - Freight Difference (hidden accounting field)` - 3 edges
8. `biltiForm()` - 3 edges
9. `addBilti()` - 3 edges
10. `agentLedger()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Transport System Repository Purpose` --conceptually_related_to--> `Transport Management Software Starter PWA`  [INFERRED]
  README.md → concept/README.txt
- `LocalStorage-only prototype limitation` --rationale_for--> `state (localStorage-backed app state object)`  [INFERRED]
  concept/README.txt → concept/index.html
- `Sri Krishna Transport Company` --shares_data_with--> `firms (array of configured firm names)`  [INFERRED]
  concept/README.txt → concept/index.html
- `Shivsakti Transport Company` --shares_data_with--> `firms (array of configured firm names)`  [INFERRED]
  concept/README.txt → concept/index.html
- `Shivam Transport Company` --shares_data_with--> `firms (array of configured firm names)`  [INFERRED]
  concept/README.txt → concept/index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Core TMS Workflow Functions (Loading through Reports)** — concept_index_loadingform, concept_index_biltiform, concept_index_agentledger, concept_index_ownerledger, concept_index_receiptform, concept_index_reports [INFERRED 0.85]
- **Documented Transport Workflow (Loading Slip to Reports)** — concept_readme_loading_slip, concept_readme_bilti_gr, concept_readme_agent_dalal_ledger, concept_readme_truck_owner_ledger, concept_readme_final_receipt, concept_readme_reports [EXTRACTED 1.00]

## Communities (7 total, 2 thin omitted)

### Community 0 - "Ledger & Accounting Flow"
Cohesion: 0.24
Nodes (9): addBilti(), addLoading(), agentLedger(), ownerLedger(), state (localStorage-backed app state object), Agent/Dalal Ledger (workflow step), FD - Freight Difference (hidden accounting field), LocalStorage-only prototype limitation (+1 more)

### Community 1 - "Navigation & Reporting"
Cohesion: 0.25
Nodes (6): firmSetup(), receiptForm(), reports(), show(name), Final Receipt (workflow step), Reports (workflow step)

### Community 2 - "PWA Manifest Config"
Cohesion: 0.25
Nodes (7): background_color, display, icons, name, short_name, start_url, theme_color

### Community 3 - "Bilti / Loading Slip Forms"
Cohesion: 0.50
Nodes (5): biltiForm(), loadingForm(), Bilti / GR (workflow step), Dalali (brokerage fee, visible on Bilti), Loading Slip (workflow step)

### Community 4 - "Configured Transport Firms"
Cohesion: 0.50
Nodes (4): firms (array of configured firm names), Shivam Transport Company, Shivsakti Transport Company, Sri Krishna Transport Company

## Knowledge Gaps
- **12 isolated node(s):** `name`, `short_name`, `start_url`, `display`, `background_color` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 18 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `show(name)` connect `Navigation & Reporting` to `Ledger & Accounting Flow`, `Bilti / Loading Slip Forms`?**
  _High betweenness centrality (0.215) - this node is a cross-community bridge._
- **Why does `state (localStorage-backed app state object)` connect `Ledger & Accounting Flow` to `Navigation & Reporting`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `reports()` connect `Navigation & Reporting` to `Ledger & Accounting Flow`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **What connects `name`, `short_name`, `start_url` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._