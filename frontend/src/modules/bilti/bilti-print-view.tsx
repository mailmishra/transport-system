import * as React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useBiltiPrint } from "@/api/bilties";
import { useFirms } from "@/api/firms";
import { Button } from "@/components/ui/button";
import { rupees } from "@/lib/money";
import type { GstPaidBy } from "@/api/types";

const GST_OPTIONS: GstPaidBy[] = ["consignor", "consignee", "transporter", "exempted"];

/** Direct port of biltiPrintView() from the retired concept/index.html.
 * FD is never rendered here -- BiltiPrint (from GET /bilties/{id}/print)
 * omits freight_difference server-side, same hidden-field rule as before.
 * window.print() + @page CSS (src/index.css) -> the browser's native
 * "Save as PDF" is still the download path, no PDF library added.
 */
export function BiltiPrintView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: b, isLoading } = useBiltiPrint(id);
  const { data: firms } = useFirms();
  const firm = firms?.find((f) => f.id === b?.firm_id);

  React.useEffect(() => {
    if (b) document.title = `Bilti-${b.bilti_no}`;
    return () => {
      document.title = "Transport Management System";
    };
  }, [b]);

  if (isLoading || !b) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  const insuranceShown = b.insured || b.insurance_company || b.insurance_policy_no;
  const bankShown = firm?.bank_name || firm?.bank_account_no;

  return (
    <div className="mx-auto max-w-3xl">
      <div className="no-print mb-4 flex flex-col gap-2 rounded border border-border bg-white p-4">
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => navigate("/bilti")}>
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
            All Subject to Local Jurisdiction
          </div>
          {firm?.address && <div className="mt-1.5 text-[11.5px] opacity-90">{firm.address}</div>}
        </div>

        <div className="px-5 py-4 text-[13px]">
          <div className="mb-2.5 flex justify-between border-b border-[#e5e8eb] pb-2 text-[11.5px] text-muted">
            <span>
              {firm?.pan_no && `PAN: ${firm.pan_no}`}
              {firm?.email && ` · ${firm.email}`}
            </span>
            <span>{firm?.phone && `Mob: ${firm.phone}`}</span>
          </div>

          <div className="mb-2.5 flex items-baseline justify-between rounded border border-[#e5e8eb] bg-background px-3 py-2">
            <b className="text-navy">GR No.: {b.bilti_no}</b>
            <span>Date: {b.bilti_date}</span>
          </div>

          <Row left={`From: ${b.from_location}`} right={`To: ${b.to_location}`} />
          <Row
            left={`Truck No.: ${b.vehicle.vehicle_no}`}
            right={b.palti_vehicle ? `Palti Vehicle No.: ${b.palti_vehicle.vehicle_no}` : ""}
          />

          <div className="my-2.5 grid grid-cols-2 gap-2.5">
            <Box label="Consignor">{b.consignor}</Box>
            <Box label="Consignee">{b.consignee}</Box>
          </div>

          <table className="my-2.5 w-full border-collapse text-xs">
            <thead>
              <tr className="bg-navy text-[10.5px] uppercase text-white">
                <Th>Package</Th>
                <Th>Description</Th>
                <Th>Weight (Actual)</Th>
                <Th>Weight (Charged)</Th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <Td>{[b.package_count, b.package_unit].filter(Boolean).join(" ")}</Td>
                <Td>{b.goods_description}</Td>
                <Td>{b.weight}</Td>
                <Td>{b.charged_weight || b.weight}</Td>
              </tr>
            </tbody>
          </table>

          <table className="my-2.5 w-full border-collapse text-xs">
            <thead>
              <tr className="bg-navy text-[10.5px] uppercase text-white">
                <Th>Freight</Th>
                <Th>Other Ch.</Th>
                <Th>Kanta Ch.</Th>
                <Th>Bahi Ch.</Th>
                <Th>Service Tax</Th>
                <Th>Hamali</Th>
                <Th>P.Freight</Th>
                <Th>Dalali</Th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <Td>
                  {rupees(b.freight)}
                  {b.freight_rate && ` (@${rupees(b.freight_rate)})`}
                </Td>
                <Td>{rupees(b.other_charges)}</Td>
                <Td>{rupees(b.kanta_charges)}</Td>
                <Td>{rupees(b.bahi_charges)}</Td>
                <Td>{rupees(b.service_tax)}</Td>
                <Td>{rupees(b.hamali)}</Td>
                <Td>{rupees(b.p_freight)}</Td>
                <Td>{rupees(b.dalali)}</Td>
              </tr>
              <TotalRow label="Grand Total" value={rupees(b.grand_total)} span={6} />
              <TotalRow label="Advance" value={rupees(b.advance_to_owner)} span={6} />
              <TotalRow label="To Pay" value={rupees(b.topay)} span={6} />
            </tbody>
          </table>

          <div className="my-2.5 flex items-center gap-4 text-[11.5px]">
            <b className="text-navy">GST Paid By:</b>
            {GST_OPTIONS.map((o) => (
              <label key={o} className="flex items-center gap-1">
                <input type="checkbox" readOnly checked={b.gst_paid_by === o} />
                {o[0].toUpperCase() + o.slice(1)}
              </label>
            ))}
          </div>

          {insuranceShown && (
            <div className="my-2.5 rounded border border-dashed border-border bg-[#fbfcfd] px-3 py-2 text-[11.5px]">
              <b className="text-navy">Insurance</b> {b.insured ? "Insured" : "Not insured / at owner's risk"}
              {b.insurance_company && ` · Company: ${b.insurance_company}`}
              {b.insurance_policy_no && ` · Policy No: ${b.insurance_policy_no}`}
              {b.insurance_amount && ` · Amount: ${rupees(b.insurance_amount)}`}
              {b.insurance_date && ` · Date: ${b.insurance_date}`}
              {b.insurance_risk && ` · Risk: ${b.insurance_risk}`}
              {b.insurance_agent_name && ` · Insurance Agent: ${b.insurance_agent_name}`}
            </div>
          )}

          <Row
            left={`Truck Owner: ${b.truck_owner.name}`}
            right={b.goods_value_declared ? `Value: ${rupees(b.goods_value_declared)}` : ""}
          />
          <Row
            left={b.agent ? `Agent / Broker: ${b.agent.name}` : ""}
            right={b.eway_bill_no ? `E-Way Bill: ${b.eway_bill_no}` : ""}
          />
          {b.invoice_value && <Row left={`Invoice Value: ${rupees(b.invoice_value)}`} right="" />}
          {b.remark && <Row left={`Remark: ${b.remark}`} right="" />}

          <div className="mt-5 border-t border-dashed border-border pt-3 text-center text-[11px] italic text-muted">
            This is a system-generated document and does not require a signature.
          </div>
        </div>

        {bankShown && (
          <div className="border-t border-[#e5e8eb] bg-background px-5 py-2 text-[10.5px] text-[#3d4952]">
            Bank: {firm?.bank_name} {firm?.bank_branch && `(${firm.bank_branch})`} · A/c No.:{" "}
            {firm?.bank_account_no} · IFSC: {firm?.bank_ifsc}
          </div>
        )}
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

function Box({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="rounded border border-border px-2.5 py-2">
      <b className="mb-1 block text-[10px] uppercase tracking-wide text-navy">{label}</b>
      {children}
    </div>
  );
}

function Th({ children }: { children: React.ReactNode }) {
  return <th className="border border-border px-1.5 py-1.5 text-left">{children}</th>;
}
function Td({ children }: { children: React.ReactNode }) {
  return <td className="border border-border px-1.5 py-1.5">{children}</td>;
}
function TotalRow({ label, value, span }: { label: string; value: string; span: number }) {
  return (
    <tr className="bg-background font-bold">
      <td colSpan={span} className="border border-border" />
      <td className="border border-border px-1.5 py-1.5">{label}</td>
      <td className="border border-border px-1.5 py-1.5">{value}</td>
    </tr>
  );
}
