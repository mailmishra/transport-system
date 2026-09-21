import * as React from "react";
import { useNavigate } from "react-router-dom";
import { Controller, useForm } from "react-hook-form";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/ui/field-error";
import { Section, Field } from "@/components/form/section";
import { AsyncCombobox } from "@/components/combobox/async-combobox";
import { useBiltiSearch } from "@/api/bilties";
import { useCreateReceipt } from "@/api/receipts";
import { useFirms } from "@/api/firms";
import { ApiError } from "@/api/client";
import type { Bilti, ReceiptCreateInput } from "@/api/types";
import { rupees } from "@/lib/money";
import { todayIso } from "@/lib/dates";

interface FormValues {
  bilti_label: string;
  receipt_date: string;
  received_from: string;
  amount: string;
  remarks: string;
}

const EMPTY: FormValues = {
  bilti_label: "",
  receipt_date: todayIso(),
  received_from: "",
  amount: "",
  remarks: "",
};

/** Receipts have no PATCH endpoint (backend/app/routers/receipts.py: create
 * or delete-and-recreate only, same as Agent/TruckOwner Payments) -- this
 * drawer is create-only, unlike Bilti/LoadingSlip's create-or-edit form.
 */
export function ReceiptFormDrawer() {
  const navigate = useNavigate();
  const { data: firms } = useFirms();
  const firmId = firms?.[0]?.id;
  const createReceipt = useCreateReceipt();
  const [selectedBilti, setSelectedBilti] = React.useState<Bilti | null>(null);

  const {
    register,
    handleSubmit,
    control,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ defaultValues: EMPTY });

  const close = () => navigate(-1);

  const onSubmit = handleSubmit(async (values) => {
    if (!firmId) return;
    if (!selectedBilti) {
      setError("bilti_label", { message: "Pick a Bilti / GR from the list" });
      return;
    }
    const payload: ReceiptCreateInput = {
      firm_id: firmId,
      bilti_id: selectedBilti.id,
      amount: Number(values.amount),
      receipt_date: values.receipt_date,
      received_from: values.received_from,
      remarks: values.remarks || null,
    };

    try {
      const created = await createReceipt.mutateAsync(payload);
      navigate(`/receipts/${created.id}/print`);
    } catch (e) {
      if (e instanceof ApiError) {
        setError("root", { message: e.message });
      }
    }
  });

  return (
    <Sheet open onOpenChange={(open) => !open && close()}>
      <SheetContent title="New Receipt">
        <form onSubmit={onSubmit} className="flex flex-1 flex-col overflow-hidden">
          <div className="flex-1 space-y-4 overflow-y-auto px-5 py-4">
            <FormError message={errors.root?.message} />

            <Section title="Against Bilti / GR">
              <Field label="Bilti / GR" error={errors.bilti_label?.message}>
                <Controller
                  control={control}
                  name="bilti_label"
                  rules={{ required: "Required" }}
                  render={({ field }) => (
                    <AsyncCombobox
                      value={field.value}
                      onChange={(v) => {
                        field.onChange(v);
                        setSelectedBilti(null);
                      }}
                      onSelectItem={setSelectedBilti}
                      useSearch={useBiltiSearch}
                      getLabel={(b) => `${b.bilti_no} — ${b.consignor}`}
                      getSubtitle={(b) => `${rupees(b.freight)} · ${b.vehicle.vehicle_no}`}
                      invalid={!!errors.bilti_label}
                      placeholder="Search GR no. or consignor…"
                    />
                  )}
                />
              </Field>
              {selectedBilti && (
                <div className="rounded border border-border bg-background px-3 py-2 text-xs text-muted">
                  Freight: {rupees(selectedBilti.freight)} · To Pay: {rupees(selectedBilti.topay)}
                </div>
              )}
            </Section>

            <Section title="Receipt">
              <Field label="Receipt Date" error={errors.receipt_date?.message}>
                <Input type="date" invalid={!!errors.receipt_date} {...register("receipt_date", { required: "Required" })} />
              </Field>
              <Field label="Received From" error={errors.received_from?.message}>
                <Input invalid={!!errors.received_from} {...register("received_from", { required: "Required" })} />
              </Field>
              <Field label="Amount" error={errors.amount?.message}>
                <Input
                  type="number"
                  step="0.01"
                  invalid={!!errors.amount}
                  {...register("amount", { required: "Required", min: { value: 0.01, message: "Must be > 0" } })}
                />
              </Field>
              <Field label="Remarks">
                <Input {...register("remarks")} />
              </Field>
            </Section>
          </div>

          <div className="flex gap-2 border-t border-border px-5 py-4">
            <Button type="button" variant="secondary" className="flex-1" onClick={close}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" className="flex-[2]" disabled={isSubmitting}>
              {isSubmitting ? "Saving…" : "Save & Print Receipt"}
            </Button>
          </div>
        </form>
      </SheetContent>
    </Sheet>
  );
}
