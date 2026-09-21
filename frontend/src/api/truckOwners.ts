import { useLookupSearch } from "./lookups";
import type { TruckOwner } from "./types";

export function useTruckOwnerSearch(q: string) {
  return useLookupSearch<TruckOwner>("truck-owners", q);
}
