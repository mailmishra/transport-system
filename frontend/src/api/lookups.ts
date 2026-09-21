import { useQuery } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";

/** Shared shape for the async-searchable lookups (Agent/Truck Owner/
 * Vehicle) that back the Combobox component -- replaces the old
 * concept/index.html pattern of loading every row into a <datalist> on
 * page load, which doesn't scale past a few dozen rows.
 */
export function useLookupSearch<T>(resource: string, q: string, opts?: { limit?: number }) {
  const limit = opts?.limit ?? 10;
  return useQuery({
    queryKey: [resource, "lookup", q, limit],
    queryFn: () =>
      api.get<Page<T>>(`/${resource}${buildQuery({ q, limit, active_only: true })}`),
    // Debounce is handled by the caller (Combobox) delaying when this
    // query key changes; keep previous results visible while typing.
    placeholderData: (prev) => prev,
    enabled: true,
  });
}
