import { cn } from "@/lib/utils";

export type BiltiStatus = "paid" | "pending" | "overdue";

const LABEL: Record<BiltiStatus, string> = {
  paid: "Paid",
  pending: "Pending",
  overdue: "Overdue",
};

const COLOR: Record<BiltiStatus, string> = {
  paid: "text-status-paid",
  pending: "text-status-pending",
  overdue: "text-status-overdue",
};

/** Dot + label, matching Style B's convention (not a filled pill --
 * see StyleB-Desktop.dc.html's table rows in the approved mockup). */
export function StatusBadge({ status }: { status: BiltiStatus }) {
  return (
    <span className={cn("inline-flex items-center gap-1.5 text-xs font-semibold", COLOR[status])}>
      <span className={cn("h-1.5 w-1.5 rounded-full", `bg-current`)} />
      {LABEL[status]}
    </span>
  );
}

/** Freight fully received -> paid; nothing received and past-due -> overdue
 * (7+ days is a reasonable default, adjustable later); otherwise pending.
 * Mirrors the arithmetic already proven in concept/index.html's
 * reportOutstanding() (freight - sum(receipts for that bilti)).
 */
export function biltiStatus(freight: string, received: number, biltiDate: string): BiltiStatus {
  const outstanding = Number(freight) - received;
  if (outstanding <= 0) return "paid";
  const daysSince = (Date.now() - new Date(biltiDate).getTime()) / 86_400_000;
  return daysSince > 7 ? "overdue" : "pending";
}
