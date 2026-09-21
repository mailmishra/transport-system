import * as React from "react";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import { DataTable } from "@/components/data-table/data-table";
import { useAgentList, useUpdateAgent } from "@/api/agents";
import type { Agent } from "@/api/types";
import { can } from "@/components/permissions/can";

/** Rename/deactivate via a plain prompt()/confirm() rather than a full
 * drawer -- this is a low-traffic internal admin utility (Agent/TruckOwner/
 * Vehicle records are normally created implicitly via Bilti/LoadingSlip
 * get-or-create), not a screen worth a dedicated form component for.
 */
export function AgentsAdminTab() {
  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState("");
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "name", desc: false }]);
  const { data, isLoading } = useAgentList({
    q: search || undefined,
    sort: sorting[0] ? `${sorting[0].desc ? "-" : ""}name` : "name",
    page,
    limit: 20,
  });
  const updateAgent = useUpdateAgent();

  const columns = React.useMemo<ColumnDef<Agent, any>[]>(
    () => [
      { id: "name", accessorKey: "name", header: "Name", enableSorting: true },
      { id: "phone", accessorKey: "phone", header: "Phone", enableSorting: false, cell: (ctx) => ctx.getValue<string | null>() ?? "—" },
      {
        id: "is_active",
        header: "Status",
        enableSorting: false,
        cell: ({ row }) => (
          <span className={row.original.is_active ? "text-status-paid" : "text-muted"}>
            {row.original.is_active ? "Active" : "Inactive"}
          </span>
        ),
      },
      {
        id: "actions",
        header: "",
        enableSorting: false,
        cell: ({ row }) => (
          <div className="flex justify-end gap-3" onClick={(e) => e.stopPropagation()}>
            {can("edit", "agent") && (
              <>
                <button
                  className="text-xs font-semibold text-navy hover:underline"
                  onClick={() => {
                    const name = window.prompt("Rename agent", row.original.name);
                    if (name && name.trim() && name !== row.original.name) {
                      updateAgent.mutate({ id: row.original.id, data: { name: name.trim() } });
                    }
                  }}
                >
                  Rename
                </button>
                <button
                  className="text-xs font-semibold text-muted hover:underline"
                  onClick={() =>
                    updateAgent.mutate({ id: row.original.id, data: { is_active: !row.original.is_active } })
                  }
                >
                  {row.original.is_active ? "Deactivate" : "Activate"}
                </button>
              </>
            )}
          </div>
        ),
      },
    ],
    [updateAgent],
  );

  return (
    <DataTable
      columns={columns}
      data={data?.items ?? []}
      total={data?.total ?? 0}
      page={data?.page ?? page}
      limit={data?.limit ?? 20}
      onPageChange={setPage}
      sorting={sorting}
      onSortingChange={(s) => {
        setSorting(s);
        setPage(1);
      }}
      search={search}
      onSearchChange={(q) => {
        setSearch(q);
        setPage(1);
      }}
      searchPlaceholder="Search agents by name…"
      isLoading={isLoading}
    />
  );
}
