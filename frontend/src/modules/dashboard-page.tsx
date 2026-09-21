import { useNavigate } from "react-router-dom";
import { useBiltiList } from "@/api/bilties";
import { useSelectedFirm } from "@/state/selected-firm";

/** Minimal counts-only dashboard for Phase 1 -- the old concept app's
 * dashboard() summed every bilti's dalali/FD client-side over the whole
 * fetched table, which is exactly the pattern this rewrite removes.
 * `total` now comes straight from the paginated envelope, no full fetch.
 */
export function DashboardPage() {
  const navigate = useNavigate();
  const { firm, firmId } = useSelectedFirm();
  const { data: bilties } = useBiltiList({ firmId, limit: 1 });

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-[19px] font-bold text-navy">Dashboard</h1>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatCard label="Bilties" value={bilties?.total ?? "…"} accent="border-navy" />
        <StatCard label="Firm" value={firm?.name ?? "…"} accent="border-gold" small />
      </div>
      <button
        onClick={() => navigate("/bilti")}
        className="w-fit rounded bg-navy px-4 py-2 text-sm font-semibold text-white"
      >
        Go to Bilti / GR →
      </button>
    </div>
  );
}

function StatCard({
  label,
  value,
  accent,
  small,
}: {
  label: string;
  value: string | number;
  accent: string;
  small?: boolean;
}) {
  return (
    <div className={`rounded border border-border border-l-4 ${accent} bg-white px-3.5 py-2.5`}>
      <div className="text-[10.5px] font-semibold uppercase tracking-wide text-muted">{label}</div>
      <div className={`mt-0.5 font-bold text-navy ${small ? "text-sm" : "text-lg"}`}>{value}</div>
    </div>
  );
}
