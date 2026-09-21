import * as React from "react";
import { useForm } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/ui/field-error";
import { useFirms, useUpdateFirm } from "@/api/firms";
import { ApiError } from "@/api/client";
import type { Firm } from "@/api/types";

interface FormValues {
  address: string;
  phone: string;
  email: string;
  pan_no: string;
  bank_name: string;
  bank_branch: string;
  bank_account_no: string;
  bank_ifsc: string;
}

/** Single-firm setup -- Phase 1's AppShell already hardcodes firms?.[0] as
 * "the" firm with no switcher UI, so this edits that same firm rather than
 * reintroducing concept/index.html's firm-switcher (multi-firm switching
 * was never carried into the React app; out of scope here too). firm.name
 * is not editable -- FirmUpdate excludes it (Firm.name is unique in the DB).
 */
export function FirmSetupTab() {
  const { data: firms } = useFirms();
  const firm = firms?.[0];
  const updateFirm = useUpdateFirm();

  const {
    register,
    handleSubmit,
    reset,
    setError,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<FormValues>({
    defaultValues: {
      address: "", phone: "", email: "", pan_no: "",
      bank_name: "", bank_branch: "", bank_account_no: "", bank_ifsc: "",
    },
  });

  React.useEffect(() => {
    if (firm) reset(toFormValues(firm));
  }, [firm, reset]);

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

  return (
    <form onSubmit={onSubmit} className="max-w-xl space-y-4 rounded border border-border bg-white p-5">
      <FormError message={errors.root?.message} />

      <div>
        <Label>Firm Name</Label>
        <Input className="mt-1" value={firm.name} disabled />
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
      <div>
        <Label>PAN No.</Label>
        <Input className="mt-1" {...register("pan_no")} />
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
  );
}

function toFormValues(firm: Firm): FormValues {
  return {
    address: firm.address ?? "",
    phone: firm.phone ?? "",
    email: firm.email ?? "",
    pan_no: firm.pan_no ?? "",
    bank_name: firm.bank_name ?? "",
    bank_branch: firm.bank_branch ?? "",
    bank_account_no: firm.bank_account_no ?? "",
    bank_ifsc: firm.bank_ifsc ?? "",
  };
}
