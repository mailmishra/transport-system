import { useQuery } from "@tanstack/react-query";
import { api, buildQuery } from "./client";
import type {
  DayBookReport,
  GstReportRow,
  LoadingSlip,
  OutstandingSummary,
  ReceivableRow,
  VehicleActivityRow,
} from "./types";

export interface DateRangeParams {
  dateFrom?: string;
  dateTo?: string;
}

export function useDayBook(firmId: string | undefined, range: DateRangeParams) {
  return useQuery({
    queryKey: ["reports", "day-book", firmId, range],
    queryFn: () =>
      api.get<DayBookReport>(
        `/reports/day-book${buildQuery({ firm_id: firmId, date_from: range.dateFrom, date_to: range.dateTo })}`,
      ),
    enabled: !!firmId,
  });
}

export function useOutstandingSummary(firmId: string | undefined) {
  return useQuery({
    queryKey: ["reports", "outstanding-summary", firmId],
    queryFn: () => api.get<OutstandingSummary>(`/reports/outstanding-summary${buildQuery({ firm_id: firmId })}`),
    enabled: !!firmId,
  });
}

export function useGstReport(firmId: string | undefined, range: DateRangeParams) {
  return useQuery({
    queryKey: ["reports", "gst", firmId, range],
    queryFn: () =>
      api.get<GstReportRow[]>(
        `/reports/gst${buildQuery({ firm_id: firmId, date_from: range.dateFrom, date_to: range.dateTo })}`,
      ),
    enabled: !!firmId,
  });
}

export function useVehicleActivity(firmId: string | undefined, range: DateRangeParams) {
  return useQuery({
    queryKey: ["reports", "vehicle-activity", firmId, range],
    queryFn: () =>
      api.get<VehicleActivityRow[]>(
        `/reports/vehicle-activity${buildQuery({ firm_id: firmId, date_from: range.dateFrom, date_to: range.dateTo })}`,
      ),
    enabled: !!firmId,
  });
}

export function usePendingLoadingSlips(firmId: string | undefined) {
  return useQuery({
    queryKey: ["reports", "pending-loading-slips", firmId],
    queryFn: () =>
      api.get<LoadingSlip[]>(`/reports/pending-loading-slips${buildQuery({ firm_id: firmId })}`),
    enabled: !!firmId,
  });
}

export function useReceivables(firmId: string | undefined) {
  return useQuery({
    queryKey: ["reports", "receivables", firmId],
    queryFn: () => api.get<ReceivableRow[]>(`/reports/receivables${buildQuery({ firm_id: firmId })}`),
    enabled: !!firmId,
  });
}
