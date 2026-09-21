import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, buildQuery, type Page } from "./client";
import { useLookupSearch } from "./lookups";
import type { Vehicle, VehicleUpdateInput } from "./types";

export function useVehicleSearch(q: string) {
  return useLookupSearch<Vehicle>("vehicles", q);
}

export interface VehicleListParams {
  q?: string;
  sort?: string;
  page?: number;
  limit?: number;
  activeOnly?: boolean;
}

export function useVehicleList(params: VehicleListParams) {
  return useQuery({
    queryKey: ["vehicles", "list", params],
    queryFn: () =>
      api.get<Page<Vehicle>>(
        `/vehicles${buildQuery({
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

export function useUpdateVehicle() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: VehicleUpdateInput }) =>
      api.patch<Vehicle>(`/vehicles/${id}`, data),
    onSuccess: (_result, { id }) => {
      qc.invalidateQueries({ queryKey: ["vehicles"] });
      qc.invalidateQueries({ queryKey: ["vehicles", id] });
    },
  });
}
