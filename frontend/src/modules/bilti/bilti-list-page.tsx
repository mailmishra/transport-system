import * as React from "react";
import { useNavigate } from "react-router-dom";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import { FileDown, Pencil, Plus, Trash2 } from "lucide-react";
import { DataTable } from "@/components/data-table/data-table";
import { Button } from "@/components/ui/button";
import { useBiltiList, useDeleteBilti } from "@/api/bilties";
import { useSelectedFirm } from "@/state/selected-firm";
import type { Bilti } from "@/api/types";
import { rupees } from "@/lib/money";
import { formatDate } from "@/lib/dates";
import { can } from "@/components/permissions/can";

const SORT_MAP: Record<string, string> = {
  bilti_date: "bilti_date",
  bilti_no: "bilti_no",
  freight: "freight",
};

export function BiltiListPage() {
  const navigate = useNavigate();
  const { firmId } = useSelectedFirm();

  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState("");
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "bilti_date", desc: true }]);

  const sortParam = sorting[0]
    ? `${sorting[0].desc ? "-" : ""}${SORT_MAP[sorting[0].id] ?? sorting[0].id}`
    : undefined;

  const { data, isLoading, isFetching } = useBiltiList({
    firmId,
    q: search || undefined,
    sort: sortParam,
    page,
    limit: 20,
  });
  const deleteBilti = useDeleteBilti();

  const columns = React.useMemo<ColumnDef<Bilti, any>[]>(
    () => [
      {
        id: "bilti_no",
        accessorKey: "bilti_no",
        header: "GR No.",
        enableSorting: true,
        cell: (ctx) => <span className="font-bold text-foreground">{ctx.getValue<string>()}</span>,
      },
      {
        id: "bilti_date",
        accessorKey: "bilti_date",
        header: "Date",
        enableSorting: true,
        cell: (ctx) => formatDate(ctx.getValue<string>()),
      },
      { id: "consignor", accessorKey: "consignor", header: "Consignor", enableSorting: false },
      { id: "consignee", accessorKey: "consignee", header: "Consignee", enableSorting: false },
      {
        id: "vehicle",
        header: "Vehicle",
        enableSorting: false,
        cell: ({ row }) => (
          <span className="font-mono text-xs text-muted">{row.original.vehicle.vehicle_no}</span>
        ),
      },
      {
        id: "freight",
        accessorKey: "freight",
        header: "Freight",
        enableSorting: true,
        cell: (ctx) => <span className="tabular-nums">{rupees(ctx.getValue<string>())}</span>,
      },
      {
        id: "grand_total",
        header: "Grand Total",
        enableSorting: false,
        cell: ({ row }) => (
          <span className="font-bold tabular-nums">{rupees(row.original.grand_total)}</span>
        ),
      },
      {
        id: "actions",
        header: "",
        enableSorting: false,
        cell: ({ row }) => (
          <div className="flex justify-end gap-3" onClick={(e) => e.stopPropagation()}>
            {can("view", "bilti") && (
              <button
                title="Print / Download"
                onClick={() => navigate(`/bilti/${row.original.id}/print`)}
                className="text-muted hover:text-navy"
              >
                <FileDown className="h-4 w-4" />
              </button>
            )}
            {can("edit", "bilti") && (
              <button
                title="Edit"
                onClick={() => navigate(`/bilti/${row.original.id}/edit`)}
                className="text-muted hover:text-navy"
              >
                <Pencil className="h-4 w-4" />
              </button>
            )}
            {can("delete", "bilti") && (
              <button
                title="Delete"
                onClick={() => {
                  if (confirm(`Delete Bilti ${row.original.bilti_no}? This cannot be undone from the UI.`)) {
                    deleteBilti.mutate(row.original.id);
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
    [navigate, deleteBilti],
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-[19px] font-bold text-navy">Bilti / GR</h1>
          <p className="mt-0.5 text-xs text-muted">
            {data ? `${data.total} records` : "Loading…"}
          </p>
        </div>
        {can("create", "bilti") && (
          <Button variant="primary" onClick={() => navigate("/bilti/new")}>
            <Plus className="h-3.5 w-3.5" /> New GR
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
        searchPlaceholder="Search by GR no., consignor, consignee…"
        isLoading={isLoading || (isFetching && !data)}
        onRowClick={(row) => navigate(`/bilti/${row.id}/print`)}
      />
    </div>
  );
}
