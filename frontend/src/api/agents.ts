import { useLookupSearch } from "./lookups";
import type { Agent } from "./types";

export function useAgentSearch(q: string) {
  return useLookupSearch<Agent>("agents", q);
}
