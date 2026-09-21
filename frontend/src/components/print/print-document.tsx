import * as React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import type { Firm } from "@/api/types";

interface PrintDocumentProps {
  firm: Firm | undefined;
  /** Uppercase label in the title strip, e.g. "Goods Consignment Note (Bilti / GR)". */
  docLabel: string;
  /** Shown in the footer's right-hand corner, e.g. "GR-KTN-24-118842". */
  docId: string;
  /** document.title while this view is open -- also the suggested "Save as PDF" filename. */
  pdfFilename: string;
  backHref: string;
  backLabel?: string;
  /** Off for internal dispatch paperwork (Loading Slip) that isn't countersigned by an external party. */
  showSignatures?: boolean;
  children: React.ReactNode;
}

/** Shared letterhead shell for every printable document (Template A —
 * navy header band, boxed sections — approved via the PDF template review).
 * Owns everything that must look identical across document types: the
 * firm's branding, the signature block, the bank/doc-id footer, and the
 * window.print() action bar. Each print view supplies only its own body.
 */
export function PrintDocument({
  firm,
  docLabel,
  docId,
  pdfFilename,
  backHref,
  backLabel = "Back",
  showSignatures = true,
  children,
}: PrintDocumentProps) {
  const navigate = useNavigate();

  React.useEffect(() => {
    document.title = pdfFilename;
    return () => {
      document.title = "Transport Management System";
    };
  }, [pdfFilename]);

  const bankShown = firm?.bank_name || firm?.bank_account_no;

  return (
    <div className="mx-auto max-w-3xl">
      <div className="no-print mb-4 flex flex-col gap-2 rounded border border-border bg-white p-4">
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => navigate(backHref)}>
            ← {backLabel}
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
        <div className="flex items-start gap-4 bg-navy px-6 py-5 text-white">
          {firm?.logo_url && (
            <img
              src={firm.logo_url}
              alt=""
              className="h-14 w-14 flex-shrink-0 rounded border border-white/30 bg-white/5 object-contain p-1"
            />
          )}
          <div className="flex-grow" style={{ fontFamily: "Georgia, 'Times New Roman', serif" }}>
            <div className="text-2xl font-bold tracking-wide">{firm?.name ?? ""}</div>
            {firm?.address && <div className="mt-1 text-[11.5px] opacity-90">{firm.address}</div>}
            {firm?.jurisdiction_text && (
              <div className="mt-1.5 text-[10px] uppercase tracking-wide opacity-70">
                {firm.jurisdiction_text}
              </div>
            )}
          </div>
          <div className="flex-shrink-0 text-right text-[10.5px] leading-relaxed opacity-90">
            {firm?.gstin && <div>GSTIN: {firm.gstin}</div>}
            {firm?.pan_no && <div>PAN: {firm.pan_no}</div>}
            {firm?.phone && <div>Mob: {firm.phone}</div>}
          </div>
        </div>

        <div className="flex items-center justify-between border-b-2 border-navy bg-background px-6 py-2.5">
          <div className="text-[11px] font-bold uppercase tracking-wide text-navy">{docLabel}</div>
          {firm?.email && <div className="text-[10.5px] text-muted">{firm.email}</div>}
        </div>

        <div className="px-5 py-4 text-[13px]">{children}</div>

        {showSignatures && (
          <div className="flex justify-between px-5 pb-2 pt-8">
            <div className="w-[190px] border-t border-[#99a3ac] pt-1.5 text-center text-[10.5px] text-muted">
              Receiver's Signature
            </div>
            <div className="w-[190px] border-t border-[#99a3ac] pt-1.5 text-center text-[10.5px] text-muted">
              For {firm?.name ?? "the Firm"}
              <br />
              <span className="text-[9.5px]">
                {firm?.signatory_name
                  ? `${firm.signatory_name}${
                      firm.signatory_designation ? `, ${firm.signatory_designation}` : ""
                    }`
                  : "Authorised Signatory"}
              </span>
            </div>
          </div>
        )}

        <div
          className={`flex items-center justify-between border-t border-[#e5e8eb] bg-background px-5 py-2 text-[10.5px] text-[#3d4952] ${
            showSignatures ? "" : "mt-2"
          }`}
        >
          <span>
            {bankShown &&
              `Bank: ${firm?.bank_name ?? ""} ${
                firm?.bank_branch ? `(${firm.bank_branch})` : ""
              } · A/c No.: ${firm?.bank_account_no ?? ""} · IFSC: ${firm?.bank_ifsc ?? ""}`}
          </span>
          <span className="text-muted">
            Computer-generated document · {docId}
          </span>
        </div>
      </div>
    </div>
  );
}

/** A bold "Label:" against a plain value, matching the approved Template A
 * mockup's field convention (e.g. "**From:** Katni, MP") -- plain string
 * concatenation like `From: ${x}` gives the label and value identical
 * weight, which is the "no distinction" gap this exists to close. Renders
 * nothing when `value` is empty, so callers can pass it directly into a
 * conditional without an extra guard.
 */
export function Field({ label, value }: { label: string; value: React.ReactNode }) {
  if (value === null || value === undefined || value === "") return null;
  return (
    <span>
      <b className="font-semibold">{label}:</b> {value}
    </span>
  );
}

/** Two Fields (or any inline content) spaced to the document's edges --
 * the standard body-row layout throughout every print view's content. */
export function FieldRow({ left, right }: { left?: React.ReactNode; right?: React.ReactNode }) {
  if (!left && !right) return null;
  return (
    <div className="my-1.5 flex justify-between text-[12.5px]">
      <span>{left}</span>
      <span>{right}</span>
    </div>
  );
}
