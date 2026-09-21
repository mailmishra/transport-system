import * as React from "react";
import { Label } from "@/components/ui/label";
import { FieldError } from "@/components/ui/field-error";

/** Shared drawer-form layout helpers -- factored out of bilti-form-drawer's
 * originally-local Section/Field once Phase 2 needed the same layout in
 * five more forms. Bilti's own local copies are untouched (no behavior
 * change there); every new Phase 2 form imports these instead.
 */
export function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <div className="text-[11px] font-bold uppercase tracking-wide text-navy">{title}</div>
      {children}
    </div>
  );
}

export function Field({
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
