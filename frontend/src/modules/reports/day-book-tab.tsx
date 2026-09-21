import * as React from "react";
import { useDayBook } from "@/api/reports";
import { rupees } from "@/lib/money";
import { formatDate, todayIso } from "@/lib/dates";
import { DateRangeFilter } from "./date-range-filter";

const KIND_LABEL: Record<string, string> = {
  receipt: "Receipt",
  agent_payment: "Agent Payment",
  truck_owner_payment: "Truck Owner Payment",
};

export function DayBookTab({ firmId }: { firmId: string | undefined }) {
  const [range, setRange] = React.useState({ dateFrom: todayIso(), dateTo: todayIso() });
  const { data, isLoading } = useDayBook(firmId, range);

  return (
    <div className="flex flex-col gap-3">
      <DateRangeFilter dateFrom={range.dateFrom} dateTo={range.dateTo} onChange={setRange} />

      {isLoading && <p className="text-sm text-muted">Loading…</p>}

      {data && (
        <>
          <div className="grid grid-cols-3 gap-3">
            <SummaryCard label="Total Inflow" value={data.total_inflow} />
            <SummaryCard label="Total Outflow" value={data.total_outflow} />
            <SummaryCard label="Net" value={data.net} emphasize />
          </div>

          <div className="overflow-hidden rounded border border-border bg-white">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-navy text-left text-[10.5px] uppercase text-white">
                  <Th>Date</Th>
                  <Th>Type</Th>
                  <Th>Particulars</Th>
                  <Th align="right">Inflow</Th>
                  <Th align="right">Outflow</Th>
                </tr>
              </thead>
              <tbody>
                {data.entries.map((e, i) => (
                  <tr key={i} className="border-t border-border">
                    <Td>{formatDate(e.date)}</Td>
                    <Td>{KIND_LABEL[e.kind] ?? e.kind}</Td>
                    <Td>{e.particulars}</Td>
                    <Td align="right">{Number(e.inflow) > 0 ? rupees(e.inflow) : "—"}</Td>
                    <Td align="right">{Number(e.outflow) > 0 ? rupees(e.outflow) : "—"}</Td>
                  </tr>
                ))}
                {data.entries.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-3 py-6 text-center text-sm text-muted">
                      No transactions in this period.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

function SummaryCard({ label, value, emphasize }: { label: string; value: string; emphasize?: boolean }) {
  return (
    <div className="rounded border-l-4 border-gold bg-white px-4 py-3">
      <div className="text-[10.5px] font-semibold uppercase tracking-wide text-muted">{label}</div>
      <div className={emphasize ? "mt-1 text-xl font-extrabold text-navy" : "mt-1 text-lg font-bold text-foreground"}>
        {rupees(value)}
      </div>
    </div>
  );
}

function Th({ children, align }: { children: React.ReactNode; align?: "right" }) {
  return <th className={`px-3 py-2 ${align === "right" ? "text-right" : "text-left"}`}>{children}</th>;
}
function Td({ children, align }: { children: React.ReactNode; align?: "right" }) {
  return <td className={`px-3 py-2 ${align === "right" ? "text-right" : "text-left"}`}>{children}</td>;
}
