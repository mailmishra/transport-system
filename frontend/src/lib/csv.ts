/** Client-side CSV export for report tables. The data driving every report
 * tab is already fetched and in memory for on-screen rendering, so this
 * builds the file from that same array rather than adding a parallel
 * ?format=csv backend endpoint per report.
 */
function csvCell(value: unknown): string {
  const s = value === null || value === undefined ? "" : String(value);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export function downloadCsv<T>(
  filename: string,
  columns: { key: keyof T; header: string }[],
  rows: T[],
): void {
  const lines = [
    columns.map((c) => csvCell(c.header)).join(","),
    ...rows.map((row) => columns.map((c) => csvCell(row[c.key])).join(",")),
  ];
  // Leading BOM so Excel (still common for this data's audience) opens the
  // file as UTF-8 instead of guessing a local codepage and mangling ₹/names.
  const blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename.endsWith(".csv") ? filename : `${filename}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}
