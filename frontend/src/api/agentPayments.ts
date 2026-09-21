import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import type { AgentPayment, AgentPaymentCreateInput } from "./types";

export interface AgentPaymentListParams {
  firmId?: string;
  agentId?: string;
  sort?: string;
  page?: number;
  limit?: number;
}

function toQuery(p: AgentPaymentListParams) {
  return buildQuery({ firm_id: p.firmId, agent_id: p.agentId, sort: p.sort, page: p.page, limit: p.limit });
}

export function useAgentPaymentList(params: AgentPaymentListParams) {
  return useQuery({
    queryKey: ["agent-payments", "list", params],
    queryFn: () => api.get<Page<AgentPayment>>(`/agent-payments${toQuery(params)}`),
    placeholderData: (prev) => prev,
    enabled: !!params.agentId,
  });
}

export function useCreateAgentPayment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentPaymentCreateInput) => api.post<AgentPayment>("/agent-payments", data),
    onSuccess: (_result, vars) => {
      qc.invalidateQueries({ queryKey: ["agent-payments", "list"] });
      qc.invalidateQueries({ queryKey: ["agents", vars.agent_id, "balance"] });
    },
  });
}

export function useDeleteAgentPayment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/agent-payments/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-payments", "list"] });
      qc.invalidateQueries({ queryKey: ["agents"] });
    },
  });
}
