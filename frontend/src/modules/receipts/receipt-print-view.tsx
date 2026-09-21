import { useParams } from "react-router-dom";
import { useReceipt } from "@/api/receipts";
import { useBilti } from "@/api/bilties";
import { useFirms } from "@/api/firms";
import { rupees } from "@/lib/money";
import { PrintDocument, Field, FieldRow } from "@/components/print/print-document";

/** Body content only -- letterhead/signatures/footer come from
 * PrintDocument. ReceiptRead has no expanded `bilti` object (just
 * bilti_id), so this fetches the Bilti separately by id to show GR
 * no./vehicle/consignor/consignee.
 */
export function ReceiptPrintView() {
  const { id } = useParams();
  const { data: r, isLoading } = useReceipt(id);
  const { data: b } = useBilti(r?.bilti_id);
  const { data: firms } = useFirms();
  const firm = firms?.find((f) => f.id === r?.firm_id);

  if (isLoading || !r) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  return (
    <PrintDocument
      firm={firm}
      docLabel="Final Receipt"
      docId={`RCPT-${r.id.slice(0, 8)}`}
      pdfFilename={`Receipt-${r.received_from}-${r.receipt_date}`}
      backHref="/receipts"
    >
      <div className="my-2.5 flex items-baseline justify-between rounded border border-[#e5e8eb] bg-background px-3 py-2">
        <b className="text-navy">Receipt</b>
        <span>Date: {r.receipt_date}</span>
      </div>

      <FieldRow
        left={<Field label="Received From" value={r.received_from} />}
        right={<Field label="Amount" value={rupees(r.amount)} />}
      />

      {b && (
        <>
          <FieldRow
            left={<Field label="Against Bilti / GR No." value={b.bilti_no} />}
            right={<Field label="Vehicle" value={b.vehicle.vehicle_no} />}
          />
          <FieldRow
            left={<Field label="Consignor" value={b.consignor} />}
            right={<Field label="Consignee" value={b.consignee} />}
          />
        </>
      )}

      {r.remarks && <FieldRow left={<Field label="Remarks" value={r.remarks} />} />}
    </PrintDocument>
  );
}
