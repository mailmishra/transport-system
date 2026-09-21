import { useParams } from "react-router-dom";
import { useAgent, useAgentStatement } from "@/api/agents";
import { useSelectedFirm } from "@/state/selected-firm";
import { rupees } from "@/lib/money";
import { formatDate } from "@/lib/dates";
import { PrintDocument } from "@/components/print/print-document";

/** Ledger Statement PDF -- the shared shell (PrintDocument) applied to a
 * multi-row tabular document instead of a single record, per the Reports +
 * PDF template plan's Phase 2. Data comes from GET /agents/{id}/statement,
 * which already computes the chronological running balance server-side
 * (same "compute don't duplicate" rule as the balance endpoint).
 */
export function AgentLedgerPrintView() {
  const { id } = useParams();
  const { data: agent } = useAgent(id);
  const { firm, firmId } = useSelectedFirm();
  const { data: statement, isLoading } = useAgentStatement(id, firmId);

  if (isLoading || !statement || !agent) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  return (
    <PrintDocument
      firm={firm}
      docLabel="Agent Ledger Statement"
      docId={`STMT-AGT-${agent.id.slice(0, 8)}`}
      pdfFilename={`AgentStatement-${agent.name}`}
      backHref="/agent-ledger"
    >
      <div className="mb-3 flex items-baseline justify-between rounded border border-[#e5e8eb] bg-background px-3 py-2">
        <b className="text-navy">Agent: {agent.name}</b>
        {agent.phone && <span>Mob: {agent.phone}</span>}
      </div>

      <table className="w-full border-collapse text-xs">
        <thead>
          <tr className="bg-navy text-[10.5px] uppercase text-white">
            <Th>Date</Th>
            <Th>Particulars</Th>
            <Th>Reference</Th>
            <Th align="right">Accrued</Th>
            <Th align="right">Paid</Th>
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
          <SummaryRow label="Total Accrued" value={rupees(statement.total_accrued)} />
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
