import * as React from "react";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import { Loader2, Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import type { UseQueryResult } from "@tanstack/react-query";
import type { Page } from "@/api/client";

interface AsyncComboboxProps<T> {
  value: string;
  onChange: (value: string) => void;
  useSearch: (q: string) => UseQueryResult<Page<T>>;
  getLabel: (item: T) => string;
  getSubtitle?: (item: T) => string | null;
  placeholder?: string;
  id?: string;
  invalid?: boolean;
  required?: boolean;
}

/** Async-searchable lookup: types into a real text input (so any value is
 * still acceptable -- the backend resolves it via get_or_create_by_name/no,
 * same as the old <datalist> free-text pattern), while a debounced query
 * against GET /{resource}?q= suggests existing rows underneath. Replaces
 * shipping the entire Agent/Truck Owner/Vehicle table to the browser on
 * every page load.
 */
export function AsyncCombobox<T>({
  value,
  onChange,
  useSearch,
  getLabel,
  getSubtitle,
  placeholder,
  id,
  invalid,
  required,
}: AsyncComboboxProps<T>) {
  const [open, setOpen] = React.useState(false);
  const [debounced, setDebounced] = React.useState(value);

  React.useEffect(() => {
    const t = setTimeout(() => setDebounced(value), 220);
    return () => clearTimeout(t);
  }, [value]);

  const { data, isFetching } = useSearch(debounced.trim());
  const items = data?.items ?? [];
  const exactMatch = items.some((it) => getLabel(it).toLowerCase() === value.trim().toLowerCase());

  return (
    <PopoverPrimitive.Root open={open && value.trim().length > 0} onOpenChange={setOpen}>
      <PopoverPrimitive.Anchor asChild>
        <div className="relative">
          <Input
            id={id}
            value={value}
            required={required}
            invalid={invalid}
            placeholder={placeholder}
            autoComplete="off"
            onChange={(e) => {
              onChange(e.target.value);
              setOpen(true);
            }}
            onFocus={() => value.trim() && setOpen(true)}
          />
          {isFetching && (
            <Loader2 className="absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 animate-spin text-muted" />
          )}
        </div>
      </PopoverPrimitive.Anchor>
      <PopoverPrimitive.Portal>
        <PopoverPrimitive.Content
          align="start"
          sideOffset={4}
          onOpenAutoFocus={(e) => e.preventDefault()}
          className={cn(
            "z-50 w-[--radix-popover-trigger-width] overflow-hidden rounded border border-border bg-white shadow-lg",
          )}
        >
          {items.length === 0 && !isFetching && (
            <div className="px-3 py-2 text-xs text-muted">No matches yet</div>
          )}
          {items.map((it, i) => {
            const label = getLabel(it);
            const subtitle = getSubtitle?.(it);
            return (
              <button
                type="button"
                key={i}
                onClick={() => {
                  onChange(label);
                  setOpen(false);
                }}
                className="flex w-full flex-col items-start px-3 py-2 text-left text-sm hover:bg-background"
              >
                <span className="font-medium text-foreground">{label}</span>
                {subtitle && <span className="text-xs text-muted">{subtitle}</span>}
              </button>
            );
          })}
          {value.trim() && !exactMatch && (
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="flex w-full items-center gap-1.5 border-t border-border px-3 py-2 text-left text-xs font-semibold text-navy hover:bg-background"
            >
              <Plus className="h-3 w-3" /> Use "{value.trim()}" as new
            </button>
          )}
        </PopoverPrimitive.Content>
      </PopoverPrimitive.Portal>
    </PopoverPrimitive.Root>
  );
}
