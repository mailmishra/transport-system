import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import { useLookupSearch } from "./lookups";
import type { TruckOwner, TruckOwnerBalance, TruckOwnerUpdateInput } from "./types";

export function useTruckOwnerSearch(q: string) {
  return useLookupSearch<TruckOwner>("truck-owners", q);
}

export interface TruckOwnerListParams {
  q?: string;
  sort?: string;
  page?: number;
  limit?: number;
  activeOnly?: boolean;
}

export function useTruckOwnerList(params: TruckOwnerListParams) {
  return useQuery({
    queryKey: ["truck-owners", "list", params],
    queryFn: () =>
      api.get<Page<TruckOwner>>(
        `/truck-owners${buildQuery({
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

export function useTruckOwner(id: string | undefined) {
  return useQuery({
    queryKey: ["truck-owners", id],
    queryFn: () => api.get<TruckOwner>(`/truck-owners/${id}`),
    enabled: !!id,
  });
}

export function useTruckOwnerBalance(id: string | undefined, firmId: string | undefined) {
  return useQuery({
    queryKey: ["truck-owners", id, "balance", firmId],
    queryFn: () =>
      api.get<TruckOwnerBalance>(`/truck-owners/${id}/balance${buildQuery({ firm_id: firmId })}`),
    enabled: !!id && !!firmId,
  });
}

export function useUpdateTruckOwner() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: TruckOwnerUpdateInput }) =>
      api.patch<TruckOwner>(`/truck-owners/${id}`, data),
    onSuccess: (_result, { id }) => {
      qc.invalidateQueries({ queryKey: ["truck-owners"] });
      qc.invalidateQueries({ queryKey: ["truck-owners", id] });
    },
  });
}
