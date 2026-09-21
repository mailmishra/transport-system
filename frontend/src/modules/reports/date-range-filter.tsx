import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

interface DateRangeFilterProps {
  dateFrom: string;
  dateTo: string;
  onChange: (range: { dateFrom: string; dateTo: string }) => void;
}

/** Shared date-range control for report tabs that take date_from/date_to --
 * kept dumb (controlled by the parent tab's own state) so each tab decides
 * its own default window instead of this component guessing one.
 */
export function DateRangeFilter({ dateFrom, dateTo, onChange }: DateRangeFilterProps) {
  return (
    <div className="flex flex-wrap items-end gap-3 rounded border border-border bg-white p-3">
      <div>
        <Label>From</Label>
        <Input
          type="date"
          className="mt-1"
          value={dateFrom}
          onChange={(e) => onChange({ dateFrom: e.target.value, dateTo })}
        />
      </div>
      <div>
        <Label>To</Label>
        <Input
          type="date"
          className="mt-1"
          value={dateTo}
          onChange={(e) => onChange({ dateFrom, dateTo: e.target.value })}
        />
      </div>
      {(dateFrom || dateTo) && (
        <Button variant="ghost" size="sm" onClick={() => onChange({ dateFrom: "", dateTo: "" })}>
          Clear
        </Button>
      )}
    </div>
  );
}
