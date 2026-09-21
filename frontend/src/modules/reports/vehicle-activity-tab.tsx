import * as React from "react";
import { useVehicleActivity } from "@/api/reports";
import { rupees } from "@/lib/money";
import { DateRangeFilter } from "./date-range-filter";
import { ExportCsvButton } from "./export-csv-button";

export function VehicleActivityTab({ firmId }: { firmId: string | undefined }) {
  const [range, setRange] = React.useState({ dateFrom: "", dateTo: "" });
  const { data, isLoading } = useVehicleActivity(firmId, range);

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-start justify-between gap-3">
        <DateRangeFilter dateFrom={range.dateFrom} dateTo={range.dateTo} onChange={setRange} />
        <ExportCsvButton
          filename="vehicle-activity"
          columns={[
            { key: "vehicle_no", header: "Vehicle No." },
            { key: "trip_count", header: "Trips" },
            { key: "total_freight", header: "Total Freight" },
          ]}
          rows={data}
        />
      </div>

      {isLoading && <p className="text-sm text-muted">Loading…</p>}

      {data && (
        <div className="overflow-hidden rounded border border-border bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-navy text-left text-[10.5px] uppercase text-white">
                <th className="px-3 py-2">Vehicle No.</th>
                <th className="px-3 py-2 text-right">Trips</th>
                <th className="px-3 py-2 text-right">Total Freight</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row) => (
                <tr key={row.vehicle_id} className="border-t border-border">
                  <td className="px-3 py-2 font-medium">{row.vehicle_no}</td>
                  <td className="px-3 py-2 text-right">{row.trip_count}</td>
                  <td className="px-3 py-2 text-right">{rupees(row.total_freight)}</td>
                </tr>
              ))}
              {data.length === 0 && (
                <tr>
                  <td colSpan={3} className="px-3 py-6 text-center text-sm text-muted">
                    No trips in this period.
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
