import { Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { downloadCsv } from "@/lib/csv";

interface ExportCsvButtonProps<T> {
  filename: string;
  columns: { key: keyof T; header: string }[];
  rows: T[] | undefined;
}

export function ExportCsvButton<T>({
  filename,
  columns,
  rows,
}: ExportCsvButtonProps<T>) {
  return (
    <Button
      variant="secondary"
      size="sm"
      disabled={!rows || rows.length === 0}
      onClick={() => rows && downloadCsv(filename, columns, rows)}
    >
      <Download className="h-3.5 w-3.5" /> Export CSV
    </Button>
  );
}
