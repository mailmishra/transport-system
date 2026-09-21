import { useParams } from "react-router-dom";
import { useTruckOwner, useTruckOwnerStatement } from "@/api/truckOwners";
import { useSelectedFirm } from "@/state/selected-firm";
import { rupees } from "@/lib/money";
import { formatDate } from "@/lib/dates";
import { PrintDocument } from "@/components/print/print-document";

/** Ledger Statement PDF for a truck owner -- mirrors
 * agent-ledger-print-view.tsx; see that file's comment for the shared
 * shape/rationale. Data comes from GET /truck-owners/{id}/statement.
 */
export function TruckOwnerLedgerPrintView() {
  const { id } = useParams();
  const { data: owner } = useTruckOwner(id);
  const { firm, firmId } = useSelectedFirm();
  const { data: statement, isLoading } = useTruckOwnerStatement(id, firmId);

  if (isLoading || !statement || !owner) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  return (
    <PrintDocument
      firm={firm}
      docLabel="Truck Owner Ledger Statement"
      docId={`STMT-TO-${owner.id.slice(0, 8)}`}
      pdfFilename={`TruckOwnerStatement-${owner.name}`}
      backHref="/truck-owner-ledger"
    >
      <div className="mb-3 flex items-baseline justify-between rounded border border-[#e5e8eb] bg-background px-3 py-2">
        <b className="text-navy">Truck Owner: {owner.name}</b>
        {owner.phone && <span>Mob: {owner.phone}</span>}
      </div>

      <table className="w-full border-collapse text-xs">
        <thead>
          <tr className="bg-navy text-[10.5px] uppercase text-white">
            <Th>Date</Th>
            <Th>Particulars</Th>
            <Th>Reference</Th>
            <Th align="right">Freight</Th>
            <Th align="right">Advance / Paid</Th>
            <Th align="right">Balance</Th>
          </tr>
        </thead>
        <tbody>
          {statement.lines.map((line, i) => (
            <tr key={i}>
              <Td>{formatDate(line.date)}</Td>
              <Td>{line.particulars}</Td>
              <Td>{line.reference ?? "—"}</Td>
              <Td align="right">{Number(line.debit) > 0 ? rupees(line.debit) : "—"}</Td>
              <Td align="right">{Number(line.credit) > 0 ? rupees(line.credit) : "—"}</Td>
              <Td align="right">{rupees(line.balance)}</Td>
            </tr>
          ))}
          {statement.lines.length === 0 && (
            <tr>
              <Td colSpan={6}>No transactions in this period.</Td>
            </tr>
          )}
        </tbody>
      </table>

      <div className="my-3 flex justify-end">
        <div className="w-64 text-[12px]">
          <SummaryRow label="Total Freight" value={rupees(statement.total_freight)} />
          <SummaryRow label="Total Advance (at loading)" value={rupees(statement.total_advance)} />
          <SummaryRow label="Total Paid" value={rupees(statement.total_paid)} />
          <SummaryRow label="Closing Balance" value={rupees(statement.closing_balance)} emphasize />
        </div>
      </div>
    </PrintDocument>
  );
}

function Th({ children, align }: { children: React.ReactNode; align?: "right" }) {
  return (
    <th className={`border border-border px-1.5 py-1.5 ${align === "right" ? "text-right" : "text-left"}`}>
      {children}
    </th>
  );
}
function Td({
  children,
  align,
  colSpan,
}: {
  children: React.ReactNode;
  align?: "right";
  colSpan?: number;
}) {
  return (
    <td
      colSpan={colSpan}
      className={`border border-border px-1.5 py-1.5 ${align === "right" ? "text-right" : "text-left"}`}
    >
      {children}
    </td>
  );
}
function SummaryRow({ label, value, emphasize }: { label: string; value: string; emphasize?: boolean }) {
  return (
    <div
      className={`flex justify-between border-b border-[#e5e8eb] py-1 ${emphasize ? "font-bold text-navy" : ""}`}
    >
      <span>{label}</span>
      <span>{value}</span>
    </div>
  );
}
