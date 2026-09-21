# Transport System — Frontend

React + TypeScript + Vite, styled with Tailwind + shadcn/ui-pattern
components, restyled to the approved "Style B — Freight ERP" tokens (navy
`#122A42` + gold `#C89B3C`, IBM Plex Sans). TanStack Query handles all
server state; TanStack Table backs the shared `DataTable` (sort/search/
pagination hit the backend, nothing is loaded and filtered client-side).

This replaces `concept/index.html`, which is retired but kept in the repo
for reference.

## Local development

Requires Node.js 20+.

```bash
cd frontend
npm install
npm run dev          # Vite dev server on :5173, proxies /api -> :8000
```

Run the backend + Postgres alongside it (from the repo root):

```bash
docker compose up --build
```

The dev server's `/api` proxy (see `vite.config.ts`) points at
`localhost:8000`, so both can run at once without CORS configuration.

## Production build

`npm run build` outputs to `dist/`. In Docker, `backend/Dockerfile`'s
`frontend-build` stage does this automatically and FastAPI serves the
result — see `backend/app/main.py`'s `SPAStaticFiles` mount, which falls
back to `index.html` for any unmatched client-side route (e.g.
`/bilti/<id>/edit`) so deep-link refreshes work.

## Structure

```
src/
  api/            typed fetch client per resource + TanStack Query hooks
  components/
    shell/         AppShell -- one responsive component (navy top bar +
                    horizontal tabs on desktop, bottom tab bar + FAB on
                    mobile), not two separate apps
    ui/            shadcn/ui-pattern primitives (button, input, sheet, ...)
    data-table/     shared DataTable: every list screen reuses this one
                     component for server-side sort/search/pagination
    combobox/       AsyncCombobox -- debounced GET .../?q= lookup,
                     replaces the old <datalist> (didn't scale)
    permissions/    can(action, resource) -- stub returns true everywhere
                     today; the seam for when Supabase auth lands
  modules/
    bilti/          List, create/edit drawer, print/PDF view -- Phase 1
    coming-soon.tsx Phase 2 placeholder for the remaining modules
```

## Status

**Phase 1 (this pass):** shared shell + the Bilti/GR module end-to-end
(paginated/searchable/sortable list, create/edit with async lookups,
print/PDF, edit/delete wired to the existing PATCH/DELETE endpoints).

**Phase 2 (not built yet):** the same pattern applied to Loading Slips,
Agent Ledger, Truck Owner Ledger, Receipts, Reports, and Firm Setup, plus
admin screens for Agent/Truck Owner/Vehicle (rename/deactivate).
