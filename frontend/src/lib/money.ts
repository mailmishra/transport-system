/** Port of concept/index.html's money() helper: format any numeric-ish
 * value (the backend returns Decimal fields as strings) as ₹X,XXX.XX.
 */
export function money(value: string | number | null | undefined): string {
  const n = Number(value ?? 0);
  return n.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function rupees(value: string | number | null | undefined): string {
  return `₹${money(value)}`;
}
