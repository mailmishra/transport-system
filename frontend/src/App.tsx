import { Routes, Route } from "react-router-dom";
import { AppShell } from "@/components/shell/app-shell";
import { BiltiListPage } from "@/modules/bilti/bilti-list-page";
import { BiltiFormDrawer } from "@/modules/bilti/bilti-form-drawer";
import { BiltiPrintView } from "@/modules/bilti/bilti-print-view";
import { LoadingSlipListPage } from "@/modules/loading-slips/loading-slip-list-page";
import { LoadingSlipFormDrawer } from "@/modules/loading-slips/loading-slip-form-drawer";
import { LoadingSlipPrintView } from "@/modules/loading-slips/loading-slip-print-view";
import { AgentLedgerPage } from "@/modules/agent-ledger/agent-ledger-page";
import { TruckOwnerLedgerPage } from "@/modules/truck-owner-ledger/truck-owner-ledger-page";
import { ReceiptListPage } from "@/modules/receipts/receipt-list-page";
import { ReceiptFormDrawer } from "@/modules/receipts/receipt-form-drawer";
import { ReceiptPrintView } from "@/modules/receipts/receipt-print-view";
import { AdminPage } from "@/modules/admin/admin-page";
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

        <Route path="/loading-slips" element={<LoadingSlipListPage />} />
        <Route path="/loading-slips/new" element={<LoadingSlipFormDrawer />} />
        <Route path="/loading-slips/:id/edit" element={<LoadingSlipFormDrawer />} />
        <Route path="/loading-slips/:id/print" element={<LoadingSlipPrintView />} />

        <Route path="/agent-ledger" element={<AgentLedgerPage />} />
        <Route path="/truck-owner-ledger" element={<TruckOwnerLedgerPage />} />

        <Route path="/receipts" element={<ReceiptListPage />} />
        <Route path="/receipts/new" element={<ReceiptFormDrawer />} />
        <Route path="/receipts/:id/print" element={<ReceiptPrintView />} />

        <Route path="/admin" element={<AdminPage />} />

        {/* Reports stays out of scope (client-side aggregation over the
            same data these modules already expose) until requested. */}
        <Route path="/reports" element={<ComingSoon title="Reports" />} />
      </Routes>
    </AppShell>
  );
}
