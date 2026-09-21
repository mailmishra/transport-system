import { useLookupSearch } from "./lookups";
import type { Vehicle } from "./types";

export function useVehicleSearch(q: string) {
  return useLookupSearch<Vehicle>("vehicles", q);
}
