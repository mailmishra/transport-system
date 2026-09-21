import * as React from "react";
import { useFirms } from "@/api/firms";
import type { Firm } from "@/api/types";

const STORAGE_KEY = "transport-system:selected-firm-id";

interface SelectedFirmContextValue {
  firms: Firm[];
  firm: Firm | undefined;
  firmId: string | undefined;
  setFirmId: (id: string) => void;
  isLoading: boolean;
}

const SelectedFirmContext = React.createContext<SelectedFirmContextValue | null>(null);

/** The one place "which firm is active" lives. Every list/form/report/ledger
 * screen that used to hardcode `firms?.[0]` reads it from here instead, so
 * picking a firm in the AppShell dropdown actually changes what the rest of
 * the app shows. Printed documents (bilti/loading-slip/receipt print views)
 * deliberately do NOT use this -- a document belongs to the firm it was
 * raised under, not whichever firm happens to be selected right now.
 */
export function SelectedFirmProvider({ children }: { children: React.ReactNode }) {
  const { data: firms, isLoading } = useFirms();
  const [storedId, setStoredId] = React.useState<string | null>(() => {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch {
      return null;
    }
  });

  // Falls back to the first firm when nothing's stored yet, or the stored
  // id no longer matches any firm (e.g. switched database/seed data).
  const firm = React.useMemo(() => {
    if (!firms || firms.length === 0) return undefined;
    return firms.find((f) => f.id === storedId) ?? firms[0];
  }, [firms, storedId]);

  const setFirmId = React.useCallback((id: string) => {
    setStoredId(id);
    try {
      localStorage.setItem(STORAGE_KEY, id);
    } catch {
      // private browsing / storage disabled -- selection just won't persist
    }
  }, []);

  const value = React.useMemo<SelectedFirmContextValue>(
    () => ({ firms: firms ?? [], firm, firmId: firm?.id, setFirmId, isLoading }),
    [firms, firm, setFirmId, isLoading],
  );

  return <SelectedFirmContext.Provider value={value}>{children}</SelectedFirmContext.Provider>;
}

export function useSelectedFirm(): SelectedFirmContextValue {
  const ctx = React.useContext(SelectedFirmContext);
  if (!ctx) throw new Error("useSelectedFirm must be used within SelectedFirmProvider");
  return ctx;
}
