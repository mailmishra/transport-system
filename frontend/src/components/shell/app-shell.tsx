import * as React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  Building2,
  ChevronDown,
  ClipboardList,
  FileText,
  Home,
  LayoutDashboard,
  Plus,
  Receipt,
  Search,
  Settings,
  Truck,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useSelectedFirm } from "@/state/selected-firm";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

/** ONE responsive shell, not two separate desktop/mobile apps -- same
 * navy/gold identity, horizontal tabs + stat surface on desktop collapsing
 * to a bottom tab bar + FAB on phone. Matches the approved Style B
 * desktop/mobile mockups: https://claude.ai/artifact/HTUkVrMB3aozxAuaJY57oT
 */
const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: Home, mobile: true },
  { to: "/loading-slips", label: "Loading Slips", icon: ClipboardList, mobile: false },
  { to: "/bilti", label: "Bilti / GR", icon: FileText, mobile: true, short: "Bilti" },
  { to: "/agent-ledger", label: "Agent Ledger", icon: Users, mobile: true, short: "Ledger" },
  { to: "/truck-owner-ledger", label: "Truck Owner Ledger", icon: Truck, mobile: false },
  { to: "/receipts", label: "Receipts", icon: Receipt, mobile: true },
  { to: "/reports", label: "Reports", icon: LayoutDashboard, mobile: false },
  { to: "/admin", label: "Admin", icon: Settings, mobile: false },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { firms, firm, firmId, setFirmId } = useSelectedFirm();
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Brand bar -- plain divs, not <header>/<nav>, so index.css's
          @media print rule (which targets those tags + .no-print) needs
          this class explicitly or the whole chrome bleeds into every
          printed document. */}
      <div className="no-print flex h-[54px] flex-shrink-0 items-center gap-3 bg-navy px-4 sm:gap-5 sm:px-6">
        <div className="flex h-6 w-6 items-center justify-center rounded bg-gold text-[11px] font-bold text-navy sm:h-[26px] sm:w-[26px] sm:text-[13px]">
          SK
        </div>
        <div className="text-sm font-bold text-white sm:text-[14px] sm:tracking-wide">
          <span className="sm:hidden">Bilti / GR</span>
          <span className="hidden sm:inline">
            {(firm?.name ?? "Transport System").toUpperCase()}
          </span>
        </div>
        <div className="hidden text-[11.5px] text-[#7E93A8] sm:block">
          {firm?.address ?? ""}
        </div>
        <div className="flex-1" />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button
              className="flex items-center gap-1.5 rounded bg-[#1C3A57] px-2 py-1.5 text-xs font-medium text-[#C6D2DD] hover:bg-[#24466A] sm:gap-2 sm:px-3"
              disabled={firms.length === 0}
              aria-label={`Switch firm (current: ${firm?.name ?? "none selected"})`}
            >
              <Building2 className="h-3.5 w-3.5 sm:hidden" />
              <span className="hidden sm:inline">Firm: {firm?.name ?? "…"}</span>
              <ChevronDown className="h-3 w-3" />
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {firms.map((f) => (
              <DropdownMenuItem key={f.id} selected={f.id === firmId} onSelect={() => setFirmId(f.id)}>
                {f.name}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
        <div className="flex h-[26px] w-[26px] items-center justify-center rounded-full bg-gold text-[11.5px] font-bold text-navy">
          AM
        </div>
      </div>

      {/* Desktop tab nav */}
      <div className="no-print hidden h-11 flex-shrink-0 items-stretch gap-0.5 border-b-2 border-navy bg-white px-5 sm:flex">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "flex items-center px-4 text-[12.5px] font-semibold text-[#5C6B7A]",
                isActive && "-mb-0.5 border-b-[3px] border-gold text-navy",
              )
            }
          >
            {item.label}
          </NavLink>
        ))}
      </div>

      {/* Mobile search row */}
      <div className="no-print flex-shrink-0 px-4 pb-2 pt-3 sm:hidden">
        <div className="flex items-center gap-2 rounded-xl border border-border bg-white px-3 py-2.5">
          <Search className="h-3.5 w-3.5 text-muted" />
          <span className="text-xs text-muted">Search GR, party, vehicle…</span>
        </div>
      </div>

      <main className="flex-1 px-4 pb-24 pt-3 sm:px-6 sm:pb-6 sm:pt-5">{children}</main>

      {/* Mobile FAB */}
      <button
        onClick={() => navigate("/bilti/new")}
        className="no-print fixed bottom-24 right-4 flex h-[54px] w-[54px] items-center justify-center rounded-xl bg-gold shadow-lg shadow-gold/40 sm:hidden"
        aria-label="New Bilti"
      >
        <Plus className="h-5 w-5 text-navy" strokeWidth={2.8} />
      </button>

      {/* Mobile bottom tab bar */}
      <div className="no-print fixed inset-x-0 bottom-0 z-30 flex h-[78px] border-t border-border bg-white pt-2.5 sm:hidden">
        {NAV_ITEMS.filter((i) => i.mobile).map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className="flex flex-1 flex-col items-center gap-1"
          >
            {({ isActive }) => (
              <>
                <item.icon
                  className={cn("h-5 w-5", isActive ? "text-navy" : "text-[#9AA7B4]")}
                  strokeWidth={isActive ? 2.4 : 2}
                />
                <span
                  className={cn(
                    "text-[9.5px] font-semibold",
                    isActive ? "text-navy" : "text-[#9AA7B4]",
                  )}
                >
                  {item.short ?? item.label}
                </span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </div>
  );
}
