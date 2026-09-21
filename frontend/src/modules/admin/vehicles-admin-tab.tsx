import * as React from "react";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import { DataTable } from "@/components/data-table/data-table";
import { useVehicleList, useUpdateVehicle } from "@/api/vehicles";
import type { Vehicle } from "@/api/types";
import { can } from "@/components/permissions/can";

export function VehiclesAdminTab() {
  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState("");
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "vehicle_no", desc: false }]);
  const { data, isLoading } = useVehicleList({
    q: search || undefined,
    sort: sorting[0] ? `${sorting[0].desc ? "-" : ""}vehicle_no` : "vehicle_no",
    page,
    limit: 20,
  });
  const updateVehicle = useUpdateVehicle();

  const columns = React.useMemo<ColumnDef<Vehicle, any>[]>(
    () => [
      {
        id: "vehicle_no",
        accessorKey: "vehicle_no",
        header: "Vehicle No.",
        enableSorting: true,
        cell: (ctx) => <span className="font-mono text-xs">{ctx.getValue<string>()}</span>,
      },
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
            {can("edit", "vehicle") && (
              <>
                <button
                  className="text-xs font-semibold text-navy hover:underline"
                  onClick={() => {
                    const no = window.prompt("Rename vehicle no.", row.original.vehicle_no);
                    if (no && no.trim() && no !== row.original.vehicle_no) {
                      updateVehicle.mutate({ id: row.original.id, data: { vehicle_no: no.trim() } });
                    }
                  }}
                >
                  Rename
                </button>
                <button
                  className="text-xs font-semibold text-muted hover:underline"
                  onClick={() =>
                    updateVehicle.mutate({ id: row.original.id, data: { is_active: !row.original.is_active } })
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
    [updateVehicle],
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
      searchPlaceholder="Search by vehicle no…"
      isLoading={isLoading}
    />
  );
}
