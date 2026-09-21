/** Per-field validation message, shown directly under the offending input --
 * ports the just-shipped concept/index.html fix (inline errors, not a
 * joined multi-field string at the bottom of the form) to a real component.
 */
export function FieldError({ message }: { message?: string }) {
  if (!message) return null;
  return <p className="mt-1 text-xs font-normal text-status-overdue">{message}</p>;
}

/** A single, concise banner for errors that aren't about one specific
 * field (e.g. "bilti_no already used for this firm"). Never a joined list.
 */
export function FormError({ message }: { message?: string | null }) {
  if (!message) return null;
  return (
    <div className="rounded border border-status-overdue/30 bg-red-50 px-3 py-2 text-sm text-status-overdue">
      {message}
    </div>
  );
}
