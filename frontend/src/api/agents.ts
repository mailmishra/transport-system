import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import { useLookupSearch } from "./lookups";
import type { Agent, AgentBalance, AgentUpdateInput } from "./types";

export function useAgentSearch(q: string) {
  return useLookupSearch<Agent>("agents", q);
}

export interface AgentListParams {
  q?: string;
  sort?: string;
  page?: number;
  limit?: number;
  activeOnly?: boolean;
}

export function useAgentList(params: AgentListParams) {
  return useQuery({
    queryKey: ["agents", "list", params],
    queryFn: () =>
      api.get<Page<Agent>>(
        `/agents${buildQuery({
          q: params.q,
          sort: params.sort,
          page: params.page,
          limit: params.limit,
          active_only: params.activeOnly,
        })}`,
      ),
    placeholderData: (prev) => prev,
  });
}

export function useAgent(id: string | undefined) {
  return useQuery({
    queryKey: ["agents", id],
    queryFn: () => api.get<Agent>(`/agents/${id}`),
    enabled: !!id,
  });
}

export function useAgentBalance(id: string | undefined, firmId: string | undefined) {
  return useQuery({
    queryKey: ["agents", id, "balance", firmId],
    queryFn: () => api.get<AgentBalance>(`/agents/${id}/balance${buildQuery({ firm_id: firmId })}`),
    enabled: !!id && !!firmId,
  });
}

export function useUpdateAgent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: AgentUpdateInput }) =>
      api.patch<Agent>(`/agents/${id}`, data),
    onSuccess: (_result, { id }) => {
      qc.invalidateQueries({ queryKey: ["agents"] });
      qc.invalidateQueries({ queryKey: ["agents", id] });
    },
  });
}
