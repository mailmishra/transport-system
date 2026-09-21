import * as React from "react";
import {
  type ColumnDef,
  type SortingState,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { ArrowDown, ArrowUp, ArrowUpDown, ChevronLeft, ChevronRight, Search } from "lucide-react";
import { cn } from "@/lib/utils";

/** Shared list-screen table: server-side sort/search/pagination (the
 * DataTable never holds the full dataset -- every module's list screen
 * (Bilti, Loading Slips, Ledgers, Receipts...) reuses this one component
 * instead of re-implementing pagination per screen).
 */
interface DataTableProps<T> {
  columns: ColumnDef<T, any>[];
  data: T[];
  total: number;
  page: number;
  limit: number;
  onPageChange: (page: number) => void;
  sorting: SortingState;
  onSortingChange: (sorting: SortingState) => void;
  search?: string;
  onSearchChange?: (q: string) => void;
  searchPlaceholder?: string;
  isLoading?: boolean;
  onRowClick?: (row: T) => void;
  toolbarExtra?: React.ReactNode;
  /** Sub-tables scoped to a single record (e.g. one agent's bilti/payment
   * history on the Ledger pages) have no backend `q` filter to search
   * against -- omit search/onSearchChange and this hides the toolbar
   * entirely rather than showing an input that looks editable but isn't.
   */
  hideSearch?: boolean;
}

export function DataTable<T>({
  columns,
  data,
  total,
  page,
  limit,
  onPageChange,
  sorting,
  onSortingChange,
  search,
  onSearchChange,
  searchPlaceholder = "Search…",
  isLoading,
  onRowClick,
  toolbarExtra,
  hideSearch,
}: DataTableProps<T>) {
  const pageCount = Math.max(1, Math.ceil(total / limit));

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: (updater) => {
      const next = typeof updater === "function" ? updater(sorting) : updater;
      onSortingChange(next);
    },
    manualSorting: true,
    manualPagination: true,
    pageCount,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="flex flex-col gap-3">
      {!hideSearch && (
        <div className="flex items-center gap-2 rounded border border-border bg-white px-3 py-2">
          <Search className="h-3.5 w-3.5 text-muted" />
          <input
            value={search}
            onChange={(e) => onSearchChange?.(e.target.value)}
            placeholder={searchPlaceholder}
            className="flex-1 border-0 bg-transparent text-sm outline-none placeholder:text-muted"
          />
          {toolbarExtra}
        </div>
      )}

      <div className="overflow-hidden rounded border border-border bg-white">
        <table className="w-full text-sm">
          <thead className="bg-navy">
            {table.getHeaderGroups().map((hg) => (
              <tr key={hg.id}>
                {hg.headers.map((header) => {
                  const sortable = header.column.getCanSort();
                  const dir = header.column.getIsSorted();
                  return (
                    <th
                      key={header.id}
                      onClick={sortable ? header.column.getToggleSortingHandler() : undefined}
                      className={cn(
                        "px-4 py-2.5 text-left text-[10.5px] font-bold uppercase tracking-wide text-white/85",
                        sortable && "cursor-pointer select-none hover:text-white",
                      )}
                    >
                      <span className="inline-flex items-center gap-1">
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {sortable &&
                          (dir === "asc" ? (
                            <ArrowUp className="h-3 w-3" />
                          ) : dir === "desc" ? (
                            <ArrowDown className="h-3 w-3" />
                          ) : (
                            <ArrowUpDown className="h-3 w-3 opacity-40" />
                          ))}
                      </span>
                    </th>
                  );
                })}
              </tr>
            ))}
          </thead>
          <tbody>
            {isLoading && (
              <tr>
                <td colSpan={columns.length} className="px-4 py-8 text-center text-sm text-muted">
                  Loading…
                </td>
              </tr>
            )}
            {!isLoading && data.length === 0 && (
              <tr>
                <td colSpan={columns.length} className="px-4 py-8 text-center text-sm text-muted">
                  No records
                </td>
              </tr>
            )}
            {!isLoading &&
              table.getRowModel().rows.map((row, i) => (
                <tr
                  key={row.id}
                  onClick={() => onRowClick?.(row.original)}
                  className={cn(
                    "border-t border-background",
                    i % 2 === 1 && "bg-background/40",
                    onRowClick && "cursor-pointer hover:bg-background",
                  )}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-4 py-2.5 align-middle">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
          </tbody>
        </table>

        <div className="flex items-center justify-between border-t border-border bg-background/60 px-4 py-2.5 text-xs text-muted">
          <span>
            Page {page} of {pageCount} · {total} total
          </span>
          <div className="flex items-center gap-1">
            <button
              disabled={page <= 1}
              onClick={() => onPageChange(page - 1)}
              className="flex h-6 w-6 items-center justify-center rounded border border-border disabled:opacity-40"
            >
              <ChevronLeft className="h-3.5 w-3.5" />
            </button>
            <button
              disabled={page >= pageCount}
              onClick={() => onPageChange(page + 1)}
              className="flex h-6 w-6 items-center justify-center rounded border border-border disabled:opacity-40"
            >
              <ChevronRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
