import { useOutstandingSummary } from "@/api/reports";
import { rupees } from "@/lib/money";
import { ExportCsvButton } from "./export-csv-button";

export function OutstandingTab({ firmId }: { firmId: string | undefined }) {
  const { data, isLoading } = useOutstandingSummary(firmId);

  if (isLoading || !data) {
    return <p className="text-sm text-muted">Loading…</p>;
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-start justify-between gap-3">
        <p className="text-xs text-muted">
          A firm-wide snapshot as of now -- not date-ranged, since "outstanding" is a point-in-time balance.
        </p>
        <ExportCsvButton
          filename="outstanding-summary"
          columns={[
            { key: "total_receivable", header: "Total Receivable" },
            { key: "total_received", header: "Total Received" },
            { key: "net_receivable", header: "Net Receivable" },
            { key: "total_agent_payable", header: "Payable to Agents" },
            { key: "total_truck_owner_payable", header: "Payable to Truck Owners" },
          ]}
          rows={[data]}
        />
      </div>
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-3">
        <Card label="Receivable from Consignees" value={data.total_receivable} />
        <Card label="Received So Far" value={data.total_received} />
        <Card label="Net Receivable" value={data.net_receivable} emphasize />
        <Card label="Payable to Agents / Dalals" value={data.total_agent_payable} />
        <Card label="Payable to Truck Owners" value={data.total_truck_owner_payable} />
      </div>
    </div>
  );
}

function Card({ label, value, emphasize }: { label: string; value: string; emphasize?: boolean }) {
  return (
    <div className="rounded border-l-4 border-gold bg-white px-4 py-3">
      <div className="text-[10.5px] font-semibold uppercase tracking-wide text-muted">{label}</div>
      <div className={emphasize ? "mt-1 text-2xl font-extrabold text-navy" : "mt-1 text-xl font-bold text-foreground"}>
        {rupees(value)}
      </div>
    </div>
  );
}
