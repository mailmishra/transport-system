import { Routes, Route } from "react-router-dom";
import { AppShell } from "@/components/shell/app-shell";
import { BiltiListPage } from "@/modules/bilti/bilti-list-page";
import { BiltiFormDrawer } from "@/modules/bilti/bilti-form-drawer";
import { BiltiPrintView } from "@/modules/bilti/bilti-print-view";
import { ComingSoon } from "@/modules/coming-soon";
import { DashboardPage } from "@/modules/dashboard-page";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<DashboardPage />} />

        <Route path="/bilti" element={<BiltiListPage />} />
        <Route path="/bilti/new" element={<BiltiFormDrawer />} />
        <Route path="/bilti/:id/edit" element={<BiltiFormDrawer />} />
        <Route path="/bilti/:id/print" element={<BiltiPrintView />} />

        {/* Phase 2: same pattern as Bilti/GR, not built yet */}
        <Route path="/loading-slips" element={<ComingSoon title="Loading Slips" />} />
        <Route path="/agent-ledger" element={<ComingSoon title="Agent Ledger" />} />
        <Route path="/truck-owner-ledger" element={<ComingSoon title="Truck Owner Ledger" />} />
        <Route path="/receipts" element={<ComingSoon title="Receipts" />} />
        <Route path="/reports" element={<ComingSoon title="Reports" />} />
      </Routes>
    </AppShell>
  );
}
