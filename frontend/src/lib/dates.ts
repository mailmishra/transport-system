/** Backend dates are plain ISO "YYYY-MM-DD" strings (no time component) --
 * format for display without going through Date/timezone conversion, which
 * would risk shifting the date by a day near midnight in IST.
 */
export function formatDate(iso: string): string {
  const [y, m, d] = iso.split("-");
  const months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
  ];
  return `${d} ${months[Number(m) - 1]} ${y}`;
}

export function todayIso(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
