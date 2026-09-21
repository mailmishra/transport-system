import * as React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useReceipt } from "@/api/receipts";
import { useBilti } from "@/api/bilties";
import { useFirms } from "@/api/firms";
import { Button } from "@/components/ui/button";
import { rupees } from "@/lib/money";

/** Direct port of receiptPrintView() from the retired concept/index.html.
 * ReceiptRead has no expanded `bilti` object (just bilti_id), so unlike
 * concept -- which already had every Bilti loaded in memory -- this fetches
 * the Bilti separately by id to show GR no./vehicle/consignor/consignee.
 */
export function ReceiptPrintView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: r, isLoading } = useReceipt(id);
  const { data: b } = useBilti(r?.bilti_id);
  const { data: firms } = useFirms();
  const firm = firms?.find((f) => f.id === r?.firm_id);

  React.useEffect(() => {
    if (r) document.title = `Receipt-${r.received_from}-${r.receipt_date}`;
    return () => {
      document.title = "Transport Management System";
    };
  }, [r]);

  if (isLoading || !r) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  return (
    <div className="mx-auto max-w-3xl">
      <div className="no-print mb-4 flex flex-col gap-2 rounded border border-border bg-white p-4">
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => navigate("/receipts")}>
            ← Back
          </Button>
          <Button variant="primary" onClick={() => window.print()}>
            Download / Print (PDF)
          </Button>
        </div>
        <p className="text-xs text-muted">
          In the print dialog, choose "Save as PDF" as the destination to download a file you
          can share on WhatsApp/email.
        </p>
      </div>

      <div className="overflow-hidden rounded border border-border bg-white shadow-sm">
        <div className="bg-navy px-6 py-5 text-center text-white">
          <h2 className="text-2xl font-extrabold tracking-wide">{firm?.name ?? ""}</h2>
          <div className="mt-0.5 text-[11px] uppercase tracking-wide opacity-85">Final Receipt</div>
          {firm?.address && <div className="mt-1.5 text-[11.5px] opacity-90">{firm.address}</div>}
        </div>

        <div className="px-5 py-4 text-[13px]">
          <Row
            left={firm?.pan_no ? `PAN: ${firm.pan_no}` : ""}
            right={firm?.phone ? `Mob: ${firm.phone}` : ""}
          />

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

          <div className="mt-5 border-t border-dashed border-border pt-3 text-center text-[11px] italic text-muted">
            This is a system-generated document and does not require a signature.
          </div>
        </div>
      </div>
    </div>
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
