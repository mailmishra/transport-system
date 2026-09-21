import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import type { Receipt, ReceiptCreateInput } from "./types";

export interface ReceiptListParams {
  firmId?: string;
  bilti_id?: string;
  q?: string;
  sort?: string;
  page?: number;
  limit?: number;
}

function toQuery(p: ReceiptListParams) {
  return buildQuery({
    firm_id: p.firmId,
    bilti_id: p.bilti_id,
    q: p.q,
    sort: p.sort,
    page: p.page,
    limit: p.limit,
  });
}

export function useReceiptList(params: ReceiptListParams) {
  return useQuery({
    queryKey: ["receipts", "list", params],
    queryFn: () => api.get<Page<Receipt>>(`/receipts${toQuery(params)}`),
    placeholderData: (prev) => prev,
  });
}

export function useReceipt(id: string | undefined) {
  return useQuery({
    queryKey: ["receipts", id],
    queryFn: () => api.get<Receipt>(`/receipts/${id}`),
    enabled: !!id,
  });
}

export function useCreateReceipt() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ReceiptCreateInput) => api.post<Receipt>("/receipts", data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["receipts", "list"] }),
  });
}

export function useDeleteReceipt() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/receipts/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["receipts", "list"] }),
  });
}
