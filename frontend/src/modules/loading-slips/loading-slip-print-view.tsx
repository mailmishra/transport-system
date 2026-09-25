import { useParams } from "react-router-dom";
import { useLoadingSlip } from "@/api/loadingSlips";
import { useFirms } from "@/api/firms";
import { rupees } from "@/lib/money";
import { PrintDocument, Field, FieldRow } from "@/components/print/print-document";

/** Body content only -- letterhead/footer come from PrintDocument. Keeps
 * the bilingual (Hindi) loading-instruction sentence, which is the
 * operative instruction to the driver/munshi and isn't cosmetic. No
 * signature block: an internal dispatch note, not countersigned by an
 * external party.
 */
export function LoadingSlipPrintView() {
  const { id } = useParams();
  const { data: s, isLoading } = useLoadingSlip(id);
  const { data: firms } = useFirms();
  const firm = firms?.find((f) => f.id === s?.firm_id);

  if (isLoading || !s) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  const advanceAmount = Number(s.advance_amount);

  return (
    <PrintDocument
      firm={firm}
      docLabel="Loading Slip"
      docId={`LS-${s.vehicle.vehicle_no}-${s.slip_date}`}
      pdfFilename={`LoadingSlip-${s.vehicle.vehicle_no}-${s.slip_date}`}
      backHref="/loading-slips"
      showSignatures={false}
    >
      {s.agent && <FieldRow left={<Field label="Through" value={s.agent.name} />} />}

      <div className="my-2.5 flex items-baseline justify-between rounded border border-[#e5e8eb] bg-background px-3 py-2">
        <b className="text-navy">Loading Instruction</b>
        <span>Date: {s.slip_date}</span>
      </div>

      {s.truck_owner && (
        <div className="my-2.5 rounded border border-border px-2.5 py-2">
          <b className="mb-1 block text-[10px] uppercase tracking-wide text-navy">M/s (Truck Owner)</b>
          {s.truck_owner.name}
        </div>
      )}

      {s.factory_name && (
        <div className="my-2.5 rounded border border-border px-2.5 py-2">
          <b className="mb-1 block text-[10px] uppercase tracking-wide text-navy">M/s (Destination Factory / Party)</b>
          {s.factory_name}
        </div>
      )}

      <p className="my-3 rounded border border-dashed border-border bg-[#fbfcfd] px-3 py-2.5 text-[13px] leading-relaxed">
        आपके पास गाड़ी क्र. <b>{s.vehicle.vehicle_no}</b> जा रही है, इसमें <b>{s.goods_description}</b> का{" "}
        <b>{s.quantity_weight}</b> चढ़ (कट्टी {s.package_count || "—"}) लोड करवाने की कृपा करें।{" "}
        गंतव्य: <b>{s.destination}</b>।
      </p>

      <FieldRow left={<Field label="From" value={s.loading_point} />} right={<Field label="To" value={s.destination} />} />

      {advanceAmount > 0 && <FieldRow left={<Field label="Advance" value={rupees(s.advance_amount)} />} />}
      {s.advance_note && <FieldRow left={<Field label="Notes" value={s.advance_note} />} />}
    </PrintDocument>
  );
}
