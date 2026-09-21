import * as React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useLoadingSlip } from "@/api/loadingSlips";
import { useFirms } from "@/api/firms";
import { Button } from "@/components/ui/button";
import { rupees } from "@/lib/money";

/** Direct port of loadingSlipPrintView() from the retired concept/index.html
 * -- including the bilingual (Hindi) loading-instruction sentence, which is
 * the operative instruction to the driver/munshi and isn't cosmetic.
 */
export function LoadingSlipPrintView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: s, isLoading } = useLoadingSlip(id);
  const { data: firms } = useFirms();
  const firm = firms?.find((f) => f.id === s?.firm_id);

  React.useEffect(() => {
    if (s) document.title = `LoadingSlip-${s.vehicle.vehicle_no}-${s.slip_date}`;
    return () => {
      document.title = "Transport Management System";
    };
  }, [s]);

  if (isLoading || !s) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  const advanceAmount = Number(s.advance_amount);

  return (
    <div className="mx-auto max-w-3xl">
      <div className="no-print mb-4 flex flex-col gap-2 rounded border border-border bg-white p-4">
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => navigate("/loading-slips")}>
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
          <div className="mt-0.5 text-[11px] uppercase tracking-wide opacity-85">
            लोडिंग स्लिप — Loading Slip
          </div>
          {firm?.address && <div className="mt-1.5 text-[11.5px] opacity-90">{firm.address}</div>}
        </div>

        <div className="px-5 py-4 text-[13px]">
          <Row
            left={s.agent ? `Through: ${s.agent.name}` : ""}
            right={firm?.phone ? `Mob: ${firm.phone}` : ""}
          />

          <div className="my-2.5 flex items-baseline justify-between rounded border border-[#e5e8eb] bg-background px-3 py-2">
            <b className="text-navy">Loading Instruction</b>
            <span>Date: {s.slip_date}</span>
          </div>

          {s.truck_owner && (
            <div className="my-2.5 rounded border border-border px-2.5 py-2">
              <b className="mb-1 block text-[10px] uppercase tracking-wide text-navy">
                M/s (Truck Owner)
              </b>
              {s.truck_owner.name}
            </div>
          )}

          <p className="my-3 rounded border border-dashed border-border bg-[#fbfcfd] px-3 py-2.5 text-[13px] leading-relaxed">
            आपके पास गाड़ी क्र. <b>{s.vehicle.vehicle_no}</b> जा रही है, इसमें{" "}
            <b>{s.goods_description}</b> का <b>{s.quantity_weight}</b> चढ़ (कट्टी{" "}
            {s.package_count || "—"}) लोड करवाने की कृपा करें।
          </p>

          <Row left={`From: ${s.loading_point}`} right={`To: ${s.destination}`} />

          {advanceAmount > 0 && <Row left={`Advance: ${rupees(s.advance_amount)}`} right="" />}
          {s.advance_note && <Row left={`Notes: ${s.advance_note}`} right="" />}

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
