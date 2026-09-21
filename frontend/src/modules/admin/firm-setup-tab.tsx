import * as React from "react";
import { useForm } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/ui/field-error";
import { useFirms, useUpdateFirm, useUploadFirmLogo } from "@/api/firms";
import { ApiError } from "@/api/client";
import type { Firm } from "@/api/types";

interface FormValues {
  address: string;
  phone: string;
  email: string;
  pan_no: string;
  gstin: string;
  signatory_name: string;
  signatory_designation: string;
  jurisdiction_text: string;
  bank_name: string;
  bank_branch: string;
  bank_account_no: string;
  bank_ifsc: string;
}

const EMPTY_VALUES: FormValues = {
  address: "", phone: "", email: "", pan_no: "", gstin: "",
  signatory_name: "", signatory_designation: "", jurisdiction_text: "",
  bank_name: "", bank_branch: "", bank_account_no: "", bank_ifsc: "",
};

/** Single-firm setup -- Phase 1's AppShell already hardcodes firms?.[0] as
 * "the" firm with no switcher UI, so this edits that same firm rather than
 * reintroducing concept/index.html's firm-switcher (multi-firm switching
 * was never carried into the React app; out of scope here too). firm.name
 * is not editable -- FirmUpdate excludes it (Firm.name is unique in the DB).
 *
 * This is the source of everything PrintDocument (components/print/) puts
 * on a printed document's letterhead -- the live preview below mirrors
 * that shell so the effect of each field is visible before printing
 * anything.
 */
export function FirmSetupTab() {
  const { data: firms } = useFirms();
  const firm = firms?.[0];
  const updateFirm = useUpdateFirm();
  const uploadLogo = useUploadFirmLogo();
  const [logoError, setLogoError] = React.useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setError,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<FormValues>({ defaultValues: EMPTY_VALUES });

  React.useEffect(() => {
    if (firm) reset(toFormValues(firm));
  }, [firm, reset]);

  const preview = watch();

  if (!firm) {
    return <div className="p-6 text-sm text-muted">Loading…</div>;
  }

  const onSubmit = handleSubmit(async (values) => {
    try {
      await updateFirm.mutateAsync({
        id: firm.id,
        data: {
          address: values.address || null,
          phone: values.phone || null,
          email: values.email || null,
          pan_no: values.pan_no || null,
          gstin: values.gstin || null,
          signatory_name: values.signatory_name || null,
          signatory_designation: values.signatory_designation || null,
          jurisdiction_text: values.jurisdiction_text || null,
          bank_name: values.bank_name || null,
          bank_branch: values.bank_branch || null,
          bank_account_no: values.bank_account_no || null,
          bank_ifsc: values.bank_ifsc || null,
        },
      });
    } catch (e) {
      if (e instanceof ApiError) setError("root", { message: e.message });
    }
  });

  const onLogoChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setLogoError(null);
    try {
      await uploadLogo.mutateAsync({ id: firm.id, file });
    } catch (err) {
      setLogoError(err instanceof ApiError ? err.message : "Logo upload failed");
    }
  };

  return (
    <div className="grid max-w-5xl grid-cols-1 gap-5 lg:grid-cols-[minmax(0,1fr)_320px]">
      <form onSubmit={onSubmit} className="space-y-4 rounded border border-border bg-white p-5">
        <FormError message={errors.root?.message} />

        <div>
          <Label>Firm Name</Label>
          <Input className="mt-1" value={firm.name} disabled />
        </div>

        <div className="border-t border-border pt-4">
          <h3 className="mb-3 text-[11px] font-bold uppercase tracking-wide text-navy">Logo</h3>
          <div className="flex items-center gap-3">
            <div className="flex h-14 w-14 flex-shrink-0 items-center justify-center overflow-hidden rounded border border-border bg-background">
              {firm.logo_url ? (
                <img src={firm.logo_url} alt="" className="h-full w-full object-contain p-1" />
              ) : (
                <span className="text-[9px] text-muted">No logo</span>
              )}
            </div>
            <div>
              <label className="inline-block cursor-pointer rounded border border-border bg-white px-3 py-1.5 text-sm font-medium hover:bg-background">
                {uploadLogo.isPending ? "Uploading…" : firm.logo_url ? "Replace logo" : "Upload logo"}
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/webp,image/svg+xml"
                  className="hidden"
                  onChange={onLogoChange}
                  disabled={uploadLogo.isPending}
                />
              </label>
              <p className="mt-1 text-xs text-muted">PNG, JPEG, WebP, or SVG · up to 2MB</p>
              <FormError message={logoError} />
            </div>
          </div>
        </div>

        <div>
          <Label>Address</Label>
          <Input className="mt-1" {...register("address")} />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label>Phone</Label>
            <Input className="mt-1" {...register("phone")} />
          </div>
          <div>
            <Label>Email</Label>
            <Input className="mt-1" type="email" {...register("email")} />
          </div>
        </div>

        <div className="border-t border-border pt-4">
          <h3 className="mb-3 text-[11px] font-bold uppercase tracking-wide text-navy">Compliance</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <Label>PAN No.</Label>
              <Input className="mt-1" {...register("pan_no")} />
            </div>
            <div>
              <Label>GSTIN</Label>
              <Input className="mt-1" {...register("gstin")} />
            </div>
          </div>
        </div>

        <div className="border-t border-border pt-4">
          <h3 className="mb-3 text-[11px] font-bold uppercase tracking-wide text-navy">
            Printed Document Defaults
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <Label>Authorised Signatory Name</Label>
              <Input className="mt-1" {...register("signatory_name")} />
            </div>
            <div>
              <Label>Signatory Designation</Label>
              <Input className="mt-1" placeholder="e.g. Proprietor" {...register("signatory_designation")} />
            </div>
          </div>
          <div className="mt-3">
            <Label>Jurisdiction Clause</Label>
            <Input
              className="mt-1"
              placeholder="All disputes subject to __ jurisdiction only"
              {...register("jurisdiction_text")}
            />
          </div>
        </div>

        <div className="border-t border-border pt-4">
          <h3 className="mb-3 text-[11px] font-bold uppercase tracking-wide text-navy">Bank Details</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <Label>Bank Name</Label>
              <Input className="mt-1" {...register("bank_name")} />
            </div>
            <div>
              <Label>Bank Branch</Label>
              <Input className="mt-1" {...register("bank_branch")} />
            </div>
            <div>
              <Label>Bank A/c No.</Label>
              <Input className="mt-1" {...register("bank_account_no")} />
            </div>
            <div>
              <Label>Bank IFSC</Label>
              <Input className="mt-1" {...register("bank_ifsc")} />
            </div>
          </div>
        </div>

        <Button type="submit" variant="primary" disabled={isSubmitting || !isDirty}>
          {isSubmitting ? "Saving…" : "Save Changes"}
        </Button>
      </form>

      <div className="lg:sticky lg:top-4 lg:self-start">
        <div className="mb-2 text-[11px] font-bold uppercase tracking-wide text-muted">
          Letterhead Preview
        </div>
        <LetterheadPreview firm={firm} values={preview} />
      </div>
    </div>
  );
}

/** Mirrors PrintDocument's header band (components/print/print-document.tsx)
 * at a smaller scale, live-fed by the form's current (unsaved) values --
 * so a field's effect on the printed page is visible before saving.
 */
function LetterheadPreview({ firm, values }: { firm: Firm; values: FormValues }) {
  return (
    <div className="overflow-hidden rounded border border-border bg-white shadow-sm">
      <div className="flex items-start gap-3 bg-navy px-4 py-3.5 text-white">
        <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center overflow-hidden rounded border border-white/30 bg-white/5">
          {firm.logo_url ? (
            <img src={firm.logo_url} alt="" className="h-full w-full object-contain p-0.5" />
          ) : (
            <span className="text-[7px] opacity-60">LOGO</span>
          )}
        </div>
        <div className="flex-grow">
          <div className="text-[15px] font-extrabold tracking-wide">{firm.name}</div>
          {values.address && <div className="mt-0.5 text-[9px] opacity-90">{values.address}</div>}
          {values.jurisdiction_text && (
            <div className="mt-1 text-[7.5px] uppercase tracking-wide opacity-70">
              {values.jurisdiction_text}
            </div>
          )}
        </div>
        <div className="flex-shrink-0 text-right text-[8px] leading-relaxed opacity-90">
          {values.gstin && <div>GSTIN: {values.gstin}</div>}
          {values.pan_no && <div>PAN: {values.pan_no}</div>}
          {values.phone && <div>Mob: {values.phone}</div>}
        </div>
      </div>
      <div className="flex items-center justify-between border-b-2 border-navy bg-background px-4 py-1.5">
        <div className="text-[8px] font-bold uppercase tracking-wide text-navy">
          Goods Consignment Note (Bilti / GR)
        </div>
      </div>
      <div className="px-4 py-3 text-[9px] text-muted">Document body …</div>
      <div className="flex justify-between px-4 pb-2 pt-5">
        <div className="w-[70px] border-t border-[#99a3ac] pt-1 text-center text-[7px] text-muted">
          Receiver's Signature
        </div>
        <div className="w-[90px] border-t border-[#99a3ac] pt-1 text-center text-[7px] text-muted">
          For {firm.name}
          <br />
          {values.signatory_name
            ? `${values.signatory_name}${
                values.signatory_designation ? `, ${values.signatory_designation}` : ""
              }`
            : "Authorised Signatory"}
        </div>
      </div>
      <div className="border-t border-[#e5e8eb] bg-background px-4 py-1.5 text-[7.5px] text-[#3d4952]">
        {(values.bank_name || values.bank_account_no) &&
          `Bank: ${values.bank_name} ${values.bank_branch ? `(${values.bank_branch})` : ""} · A/c No.: ${values.bank_account_no} · IFSC: ${values.bank_ifsc}`}
      </div>
    </div>
  );
}

function toFormValues(firm: Firm): FormValues {
  return {
    address: firm.address ?? "",
    phone: firm.phone ?? "",
    email: firm.email ?? "",
    pan_no: firm.pan_no ?? "",
    gstin: firm.gstin ?? "",
    signatory_name: firm.signatory_name ?? "",
    signatory_designation: firm.signatory_designation ?? "",
    jurisdiction_text: firm.jurisdiction_text ?? "",
    bank_name: firm.bank_name ?? "",
    bank_branch: firm.bank_branch ?? "",
    bank_account_no: firm.bank_account_no ?? "",
    bank_ifsc: firm.bank_ifsc ?? "",
  };
}
