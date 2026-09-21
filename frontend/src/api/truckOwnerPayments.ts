import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import type { TruckOwnerPayment, TruckOwnerPaymentCreateInput } from "./types";

export interface TruckOwnerPaymentListParams {
  firmId?: string;
  truckOwnerId?: string;
  sort?: string;
  page?: number;
  limit?: number;
}

function toQuery(p: TruckOwnerPaymentListParams) {
  return buildQuery({
    firm_id: p.firmId,
    truck_owner_id: p.truckOwnerId,
    sort: p.sort,
    page: p.page,
    limit: p.limit,
  });
}

export function useTruckOwnerPaymentList(params: TruckOwnerPaymentListParams) {
  return useQuery({
    queryKey: ["truck-owner-payments", "list", params],
    queryFn: () => api.get<Page<TruckOwnerPayment>>(`/truck-owner-payments${toQuery(params)}`),
    placeholderData: (prev) => prev,
    enabled: !!params.truckOwnerId,
  });
}

export function useCreateTruckOwnerPayment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: TruckOwnerPaymentCreateInput) =>
      api.post<TruckOwnerPayment>("/truck-owner-payments", data),
    onSuccess: (_result, vars) => {
      qc.invalidateQueries({ queryKey: ["truck-owner-payments", "list"] });
      qc.invalidateQueries({ queryKey: ["truck-owners", vars.truck_owner_id, "balance"] });
    },
  });
}

export function useDeleteTruckOwnerPayment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/truck-owner-payments/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["truck-owner-payments", "list"] });
      qc.invalidateQueries({ queryKey: ["truck-owners"] });
    },
  });
}
