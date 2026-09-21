import { Link } from "react-router-dom";
import { useReceivables } from "@/api/reports";
import { rupees } from "@/lib/money";
import { formatDate } from "@/lib/dates";
import { ExportCsvButton } from "./export-csv-button";

export function ReceivablesTab({ firmId }: { firmId: string | undefined }) {
  const { data, isLoading } = useReceivables(firmId);

  if (isLoading) {
    return <p className="text-sm text-muted">Loading…</p>;
  }

  const totalOutstanding = data?.reduce((sum, r) => sum + Number(r.outstanding), 0) ?? 0;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-start justify-between gap-3">
        <div className="rounded border-l-4 border-gold bg-white px-4 py-3">
          <div className="text-[10.5px] font-semibold uppercase tracking-wide text-muted">
            Total Outstanding ({data?.length ?? 0} bilties)
          </div>
          <div className="mt-1 text-xl font-extrabold text-navy">{rupees(totalOutstanding)}</div>
        </div>
        <ExportCsvButton
          filename="receivables"
          columns={[
            { key: "bilti_date", header: "Date" },
            { key: "bilti_no", header: "Bilti" },
            { key: "consignor", header: "Consignor" },
            { key: "consignee", header: "Consignee" },
            { key: "topay", header: "To Pay" },
            { key: "received", header: "Received" },
            { key: "outstanding", header: "Outstanding" },
            { key: "days_outstanding", header: "Days Outstanding" },
          ]}
          rows={data}
        />
      </div>

      <div className="overflow-hidden rounded border border-border bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-navy text-left text-[10.5px] uppercase text-white">
              <th className="px-3 py-2">Date</th>
              <th className="px-3 py-2">Bilti</th>
              <th className="px-3 py-2">Consignor</th>
              <th className="px-3 py-2">Consignee</th>
              <th className="px-3 py-2 text-right">To Pay</th>
              <th className="px-3 py-2 text-right">Received</th>
              <th className="px-3 py-2 text-right">Outstanding</th>
              <th className="px-3 py-2 text-right">Days</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((r) => (
              <tr key={r.bilti_id} className="border-t border-border">
                <td className="px-3 py-2">{formatDate(r.bilti_date)}</td>
                <td className="px-3 py-2">
                  <Link to={`/bilti/${r.bilti_id}/edit`} className="font-semibold text-navy hover:underline">
                    {r.bilti_no}
                  </Link>
                </td>
                <td className="px-3 py-2">{r.consignor}</td>
                <td className="px-3 py-2">{r.consignee}</td>
                <td className="px-3 py-2 text-right">{rupees(r.topay)}</td>
                <td className="px-3 py-2 text-right">{rupees(r.received)}</td>
                <td className="px-3 py-2 text-right font-semibold">{rupees(r.outstanding)}</td>
                <td className={`px-3 py-2 text-right ${r.days_outstanding > 30 ? "text-status-overdue" : ""}`}>
                  {r.days_outstanding}
                </td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td colSpan={8} className="px-3 py-6 text-center text-sm text-muted">
                  Nothing outstanding -- every bilti has been fully received.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
