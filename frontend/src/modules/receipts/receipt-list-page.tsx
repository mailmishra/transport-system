import * as React from "react";
import { useNavigate } from "react-router-dom";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import { FileDown, Plus, Trash2, ExternalLink } from "lucide-react";
import { DataTable } from "@/components/data-table/data-table";
import { Button } from "@/components/ui/button";
import { useReceiptList, useDeleteReceipt } from "@/api/receipts";
import { useSelectedFirm } from "@/state/selected-firm";
import type { Receipt } from "@/api/types";
import { rupees } from "@/lib/money";
import { formatDate } from "@/lib/dates";
import { can } from "@/components/permissions/can";

const SORT_MAP: Record<string, string> = { receipt_date: "receipt_date", amount: "amount" };

/** Receipt.bilti_id is a bare FK (ReceiptRead doesn't expand the Bilti
 * object -- see backend/app/schemas/receipt.py), so the list intentionally
 * does not show the GR number inline: doing that would mean an extra fetch
 * per row (N+1), the same scale trade-off Phase 1 already declined for the
 * Bilti list's status badge. "View GR" opens the Bilti print view directly.
 */
export function ReceiptListPage() {
  const navigate = useNavigate();
  const { firmId } = useSelectedFirm();

  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState("");
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "receipt_date", desc: true }]);

  const sortParam = sorting[0]
    ? `${sorting[0].desc ? "-" : ""}${SORT_MAP[sorting[0].id] ?? sorting[0].id}`
    : undefined;

  const { data, isLoading, isFetching } = useReceiptList({
    firmId,
    q: search || undefined,
    sort: sortParam,
    page,
    limit: 20,
  });
  const deleteReceipt = useDeleteReceipt();

  const columns = React.useMemo<ColumnDef<Receipt, any>[]>(
    () => [
      {
        id: "receipt_date",
        accessorKey: "receipt_date",
        header: "Date",
        enableSorting: true,
        cell: (ctx) => formatDate(ctx.getValue<string>()),
      },
      { id: "received_from", accessorKey: "received_from", header: "Received From", enableSorting: false },
      {
        id: "amount",
        accessorKey: "amount",
        header: "Amount",
        enableSorting: true,
        cell: (ctx) => <span className="font-bold tabular-nums">{rupees(ctx.getValue<string>())}</span>,
      },
      {
        id: "remarks",
        accessorKey: "remarks",
        header: "Remarks",
        enableSorting: false,
        cell: (ctx) => ctx.getValue<string | null>() ?? "—",
      },
      {
        id: "actions",
        header: "",
        enableSorting: false,
        cell: ({ row }) => (
          <div className="flex justify-end gap-3" onClick={(e) => e.stopPropagation()}>
            <button
              title="View GR"
              onClick={() => navigate(`/bilti/${row.original.bilti_id}/print`)}
              className="text-muted hover:text-navy"
            >
              <ExternalLink className="h-4 w-4" />
            </button>
            {can("view", "receipt") && (
              <button
                title="Print / Download Receipt"
                onClick={() => navigate(`/receipts/${row.original.id}/print`)}
                className="text-muted hover:text-navy"
              >
                <FileDown className="h-4 w-4" />
              </button>
            )}
            {can("delete", "receipt") && (
              <button
                title="Delete"
                onClick={() => {
                  if (confirm("Delete this receipt? This cannot be undone from the UI.")) {
                    deleteReceipt.mutate(row.original.id);
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
    [navigate, deleteReceipt],
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-[19px] font-bold text-navy">Receipts</h1>
          <p className="mt-0.5 text-xs text-muted">{data ? `${data.total} records` : "Loading…"}</p>
        </div>
        {can("create", "receipt") && (
          <Button variant="primary" onClick={() => navigate("/receipts/new")}>
            <Plus className="h-3.5 w-3.5" /> New Receipt
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
        searchPlaceholder="Search by received from…"
        isLoading={isLoading || (isFetching && !data)}
        onRowClick={(row) => navigate(`/receipts/${row.id}/print`)}
      />
    </div>
  );
}
