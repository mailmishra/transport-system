import * as React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Controller, useForm } from "react-hook-form";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/ui/field-error";
import { Section, Field } from "@/components/form/section";
import { AsyncCombobox } from "@/components/combobox/async-combobox";
import { useVehicleSearch } from "@/api/vehicles";
import { useAgentSearch } from "@/api/agents";
import { useTruckOwnerSearch } from "@/api/truckOwners";
import { useLoadingSlip, useCreateLoadingSlip, useUpdateLoadingSlip } from "@/api/loadingSlips";
import { useFirms } from "@/api/firms";
import { ApiError } from "@/api/client";
import type { LoadingSlipCreateInput } from "@/api/types";
import { todayIso } from "@/lib/dates";

interface FormValues {
  slip_date: string;
  vehicle_no: string;
  truck_owner_name: string;
  agent_name: string;
  loading_point: string;
  destination: string;
  goods_description: string;
  quantity_weight: string;
  package_count: string;
  advance_amount: string;
  advance_note: string;
}

const EMPTY: FormValues = {
  slip_date: todayIso(),
  vehicle_no: "",
  truck_owner_name: "",
  agent_name: "",
  loading_point: "",
  destination: "",
  goods_description: "",
  quantity_weight: "",
  package_count: "",
  advance_amount: "0",
  advance_note: "",
};

const FIELD_NAMES = Object.keys(EMPTY) as Array<keyof FormValues>;

export function LoadingSlipFormDrawer() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = !!id;
  const { data: firms } = useFirms();
  const firmId = firms?.[0]?.id;
  const { data: existing } = useLoadingSlip(id);
  const createSlip = useCreateLoadingSlip();
  const updateSlip = useUpdateLoadingSlip();

  const {
    register,
    handleSubmit,
    control,
    reset,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ defaultValues: EMPTY });

  React.useEffect(() => {
    if (existing) {
      reset({
        slip_date: existing.slip_date,
        vehicle_no: existing.vehicle.vehicle_no,
        truck_owner_name: existing.truck_owner?.name ?? "",
        agent_name: existing.agent?.name ?? "",
        loading_point: existing.loading_point,
        destination: existing.destination,
        goods_description: existing.goods_description,
        quantity_weight: existing.quantity_weight,
        package_count: existing.package_count ?? "",
        advance_amount: existing.advance_amount,
        advance_note: existing.advance_note ?? "",
      });
    }
  }, [existing, reset]);

  const close = () => navigate(-1);

  const onSubmit = handleSubmit(async (values) => {
    if (!firmId) return;
    const payload: LoadingSlipCreateInput = {
      firm_id: firmId,
      slip_date: values.slip_date,
      vehicle_no: values.vehicle_no,
      truck_owner_name: values.truck_owner_name || null,
      agent_name: values.agent_name || null,
      loading_point: values.loading_point,
      destination: values.destination,
      goods_description: values.goods_description,
      quantity_weight: values.quantity_weight,
      package_count: values.package_count || null,
      advance_amount: values.advance_amount.trim() === "" ? 0 : Number(values.advance_amount),
      advance_note: values.advance_note || null,
    };

    try {
      if (isEdit && id) {
        await updateSlip.mutateAsync({ id, data: payload });
        navigate(`/loading-slips/${id}/print`);
      } else {
        const created = await createSlip.mutateAsync(payload);
        navigate(`/loading-slips/${created.id}/print`);
      }
    } catch (e) {
      if (e instanceof ApiError && e.fields) {
        let anyMapped = false;
        for (const [backendField, message] of Object.entries(e.fields)) {
          if (FIELD_NAMES.includes(backendField as keyof FormValues)) {
            setError(backendField as keyof FormValues, { message });
            anyMapped = true;
          }
        }
        if (!anyMapped) setError("root", { message: e.message });
      } else if (e instanceof ApiError) {
        setError("root", { message: e.message });
      }
    }
  });

  return (
    <Sheet open onOpenChange={(open) => !open && close()}>
      <SheetContent title={isEdit ? "Edit Loading Slip" : "New Loading Slip"}>
        <form onSubmit={onSubmit} className="flex flex-1 flex-col overflow-hidden">
          <div className="flex-1 space-y-4 overflow-y-auto px-5 py-4">
            <FormError message={errors.root?.message} />

            <Section title="Vehicle & Party">
              <Field label="Lorry / Vehicle No." error={errors.vehicle_no?.message}>
                <Controller
                  control={control}
                  name="vehicle_no"
                  rules={{ required: "Required" }}
                  render={({ field }) => (
                    <AsyncCombobox
                      value={field.value}
                      onChange={field.onChange}
                      useSearch={useVehicleSearch}
                      getLabel={(v) => v.vehicle_no}
                      invalid={!!errors.vehicle_no}
                      placeholder="MP20AB1234"
                    />
                  )}
                />
              </Field>
              <Field label="Date" error={errors.slip_date?.message}>
                <Input type="date" invalid={!!errors.slip_date} {...register("slip_date", { required: "Required" })} />
              </Field>
              <Field label="M/s (Truck Owner)">
                <Controller
                  control={control}
                  name="truck_owner_name"
                  render={({ field }) => (
                    <AsyncCombobox
                      value={field.value}
                      onChange={field.onChange}
                      useSearch={useTruckOwnerSearch}
                      getLabel={(o) => o.name}
                      placeholder="optional"
                    />
                  )}
                />
              </Field>
              <Field label="Through / Broker">
                <Controller
                  control={control}
                  name="agent_name"
                  render={({ field }) => (
                    <AsyncCombobox
                      value={field.value}
                      onChange={field.onChange}
                      useSearch={useAgentSearch}
                      getLabel={(a) => a.name}
                      placeholder="optional"
                    />
                  )}
                />
              </Field>
            </Section>

            <Section title="Route & Goods">
              <Field label="Loading Point" error={errors.loading_point?.message}>
                <Input invalid={!!errors.loading_point} {...register("loading_point", { required: "Required" })} />
              </Field>
              <Field label="Destination" error={errors.destination?.message}>
                <Input invalid={!!errors.destination} {...register("destination", { required: "Required" })} />
              </Field>
              <Field label="Goods / Material" error={errors.goods_description?.message}>
                <Input invalid={!!errors.goods_description} {...register("goods_description", { required: "Required" })} />
              </Field>
              <Field label="Quantity / Weight" error={errors.quantity_weight?.message}>
                <Input invalid={!!errors.quantity_weight} {...register("quantity_weight", { required: "Required" })} />
              </Field>
              <Field label="Package Count (कट्टी)">
                <Input {...register("package_count")} placeholder="e.g. 500 bags" />
              </Field>
            </Section>

            <Section title="Advance">
              <Field label="Advance Rs">
                <Input type="number" step="0.01" min="0" {...register("advance_amount")} />
              </Field>
              <Field label="Advance Breakdown (notes)">
                <Input {...register("advance_note")} />
              </Field>
            </Section>
          </div>

          <div className="flex gap-2 border-t border-border px-5 py-4">
            <Button type="button" variant="secondary" className="flex-1" onClick={close}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" className="flex-[2]" disabled={isSubmitting}>
              {isSubmitting ? "Saving…" : "Save & Print Slip"}
            </Button>
          </div>
        </form>
      </SheetContent>
    </Sheet>
  );
}
