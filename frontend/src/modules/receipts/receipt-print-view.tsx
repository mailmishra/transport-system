import { useParams } from "react-router-dom";
import { useReceipt } from "@/api/receipts";
import { useBilti } from "@/api/bilties";
import { useFirms } from "@/api/firms";
import { rupees } from "@/lib/money";
import { PrintDocument } from "@/components/print/print-document";

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

      <Row left={`Received From: ${r.received_from}`} right={`Amount: ${rupees(r.amount)}`} />

      {b && (
        <>
          <Row left={`Against Bilti / GR No.: ${b.bilti_no}`} right={`Vehicle: ${b.vehicle.vehicle_no}`} />
          <Row left={`Consignor: ${b.consignor}`} right={`Consignee: ${b.consignee}`} />
        </>
      )}

      {r.remarks && <Row left={`Remarks: ${r.remarks}`} right="" />}
    </PrintDocument>
  );
}

function Row({ left, right }: { left: string; right: string }) {
  if (!left && !right) return null;
  return (
    <div className="my-1.5 flex justify-between text-[12.5px]">
      <span>{left}</span>
      <span>{right}</span>
    </div>
  );
}
