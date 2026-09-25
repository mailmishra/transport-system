import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import type { Bilti, BiltiCreateInput, BiltiPrint, BiltiUpdateInput } from "./types";

export interface BiltiListParams {
  firmId?: string;
  q?: string;
  sort?: string;
  page?: number;
  limit?: number;
  agentId?: string;
  truckOwnerId?: string;
  vehicleNo?: string;
  fromLocation?: string;
  toLocation?: string;
  agentName?: string;
  factoryName?: string;
  dateFrom?: string;
  dateTo?: string;
}

function toQuery(p: BiltiListParams) {
  return buildQuery({
    firm_id: p.firmId,
    q: p.q,
    sort: p.sort,
    page: p.page,
    limit: p.limit,
    agent_id: p.agentId,
    truck_owner_id: p.truckOwnerId,
    vehicle_no: p.vehicleNo,
    from_location: p.fromLocation,
    to_location: p.toLocation,
    agent_name: p.agentName,
    factory_name: p.factoryName,
    date_from: p.dateFrom,
    date_to: p.dateTo,
  });
}

export function useBiltiList(params: BiltiListParams) {
  return useQuery({
    queryKey: ["bilties", "list", params],
    queryFn: () => api.get<Page<Bilti>>(`/bilties${toQuery(params)}`),
    placeholderData: (prev) => prev,
  });
}

/** Debounced search over Bilti/GR no., consignor, consignee -- backs the
 * Receipt form's "which Bilti is this against" picker, same AsyncCombobox
 * pattern as the Vehicle/Agent/TruckOwner lookups (but against a real FK,
 * not a get-or-create text field).
 */
export function useBiltiSearch(q: string) {
  return useQuery({
    queryKey: ["bilties", "lookup", q],
    queryFn: () => api.get<Page<Bilti>>(`/bilties${buildQuery({ q, limit: 10 })}`),
    placeholderData: (prev) => prev,
  });
}

export function useBilti(id: string | undefined) {
  return useQuery({
    queryKey: ["bilties", id],
    queryFn: () => api.get<Bilti>(`/bilties/${id}`),
    enabled: !!id,
  });
}

export function useBiltiPrint(id: string | undefined) {
  return useQuery({
    queryKey: ["bilties", id, "print"],
    queryFn: () => api.get<BiltiPrint>(`/bilties/${id}/print`),
    enabled: !!id,
  });
}

export function useCreateBilti() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: BiltiCreateInput) => api.post<Bilti>("/bilties", data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["bilties", "list"] }),
  });
}

export function useUpdateBilti() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: BiltiUpdateInput }) =>
      api.patch<Bilti>(`/bilties/${id}`, data),
    onSuccess: (_result, { id }) => {
      qc.invalidateQueries({ queryKey: ["bilties", "list"] });
      qc.invalidateQueries({ queryKey: ["bilties", id] });
    },
  });
}

export function fetchNextBiltiNo(firmId: string): Promise<{ next_no: string }> {
  return api.get(`/bilties/next-no?firm_id=${firmId}`);
}

export function useDeleteBilti() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/bilties/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["bilties", "list"] }),
  });
}
