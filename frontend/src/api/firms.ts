import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, ApiError } from "./client";
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

/** Multipart upload -- the shared `api` client only speaks JSON, so this
 * talks to fetch directly rather than stretching client.ts's request() to
 * cover a body type every other endpoint doesn't use.
 */
export function useUploadFirmLogo() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, file }: { id: string; file: File }) => {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`/api/firms/${id}/logo`, { method: "POST", body: form });
      let data: unknown = null;
      try {
        data = await res.json();
      } catch {
        // no body
      }
      if (!res.ok) {
        const detail = (data as { detail?: unknown } | null)?.detail;
        const message = typeof detail === "string" ? detail : res.statusText;
        throw new ApiError(message || "Upload failed", res.status, null);
      }
      return data as Firm;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["firms"] }),
  });
}
