import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import type { LoadingSlip, LoadingSlipCreateInput, LoadingSlipUpdateInput } from "./types";

export interface LoadingSlipListParams {
  firmId?: string;
  q?: string;
  sort?: string;
  page?: number;
  limit?: number;
}

function toQuery(p: LoadingSlipListParams) {
  return buildQuery({ firm_id: p.firmId, q: p.q, sort: p.sort, page: p.page, limit: p.limit });
}

export function useLoadingSlipList(params: LoadingSlipListParams) {
  return useQuery({
    queryKey: ["loading-slips", "list", params],
    queryFn: () => api.get<Page<LoadingSlip>>(`/loading-slips${toQuery(params)}`),
    placeholderData: (prev) => prev,
  });
}

export function useLoadingSlip(id: string | undefined) {
  return useQuery({
    queryKey: ["loading-slips", id],
    queryFn: () => api.get<LoadingSlip>(`/loading-slips/${id}`),
    enabled: !!id,
  });
}

export function useCreateLoadingSlip() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: LoadingSlipCreateInput) => api.post<LoadingSlip>("/loading-slips", data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["loading-slips", "list"] }),
  });
}

export function useUpdateLoadingSlip() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: LoadingSlipUpdateInput }) =>
      api.patch<LoadingSlip>(`/loading-slips/${id}`, data),
    onSuccess: (_result, { id }) => {
      qc.invalidateQueries({ queryKey: ["loading-slips", "list"] });
      qc.invalidateQueries({ queryKey: ["loading-slips", id] });
    },
  });
}

export function useDeleteLoadingSlip() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/loading-slips/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["loading-slips", "list"] }),
  });
}
