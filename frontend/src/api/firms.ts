import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "./client";
import type { Firm } from "./types";

export function useFirms() {
  return useQuery({ queryKey: ["firms"], queryFn: () => api.get<Firm[]>("/firms") });
}

export function useUpdateFirm() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Firm> }) =>
      api.patch<Firm>(`/firms/${id}`, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["firms"] }),
  });
}
