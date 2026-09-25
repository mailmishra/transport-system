import * as React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Controller, useForm } from "react-hook-form";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { FieldError, FormError } from "@/components/ui/field-error";
import { AsyncCombobox } from "@/components/combobox/async-combobox";
import { useVehicleSearch } from "@/api/vehicles";
import { useAgentSearch } from "@/api/agents";
import { useTruckOwnerSearch } from "@/api/truckOwners";
import { useBilti, useCreateBilti, useUpdateBilti, fetchNextBiltiNo } from "@/api/bilties";
import { useSelectedFirm } from "@/state/selected-firm";
import { ApiError } from "@/api/client";
import type { BiltiCreateInput, GstPaidBy } from "@/api/types";
import { todayIso } from "@/lib/dates";

interface FormValues {
  bilti_no: string;
  bilti_date: string;
  consignee: string;
  from_location: string;
  to_location: string;
  vehicle_no: string;
  palti_vehicle_no: string;
  truck_owner_name: string;
  agent_name: string;
  package_count: string;
  package_unit: string;
  weight: string;
  weight_per_bag: string;
  charged_weight: string;
  freight_rate: string;
  freight: string;
  other_charges: string;
  kanta_charges: string;
  bahi_charges: string;
  service_tax: string;
  hamali: string;
  p_freight: string;
  dalali: string;
  advance_to_owner: string;
  freight_difference: string;
  gst_paid_by: string;
  eway_bill_no: string;
  invoice_value: string;
  goods_value_declared: string;
  remark: string;
}

const EMPTY: FormValues = {
  bilti_no: "", bilti_date: todayIso(), consignee: "",
  from_location: "", to_location: "", vehicle_no: "", palti_vehicle_no: "",
  truck_owner_name: "", agent_name: "", package_count: "", package_unit: "",
  weight: "", charged_weight: "", weight_per_bag: "", freight_rate: "",
  freight: "", other_charges: "0", kanta_charges: "0", bahi_charges: "0",
  service_tax: "0", hamali: "0", p_freight: "0", dalali: "0",
  advance_to_owner: "0", freight_difference: "0", gst_paid_by: "",
  eway_bill_no: "", invoice_value: "", goods_value_declared: "", remark: "",
};

const FIELD_NAMES = Object.keys(EMPTY) as Array<keyof FormValues>;

export function BiltiFormDrawer() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = !!id;
  const { firmId } = useSelectedFirm();
  const { data: existing } = useBilti(id);
  const createBilti = useCreateBilti();
  const updateBilti = useUpdateBilti();

  // Multi-consignor: each entry is one name
  const [consignors, setConsignors] = React.useState<string[]>([""]);
  // Multi-goods: each entry is one goods line
  const [goodsLines, setGoodsLines] = React.useState<string[]>([""]);
  const [consignorError, setConsignorError] = React.useState<string>();
  const [goodsError, setGoodsError] = React.useState<string>();
  const [generatingNo, setGeneratingNo] = React.useState(false);

  const {
    register,
    handleSubmit,
    control,
    reset,
    setError,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ defaultValues: EMPTY });

  // Auto-calc weight when package_count × weight_per_bag are both entered
  const packageCount = watch("package_count");
  const weightPerBag = watch("weight_per_bag");
  React.useEffect(() => {
    const count = parseFloat(packageCount);
    const perBag = parseFloat(weightPerBag);
    if (!isNaN(count) && count > 0 && !isNaN(perBag) && perBag > 0) {
      setValue("weight", String(Math.round(count * perBag * 1000) / 1000));
    }
  }, [packageCount, weightPerBag, setValue]);

  // Auto-calc freight when rate × weight are both entered
  const freightRate = watch("freight_rate");
  const weight = watch("weight");
  React.useEffect(() => {
    const rate = parseFloat(freightRate);
    const w = parseFloat(weight);
    if (!isNaN(rate) && rate > 0 && !isNaN(w) && w > 0) {
      setValue("freight", String(Math.round(rate * w * 100) / 100));
    }
  }, [freightRate, weight, setValue]);

  React.useEffect(() => {
    if (existing) {
      setConsignors(existing.consignor.split("\n").filter(Boolean) || [""]);
      setGoodsLines(existing.goods_description.split("\n").filter(Boolean) || [""]);
      reset({
        bilti_no: existing.bilti_no,
        bilti_date: existing.bilti_date,
        consignee: existing.consignee,
        from_location: existing.from_location,
        to_location: existing.to_location,
        vehicle_no: existing.vehicle.vehicle_no,
        palti_vehicle_no: existing.palti_vehicle?.vehicle_no ?? "",
        truck_owner_name: existing.truck_owner.name,
        agent_name: existing.agent?.name ?? "",
        package_count: existing.package_count ?? "",
        package_unit: existing.package_unit ?? "",
        weight: existing.weight,
        weight_per_bag: existing.weight_per_bag ?? "",
        charged_weight: existing.charged_weight ?? "",
        freight_rate: existing.freight_rate ?? "",
        freight: existing.freight,
        other_charges: existing.other_charges,
        kanta_charges: existing.kanta_charges,
        bahi_charges: existing.bahi_charges,
        service_tax: existing.service_tax,
        hamali: existing.hamali,
        p_freight: existing.p_freight,
        dalali: existing.dalali,
        advance_to_owner: existing.advance_to_owner,
        freight_difference: existing.freight_difference,
        gst_paid_by: existing.gst_paid_by ?? "",
        eway_bill_no: existing.eway_bill_no ?? "",
        invoice_value: existing.invoice_value ?? "",
        goods_value_declared: existing.goods_value_declared ?? "",
        remark: existing.remark ?? "",
      });
    }
  }, [existing, reset]);

  const close = () => navigate(-1);

  const generateNo = async () => {
    if (!firmId) return;
    setGeneratingNo(true);
    try {
      const { next_no } = await fetchNextBiltiNo(firmId);
      setValue("bilti_no", next_no);
    } finally {
      setGeneratingNo(false);
    }
  };

  const onSubmit = handleSubmit(async (values) => {
    if (!firmId) return;

    // Validate dynamic arrays
    const filledConsignors = consignors.map((s) => s.trim()).filter(Boolean);
    const filledGoods = goodsLines.map((s) => s.trim()).filter(Boolean);
    if (filledConsignors.length === 0) {
      setConsignorError("At least one consignor is required");
      return;
    }
    if (filledGoods.length === 0) {
      setGoodsError("At least one goods description is required");
      return;
    }
    setConsignorError(undefined);
    setGoodsError(undefined);

    const num = (s: string) => (s.trim() === "" ? undefined : Number(s));
    const payload: BiltiCreateInput = {
      firm_id: firmId,
      bilti_no: values.bilti_no,
      bilti_date: values.bilti_date,
      consignor: filledConsignors.join("\n"),
      consignee: values.consignee,
      from_location: values.from_location,
      to_location: values.to_location,
      vehicle_no: values.vehicle_no,
      palti_vehicle_no: values.palti_vehicle_no || null,
      truck_owner_name: values.truck_owner_name,
      agent_name: values.agent_name,
      goods_description: filledGoods.join("\n"),
      package_count: values.package_count || null,
      package_unit: values.package_unit || null,
      weight: values.weight,
      weight_per_bag: num(values.weight_per_bag) ?? null,
      charged_weight: values.charged_weight || null,
      freight_rate: num(values.freight_rate) ?? null,
      freight: Number(values.freight),
      other_charges: num(values.other_charges) ?? 0,
      kanta_charges: num(values.kanta_charges) ?? 0,
      bahi_charges: num(values.bahi_charges) ?? 0,
      service_tax: num(values.service_tax) ?? 0,
      hamali: num(values.hamali) ?? 0,
      p_freight: num(values.p_freight) ?? 0,
      dalali: num(values.dalali) ?? 0,
      advance_to_owner: num(values.advance_to_owner) ?? 0,
      freight_difference: num(values.freight_difference) ?? 0,
      gst_paid_by: (values.gst_paid_by || null) as GstPaidBy | null,
      eway_bill_no: values.eway_bill_no || null,
      invoice_value: num(values.invoice_value) ?? null,
      goods_value_declared: num(values.goods_value_declared) ?? null,
      remark: values.remark || null,
    };

    try {
      if (isEdit && id) {
        await updateBilti.mutateAsync({ id, data: payload });
        navigate(`/bilti/${id}/print`);
      } else {
        const created = await createBilti.mutateAsync(payload);
        navigate(`/bilti/${created.id}/print`);
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
      <SheetContent title={isEdit ? "Edit Bilti / GR" : "New Bilti / GR"}>
        <form onSubmit={onSubmit} className="flex flex-1 flex-col overflow-hidden">
          <div className="flex-1 space-y-4 overflow-y-auto px-5 py-4">
            <FormError message={errors.root?.message} />

            <Section title="Route & Party">
              <Field label="Bilti / GR No." error={errors.bilti_no?.message}>
                <div className="flex gap-2">
                  <Input invalid={!!errors.bilti_no} {...register("bilti_no", { required: "Required" })} className="flex-1" />
                  <Button type="button" variant="secondary" className="shrink-0 px-3 text-xs" onClick={generateNo} disabled={generatingNo}>
                    {generatingNo ? "…" : "Generate"}
                  </Button>
                </div>
              </Field>
              <Field label="Date" error={errors.bilti_date?.message}>
                <Input type="date" invalid={!!errors.bilti_date} {...register("bilti_date", { required: "Required" })} />
              </Field>

              <div>
                <Label>Consignor(s)</Label>
                <div className="mt-1 space-y-1.5">
                  {consignors.map((val, i) => (
                    <div key={i} className="flex gap-1.5">
                      <Input
                        value={val}
                        onChange={(e) => {
                          const next = [...consignors];
                          next[i] = e.target.value;
                          setConsignors(next);
                        }}
                        placeholder={`Consignor ${i + 1}`}
                        className="flex-1"
                      />
                      {consignors.length > 1 && (
                        <button
                          type="button"
                          className="px-2 text-sm text-muted hover:text-destructive"
                          onClick={() => setConsignors(consignors.filter((_, j) => j !== i))}
                        >
                          ✕
                        </button>
                      )}
                    </div>
                  ))}
                  <button
                    type="button"
                    className="text-xs text-navy underline"
                    onClick={() => setConsignors([...consignors, ""])}
                  >
                    + Add Consignor
                  </button>
                </div>
                {consignorError && <p className="mt-1 text-xs text-destructive">{consignorError}</p>}
              </div>

              <Field label="Consignee" error={errors.consignee?.message}>
                <Input invalid={!!errors.consignee} {...register("consignee", { required: "Required" })} />
              </Field>
              <Field label="From" error={errors.from_location?.message}>
                <Input invalid={!!errors.from_location} {...register("from_location", { required: "Required" })} />
              </Field>
              <Field label="To" error={errors.to_location?.message}>
                <Input invalid={!!errors.to_location} {...register("to_location", { required: "Required" })} />
              </Field>
              <Field label="Vehicle No." error={errors.vehicle_no?.message}>
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
              <Field label="Palti (Alt.) Vehicle No.">
                <Controller
                  control={control}
                  name="palti_vehicle_no"
                  render={({ field }) => (
                    <AsyncCombobox
                      value={field.value}
                      onChange={field.onChange}
                      useSearch={useVehicleSearch}
                      getLabel={(v) => v.vehicle_no}
                      placeholder="optional"
                    />
                  )}
                />
              </Field>
              <Field label="Truck Owner" error={errors.truck_owner_name?.message}>
                <Controller
                  control={control}
                  name="truck_owner_name"
                  rules={{ required: "Required" }}
                  render={({ field }) => (
                    <AsyncCombobox
                      value={field.value}
                      onChange={field.onChange}
                      useSearch={useTruckOwnerSearch}
                      getLabel={(o) => o.name}
                      invalid={!!errors.truck_owner_name}
                    />
                  )}
                />
              </Field>
              <Field label="Agent / Dalal (Broker)" error={errors.agent_name?.message}>
                <Controller
                  control={control}
                  name="agent_name"
                  rules={{ required: "Required" }}
                  render={({ field }) => (
                    <AsyncCombobox
                      value={field.value}
                      onChange={field.onChange}
                      useSearch={useAgentSearch}
                      getLabel={(a) => a.name}
                      invalid={!!errors.agent_name}
                    />
                  )}
                />
              </Field>
            </Section>

            <Section title="Goods & Weight">
              <div>
                <Label>Goods / Description</Label>
                <div className="mt-1 space-y-1.5">
                  {goodsLines.map((val, i) => (
                    <div key={i} className="flex gap-1.5">
                      <Input
                        value={val}
                        onChange={(e) => {
                          const next = [...goodsLines];
                          next[i] = e.target.value;
                          setGoodsLines(next);
                        }}
                        placeholder={`Item ${i + 1}`}
                        className="flex-1"
                      />
                      {goodsLines.length > 1 && (
                        <button
                          type="button"
                          className="px-2 text-sm text-muted hover:text-destructive"
                          onClick={() => setGoodsLines(goodsLines.filter((_, j) => j !== i))}
                        >
                          ✕
                        </button>
                      )}
                    </div>
                  ))}
                  <button
                    type="button"
                    className="text-xs text-navy underline"
                    onClick={() => setGoodsLines([...goodsLines, ""])}
                  >
                    + Add Item
                  </button>
                </div>
                {goodsError && <p className="mt-1 text-xs text-destructive">{goodsError}</p>}
              </div>
              <div className="grid grid-cols-2 gap-2">
                <Field label="Package Count"><Input {...register("package_count")} placeholder="67" /></Field>
                <Field label="Package Unit"><Input {...register("package_unit")} placeholder="BAG" /></Field>
              </div>
              <Field label="Weight per Bag / Unit (MT)">
                <Input type="number" step="0.001" {...register("weight_per_bag")} placeholder="e.g. 0.05 for 50 kg" />
              </Field>
              <Field label="Weight (Actual)" error={errors.weight?.message}>
                <Input invalid={!!errors.weight} {...register("weight", { required: "Required" })} />
              </Field>
              <Field label="Weight (Charged)"><Input {...register("charged_weight")} /></Field>
            </Section>

            <Section title="Charges">
              <div className="grid grid-cols-2 gap-2">
                <Field label="Freight Rate"><Input type="number" step="0.01" {...register("freight_rate")} /></Field>
                <Field label="Freight" error={errors.freight?.message}>
                  <Input type="number" step="0.01" invalid={!!errors.freight} {...register("freight", { required: "Required", min: { value: 0.01, message: "Must be > 0" } })} />
                </Field>
                <Field label="Other Charges"><Input type="number" step="0.01" {...register("other_charges")} /></Field>
                <Field label="Kanta Charges"><Input type="number" step="0.01" {...register("kanta_charges")} /></Field>
                <Field label="Bahi Charges"><Input type="number" step="0.01" {...register("bahi_charges")} /></Field>
                <Field label="Service Tax"><Input type="number" step="0.01" {...register("service_tax")} /></Field>
                <Field label="Hamali"><Input type="number" step="0.01" {...register("hamali")} /></Field>
                <Field label="P.Freight"><Input type="number" step="0.01" {...register("p_freight")} /></Field>
                <Field label="Dalali"><Input type="number" step="0.01" {...register("dalali")} /></Field>
                <Field label="Advance to Owner"><Input type="number" step="0.01" {...register("advance_to_owner")} /></Field>
              </div>
              <Field label="FD — Freight Difference (hidden from printed Bilti)">
                <Input type="number" step="0.01" {...register("freight_difference")} />
              </Field>
            </Section>

            <Section title="Compliance">
              <Field label="GST Paid By">
                <select
                  className="h-9 w-full rounded border border-border bg-white px-3 text-sm"
                  {...register("gst_paid_by")}
                >
                  <option value="">(unspecified)</option>
                  <option value="consignor">Consignor</option>
                  <option value="consignee">Consignee</option>
                  <option value="transporter">Transporter</option>
                  <option value="exempted">Exempted</option>
                </select>
              </Field>
              <Field label="E-Way Bill No."><Input {...register("eway_bill_no")} /></Field>
              <Field label="Invoice Value"><Input type="number" step="0.01" {...register("invoice_value")} /></Field>
              <Field label="Goods Value Declared"><Input type="number" step="0.01" {...register("goods_value_declared")} /></Field>
              <Field label="Remark"><Input {...register("remark")} /></Field>
            </Section>
          </div>

          <div className="flex gap-2 border-t border-border px-5 py-4">
            <Button type="button" variant="secondary" className="flex-1" onClick={close}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" className="flex-[2]" disabled={isSubmitting}>
              {isSubmitting ? "Saving…" : "Save & Print GR"}
            </Button>
          </div>
        </form>
      </SheetContent>
    </Sheet>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <div className="text-[11px] font-bold uppercase tracking-wide text-navy">{title}</div>
      {children}
    </div>
  );
}

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <Label>{label}</Label>
      <div className="mt-1">{children}</div>
      <FieldError message={error} />
    </div>
  );
}
