import * as React from "react";
import { Download } from "lucide-react";
import { useBiltiList } from "@/api/bilties";
import { useAgentList } from "@/api/agents";
import { useVehicleList } from "@/api/vehicles";
import { useLoadingSlipList } from "@/api/loadingSlips";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { rupees } from "@/lib/money";
import { formatDate } from "@/lib/dates";
import { downloadCsv } from "@/lib/csv";
import type { Bilti } from "@/api/types";

const SELECT_CLS =
  "flex h-9 w-full rounded border border-border bg-white px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-navy";

interface Filters {
  dateFrom: string;
  dateTo: string;
  vehicleNo: string;
  fromLocation: string;
  toLocation: string;
  agentName: string;
  factoryName: string;
}

const EMPTY: Filters = {
  dateFrom: "", dateTo: "", vehicleNo: "", fromLocation: "",
  toLocation: "", agentName: "", factoryName: "",
};

function hasFilter(f: Filters) {
  return Object.values(f).some(Boolean);
}

function flattenForCsv(row: Bilti) {
  return {
    bilti_no: row.bilti_no,
    bilti_date: row.bilti_date,
    consignor: row.consignor,
    consignee: row.consignee,
    from_location: row.from_location,
    to_location: row.to_location,
    vehicle_no: row.vehicle.vehicle_no,
    agent: row.agent?.name ?? "",
    truck_owner: row.truck_owner.name,
    goods_description: row.goods_description,
    weight: row.weight,
    freight: row.freight,
    grand_total: row.grand_total,
    topay: row.topay,
    advance_to_owner: row.advance_to_owner,
  };
}

const CSV_COLS = [
  { key: "bilti_no" as const, header: "GR No." },
  { key: "bilti_date" as const, header: "Date" },
  { key: "consignor" as const, header: "Consignor" },
  { key: "consignee" as const, header: "Consignee" },
  { key: "from_location" as const, header: "From" },
  { key: "to_location" as const, header: "To" },
  { key: "vehicle_no" as const, header: "Vehicle No." },
  { key: "agent" as const, header: "Agent" },
  { key: "truck_owner" as const, header: "Truck Owner" },
  { key: "goods_description" as const, header: "Goods" },
  { key: "weight" as const, header: "Weight" },
  { key: "freight" as const, header: "Freight" },
  { key: "grand_total" as const, header: "Grand Total" },
  { key: "topay" as const, header: "To Pay" },
  { key: "advance_to_owner" as const, header: "Advance" },
];

export function GrReportTab({ firmId }: { firmId: string | undefined }) {
  const [filters, setFilters] = React.useState<Filters>(EMPTY);
  const [applied, setApplied] = React.useState<Filters>(EMPTY);

  // Populate dropdowns — fetch all at once; these lists are small
  const { data: agentsPage } = useAgentList({ sort: "name", limit: 500 });
  const { data: vehiclesPage } = useVehicleList({ sort: "vehicle_no", limit: 500 });
  const { data: slipsPage } = useLoadingSlipList({ firmId, limit: 500 });

  const agents = agentsPage?.items ?? [];
  const vehicles = vehiclesPage?.items ?? [];

  // Unique, sorted factory names from loading slips
  const factories = React.useMemo(() => {
    const names = (slipsPage?.items ?? [])
      .map((s) => s.factory_name)
      .filter((n): n is string => !!n);
    return [...new Set(names)].sort((a, b) => a.localeCompare(b));
  }, [slipsPage]);

  const active = hasFilter(applied);

  const { data, isLoading } = useBiltiList({
    firmId,
    dateFrom: applied.dateFrom || undefined,
    dateTo: applied.dateTo || undefined,
    vehicleNo: applied.vehicleNo || undefined,
    fromLocation: applied.fromLocation || undefined,
    toLocation: applied.toLocation || undefined,
    agentName: applied.agentName || undefined,
    factoryName: applied.factoryName || undefined,
    limit: 500,
    sort: "-bilti_date",
  });

  function set(key: keyof Filters, value: string) {
    setFilters((f) => ({ ...f, [key]: value }));
  }

  function apply() {
    setApplied({ ...filters });
  }

  function reset() {
    setFilters(EMPTY);
    setApplied(EMPTY);
  }

  const rows = data?.items ?? [];
  const flatRows = rows.map(flattenForCsv);

  return (
    <div className="flex flex-col gap-4">
      {/* Filter panel */}
      <div className="rounded border border-border bg-white p-4">
        <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted">Filters</p>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          <div>
            <Label>Date From</Label>
            <Input type="date" className="mt-1" value={filters.dateFrom}
              onChange={(e) => set("dateFrom", e.target.value)} />
          </div>
          <div>
            <Label>Date To</Label>
            <Input type="date" className="mt-1" value={filters.dateTo}
              onChange={(e) => set("dateTo", e.target.value)} />
          </div>

          <div>
            <Label>Truck / Vehicle No.</Label>
            <select className={`${SELECT_CLS} mt-1`} value={filters.vehicleNo}
              onChange={(e) => set("vehicleNo", e.target.value)}>
              <option value="">All vehicles</option>
              {vehicles.map((v) => (
                <option key={v.id} value={v.vehicle_no}>{v.vehicle_no}</option>
              ))}
            </select>
          </div>

          <div>
            <Label>Agent / Dalal</Label>
            <select className={`${SELECT_CLS} mt-1`} value={filters.agentName}
              onChange={(e) => set("agentName", e.target.value)}>
              <option value="">All agents</option>
              {agents.map((a) => (
                <option key={a.id} value={a.name}>{a.name}</option>
              ))}
            </select>
          </div>

          <div>
            <Label>Factory / Mill</Label>
            <select className={`${SELECT_CLS} mt-1`} value={filters.factoryName}
              onChange={(e) => set("factoryName", e.target.value)}>
              <option value="">All factories</option>
              {factories.map((f) => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>

          <div>
            <Label>From (Source)</Label>
            <Input className="mt-1" placeholder="e.g. Indore" value={filters.fromLocation}
              onChange={(e) => set("fromLocation", e.target.value)} />
          </div>
          <div>
            <Label>To (Destination)</Label>
            <Input className="mt-1" placeholder="e.g. Mumbai" value={filters.toLocation}
              onChange={(e) => set("toLocation", e.target.value)} />
          </div>
        </div>
        <div className="mt-3 flex gap-2">
          <Button variant="primary" size="sm" onClick={apply}>Apply Filters</Button>
          {hasFilter(filters) && (
            <Button variant="ghost" size="sm" onClick={reset}>Clear</Button>
          )}
        </div>
      </div>

      {/* Results header */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted">
          {!active
            ? "Apply filters above to load GRs."
            : isLoading
            ? "Loading…"
            : `${data?.total ?? 0} GR${(data?.total ?? 0) === 1 ? "" : "s"} found`}
        </p>
        <Button
          variant="secondary"
          size="sm"
          disabled={flatRows.length === 0}
          onClick={() => downloadCsv("gr-report", CSV_COLS, flatRows)}
        >
          <Download className="h-3.5 w-3.5" /> Export CSV
        </Button>
      </div>

      {/* Table */}
      {active && !isLoading && (
        <div className="overflow-x-auto rounded border border-border bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-navy text-left text-[10.5px] uppercase text-white">
                <th className="px-3 py-2">GR No.</th>
                <th className="px-3 py-2">Date</th>
                <th className="px-3 py-2">Consignor</th>
                <th className="px-3 py-2">Consignee</th>
                <th className="px-3 py-2">From</th>
                <th className="px-3 py-2">To</th>
                <th className="px-3 py-2">Vehicle</th>
                <th className="px-3 py-2">Agent</th>
                <th className="px-3 py-2">Goods</th>
                <th className="px-3 py-2 text-right">Freight</th>
                <th className="px-3 py-2 text-right">Grand Total</th>
                <th className="px-3 py-2 text-right">To Pay</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="border-t border-border hover:bg-muted/30">
                  <td className="px-3 py-2 font-bold">{row.bilti_no}</td>
                  <td className="px-3 py-2 tabular-nums">{formatDate(row.bilti_date)}</td>
                  <td className="px-3 py-2">{row.consignor}</td>
                  <td className="px-3 py-2">{row.consignee}</td>
                  <td className="px-3 py-2">{row.from_location}</td>
                  <td className="px-3 py-2">{row.to_location}</td>
                  <td className="px-3 py-2 font-mono text-xs">{row.vehicle.vehicle_no}</td>
                  <td className="px-3 py-2">{row.agent?.name ?? "—"}</td>
                  <td className="px-3 py-2 max-w-[140px] truncate" title={row.goods_description}>
                    {row.goods_description}
                  </td>
                  <td className="px-3 py-2 text-right tabular-nums">{rupees(row.freight)}</td>
                  <td className="px-3 py-2 text-right font-bold tabular-nums">{rupees(row.grand_total)}</td>
                  <td className="px-3 py-2 text-right tabular-nums">{rupees(row.topay)}</td>
                </tr>
              ))}
              {rows.length === 0 && (
                <tr>
                  <td colSpan={12} className="px-3 py-8 text-center text-sm text-muted">
                    No GRs match these filters.
                  </td>
                </tr>
              )}
            </tbody>
            {rows.length > 0 && (
              <tfoot>
                <tr className="border-t-2 border-border bg-gray-50 font-bold">
                  <td colSpan={9} className="px-3 py-2 text-xs text-muted">
                    Total ({rows.length} GRs)
                  </td>
                  <td className="px-3 py-2 text-right tabular-nums">
                    {rupees(rows.reduce((s, r) => s + parseFloat(r.freight as string), 0).toFixed(2))}
                  </td>
                  <td className="px-3 py-2 text-right tabular-nums">
                    {rupees(rows.reduce((s, r) => s + parseFloat(r.grand_total as string), 0).toFixed(2))}
                  </td>
                  <td className="px-3 py-2 text-right tabular-nums">
                    {rupees(rows.reduce((s, r) => s + parseFloat(r.topay as string), 0).toFixed(2))}
                  </td>
                </tr>
              </tfoot>
            )}
          </table>
        </div>
      )}
    </div>
  );
}
