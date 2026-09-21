import * as React from "react";
import { useParams } from "react-router-dom";
import { useBiltiPrint } from "@/api/bilties";
import { useFirms } from "@/api/firms";
import { rupees } from "@/lib/money";
import { PrintDocument, Field, FieldRow } from "@/components/print/print-document";
import type { GstPaidBy } from "@/api/types";

const GST_OPTIONS: GstPaidBy[] = ["consignor", "consignee", "transporter", "exempted"];

/** Body content only -- letterhead, signatures and footer come from
 * PrintDocument. FD is never rendered here -- BiltiPrint (from
 * GET /bilties/{id}/print) omits freight_difference server-side, same
 * hidden-field rule as before.
 */
export function BiltiPrintView() {
  const { id } = useParams();
  const { data: b, isLoading } = useBiltiPrint(id);
  const { data: firms } = useFirms();
  const firm = firms?.find((f) => f.id === b?.firm_id);

  if (isLoading || !b) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  const insuranceShown = b.insured || b.insurance_company || b.insurance_policy_no;

  return (
    <PrintDocument
      firm={firm}
      docLabel="Goods Consignment Note (Bilti / GR)"
      docId={`GR-${b.bilti_no}`}
      pdfFilename={`Bilti-${b.bilti_no}`}
      backHref="/bilti"
    >
      <div className="mb-2.5 flex items-baseline justify-between rounded border border-[#e5e8eb] bg-background px-3 py-2">
        <b className="text-navy">GR No.: {b.bilti_no}</b>
        <span>Date: {b.bilti_date}</span>
      </div>

      <FieldRow left={<Field label="From" value={b.from_location} />} right={<Field label="To" value={b.to_location} />} />
      <FieldRow
        left={<Field label="Truck No." value={b.vehicle.vehicle_no} />}
        right={b.palti_vehicle && <Field label="Palti Vehicle No." value={b.palti_vehicle.vehicle_no} />}
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

      <FieldRow
        left={<Field label="Truck Owner" value={b.truck_owner.name} />}
        right={b.goods_value_declared && <Field label="Value" value={rupees(b.goods_value_declared)} />}
      />
      <FieldRow
        left={b.agent && <Field label="Agent / Broker" value={b.agent.name} />}
        right={b.eway_bill_no && <Field label="E-Way Bill" value={b.eway_bill_no} />}
      />
      {b.invoice_value && <FieldRow left={<Field label="Invoice Value" value={rupees(b.invoice_value)} />} />}
      {b.remark && <FieldRow left={<Field label="Remark" value={b.remark} />} />}
    </PrintDocument>
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
