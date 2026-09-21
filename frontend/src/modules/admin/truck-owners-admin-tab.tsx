import * as React from "react";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import { DataTable } from "@/components/data-table/data-table";
import { useTruckOwnerList, useUpdateTruckOwner } from "@/api/truckOwners";
import type { TruckOwner } from "@/api/types";
import { can } from "@/components/permissions/can";

export function TruckOwnersAdminTab() {
  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState("");
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "name", desc: false }]);
  const { data, isLoading } = useTruckOwnerList({
    q: search || undefined,
    sort: sorting[0] ? `${sorting[0].desc ? "-" : ""}name` : "name",
    page,
    limit: 20,
  });
  const updateOwner = useUpdateTruckOwner();

  const columns = React.useMemo<ColumnDef<TruckOwner, any>[]>(
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
            {can("edit", "truck-owner") && (
              <>
                <button
                  className="text-xs font-semibold text-navy hover:underline"
                  onClick={() => {
                    const name = window.prompt("Rename truck owner", row.original.name);
                    if (name && name.trim() && name !== row.original.name) {
                      updateOwner.mutate({ id: row.original.id, data: { name: name.trim() } });
                    }
                  }}
                >
                  Rename
                </button>
                <button
                  className="text-xs font-semibold text-muted hover:underline"
                  onClick={() =>
                    updateOwner.mutate({ id: row.original.id, data: { is_active: !row.original.is_active } })
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
    [updateOwner],
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
      searchPlaceholder="Search truck owners by name…"
      isLoading={isLoading}
    />
  );
}
