import { Link } from "react-router-dom";
import { usePendingLoadingSlips } from "@/api/reports";
import { formatDate } from "@/lib/dates";

export function PendingLoadingSlipsTab({ firmId }: { firmId: string | undefined }) {
  const { data, isLoading } = usePendingLoadingSlips(firmId);

  if (isLoading) {
    return <p className="text-sm text-muted">Loading…</p>;
  }

  return (
    <div className="flex flex-col gap-3">
      <p className="text-xs text-muted">
        Loading slips with no Bilti / GR raised against them yet -- a dispatch follow-up queue.
      </p>
      <div className="overflow-hidden rounded border border-border bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-navy text-left text-[10.5px] uppercase text-white">
              <th className="px-3 py-2">Date</th>
              <th className="px-3 py-2">Vehicle</th>
              <th className="px-3 py-2">From</th>
              <th className="px-3 py-2">To</th>
              <th className="px-3 py-2">Truck Owner</th>
              <th className="px-3 py-2"></th>
            </tr>
          </thead>
          <tbody>
            {data?.map((slip) => (
              <tr key={slip.id} className="border-t border-border">
                <td className="px-3 py-2">{formatDate(slip.slip_date)}</td>
                <td className="px-3 py-2 font-mono text-xs text-muted">{slip.vehicle.vehicle_no}</td>
                <td className="px-3 py-2">{slip.loading_point}</td>
                <td className="px-3 py-2">{slip.destination}</td>
                <td className="px-3 py-2">{slip.truck_owner?.name ?? "—"}</td>
                <td className="px-3 py-2 text-right">
                  <Link to={`/loading-slips/${slip.id}/edit`} className="text-xs font-semibold text-navy hover:underline">
                    Open
                  </Link>
                </td>
              </tr>
            ))}
            {data?.length === 0 && (
              <tr>
                <td colSpan={6} className="px-3 py-6 text-center text-sm text-muted">
                  Nothing pending -- every loading slip has a Bilti / GR.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
