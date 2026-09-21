import * as React from "react";
import { useNavigate } from "react-router-dom";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import { FileDown, Pencil, Plus, Trash2 } from "lucide-react";
import { DataTable } from "@/components/data-table/data-table";
import { Button } from "@/components/ui/button";
import { useLoadingSlipList, useDeleteLoadingSlip } from "@/api/loadingSlips";
import { useFirms } from "@/api/firms";
import type { LoadingSlip } from "@/api/types";
import { formatDate } from "@/lib/dates";
import { can } from "@/components/permissions/can";

const SORT_MAP: Record<string, string> = { slip_date: "slip_date" };

export function LoadingSlipListPage() {
  const navigate = useNavigate();
  const { data: firms } = useFirms();
  const firmId = firms?.[0]?.id;

  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState("");
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "slip_date", desc: true }]);

  const sortParam = sorting[0]
    ? `${sorting[0].desc ? "-" : ""}${SORT_MAP[sorting[0].id] ?? sorting[0].id}`
    : undefined;

  const { data, isLoading, isFetching } = useLoadingSlipList({
    firmId,
    q: search || undefined,
    sort: sortParam,
    page,
    limit: 20,
  });
  const deleteSlip = useDeleteLoadingSlip();

  const columns = React.useMemo<ColumnDef<LoadingSlip, any>[]>(
    () => [
      {
        id: "slip_date",
        accessorKey: "slip_date",
        header: "Date",
        enableSorting: true,
        cell: (ctx) => formatDate(ctx.getValue<string>()),
      },
      {
        id: "vehicle",
        header: "Vehicle",
        enableSorting: false,
        cell: ({ row }) => (
          <span className="font-mono text-xs text-muted">{row.original.vehicle.vehicle_no}</span>
        ),
      },
      {
        id: "truck_owner",
        header: "Truck Owner",
        enableSorting: false,
        cell: ({ row }) => row.original.truck_owner?.name ?? "—",
      },
      {
        id: "agent",
        header: "Broker",
        enableSorting: false,
        cell: ({ row }) => row.original.agent?.name ?? "—",
      },
      { id: "loading_point", accessorKey: "loading_point", header: "From", enableSorting: false },
      { id: "destination", accessorKey: "destination", header: "To", enableSorting: false },
      { id: "goods_description", accessorKey: "goods_description", header: "Goods", enableSorting: false },
      { id: "quantity_weight", accessorKey: "quantity_weight", header: "Qty", enableSorting: false },
      {
        id: "actions",
        header: "",
        enableSorting: false,
        cell: ({ row }) => (
          <div className="flex justify-end gap-3" onClick={(e) => e.stopPropagation()}>
            {can("view", "loading-slip") && (
              <button
                title="Print / Download"
                onClick={() => navigate(`/loading-slips/${row.original.id}/print`)}
                className="text-muted hover:text-navy"
              >
                <FileDown className="h-4 w-4" />
              </button>
            )}
            {can("edit", "loading-slip") && (
              <button
                title="Edit"
                onClick={() => navigate(`/loading-slips/${row.original.id}/edit`)}
                className="text-muted hover:text-navy"
              >
                <Pencil className="h-4 w-4" />
              </button>
            )}
            {can("delete", "loading-slip") && (
              <button
                title="Delete"
                onClick={() => {
                  if (confirm(`Delete this Loading Slip? This cannot be undone from the UI.`)) {
                    deleteSlip.mutate(row.original.id);
                  }
                }}
                className="text-muted hover:text-status-overdue"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            )}
          </div>
        ),
      },
    ],
    [navigate, deleteSlip],
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-[19px] font-bold text-navy">Loading Slips</h1>
          <p className="mt-0.5 text-xs text-muted">{data ? `${data.total} records` : "Loading…"}</p>
        </div>
        {can("create", "loading-slip") && (
          <Button variant="primary" onClick={() => navigate("/loading-slips/new")}>
            <Plus className="h-3.5 w-3.5" /> New Slip
          </Button>
        )}
      </div>

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
        searchPlaceholder="Search by goods or loading point…"
        isLoading={isLoading || (isFetching && !data)}
        onRowClick={(row) => navigate(`/loading-slips/${row.id}/print`)}
      />
    </div>
  );
}
