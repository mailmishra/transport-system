/** Phase 2 placeholder: same DataTable + drawer + print pattern as
 * Bilti/GR, built module-by-module after Phase 1 is confirmed working
 * (see the approved plan). Not a real screen yet.
 */
export function ComingSoon({ title }: { title: string }) {
  return (
    <div className="rounded border border-dashed border-border bg-white p-8 text-center">
      <h2 className="text-lg font-bold text-navy">{title}</h2>
      <p className="mt-1 text-sm text-muted">
        Coming in Phase 2 — same list/create/print pattern as Bilti / GR.
      </p>
    </div>
  );
}
