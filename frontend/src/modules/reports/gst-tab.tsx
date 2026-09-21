import * as React from "react";
import { useGstReport } from "@/api/reports";
import { rupees } from "@/lib/money";
import { DateRangeFilter } from "./date-range-filter";

const LABELS: Record<string, string> = {
  consignor: "Consignor",
  consignee: "Consignee",
  transporter: "Transporter",
  exempted: "Exempted",
};

export function GstTab({ firmId }: { firmId: string | undefined }) {
  const [range, setRange] = React.useState({ dateFrom: "", dateTo: "" });
  const { data, isLoading } = useGstReport(firmId, range);

  return (
    <div className="flex flex-col gap-3">
      <DateRangeFilter dateFrom={range.dateFrom} dateTo={range.dateTo} onChange={setRange} />

      {isLoading && <p className="text-sm text-muted">Loading…</p>}

      {data && (
        <div className="overflow-hidden rounded border border-border bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-navy text-left text-[10.5px] uppercase text-white">
                <th className="px-3 py-2">GST Paid By</th>
                <th className="px-3 py-2 text-right">Bilti Count</th>
                <th className="px-3 py-2 text-right">Total Freight</th>
                <th className="px-3 py-2 text-right">Total Grand Total</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row) => (
                <tr key={row.gst_paid_by ?? "unset"} className="border-t border-border">
                  <td className="px-3 py-2">
                    {row.gst_paid_by ? LABELS[row.gst_paid_by] ?? row.gst_paid_by : "Not set"}
                  </td>
                  <td className="px-3 py-2 text-right">{row.bilti_count}</td>
                  <td className="px-3 py-2 text-right">{rupees(row.total_freight)}</td>
                  <td className="px-3 py-2 text-right">{rupees(row.total_grand_total)}</td>
                </tr>
              ))}
              {data.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-3 py-6 text-center text-sm text-muted">
                    No bilties in this period.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
