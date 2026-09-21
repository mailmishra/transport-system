import * as React from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import type { ColumnDef, SortingState } from "@tanstack/react-table";
import { DataTable } from "@/components/data-table/data-table";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/ui/field-error";
import { useAgentList, useAgentBalance } from "@/api/agents";
import { useAgentPaymentList, useCreateAgentPayment } from "@/api/agentPayments";
import { useBiltiList } from "@/api/bilties";
import { useSelectedFirm } from "@/state/selected-firm";
import { ApiError } from "@/api/client";
import type { Agent, AgentPayment, Bilti } from "@/api/types";
import { rupees } from "@/lib/money";
import { formatDate, todayIso } from "@/lib/dates";
import { can } from "@/components/permissions/can";

/** Balances are computed server-side (GET /agents/{id}/balance), not
 * summed client-side from a fully-loaded bilti/payment list the way the
 * retired concept/index.html did -- same total_accrued/total_paid/balance
 * formula, now the single source of truth on both screens that need it.
 *
 * Lands on a browsable, searchable agent list (not a blank search box) so
 * it's obvious at a glance whether there's any data -- picking a row drills
 * into that agent's ledger detail below.
 */
export function AgentLedgerPage() {
  const { firmId } = useSelectedFirm();

  const [agent, setAgent] = React.useState<Agent | null>(null);

  if (!agent) {
    return <AgentPickerList onSelect={setAgent} />;
  }

  return <AgentLedgerDetail firmId={firmId} agent={agent} onBack={() => setAgent(null)} />;
}

function AgentPickerList({ onSelect }: { onSelect: (agent: Agent) => void }) {
  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState("");
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "name", desc: false }]);
  const { data, isLoading } = useAgentList({
    q: search || undefined,
    sort: sorting[0] ? `${sorting[0].desc ? "-" : ""}name` : "name",
    page,
    limit: 20,
  });

  const columns = React.useMemo<ColumnDef<Agent, any>[]>(
    () => [
      { id: "name", accessorKey: "name", header: "Name", enableSorting: true },
      { id: "phone", accessorKey: "phone", header: "Phone", enableSorting: false, cell: (ctx) => ctx.getValue<string | null>() ?? "—" },
      {
        id: "is_active",
        header: "Status",
        enableSorting: false,
        cell: ({ row }) => (
          <span className={row.original.is_active ? "text-status-paid" : "text-muted"}>
            {row.original.is_active ? "Active" : "Inactive"}
          </span>
        ),
      },
    ],
    [],
  );

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1 className="text-[19px] font-bold text-navy">Agent Ledger</h1>
        <p className="mt-0.5 text-xs text-muted">
          {data ? `${data.total} agents — pick one to see their ledger` : "Loading…"}
        </p>
      </div>
      <DataTable
        columns={columns}
        data={data?.items ?? []}
        total={data?.total ?? 0}
        page={data?.page ?? page}
        limit={data?.limit ?? 20}
        onPageChange={setPage}
        sorting={sorting}
        onSortingChange={(s) => {
          setSorting(s);
          setPage(1);
        }}
        search={search}
        onSearchChange={(q) => {
          setSearch(q);
          setPage(1);
        }}
        searchPlaceholder="Search agents by name…"
        isLoading={isLoading}
        onRowClick={onSelect}
      />
    </div>
  );
}

function AgentLedgerDetail({
  firmId,
  agent,
  onBack,
}: {
  firmId: string | undefined;
  agent: Agent;
  onBack: () => void;
}) {
  const { data: balance } = useAgentBalance(agent.id, firmId);

  const [biltiPage, setBiltiPage] = React.useState(1);
  const [biltiSorting, setBiltiSorting] = React.useState<SortingState>([{ id: "bilti_date", desc: true }]);
  const { data: biltiData, isLoading: biltiLoading } = useBiltiList({
    firmId,
    agentId: agent?.id,
    sort: biltiSorting[0] ? `${biltiSorting[0].desc ? "-" : ""}bilti_date` : undefined,
    page: biltiPage,
    limit: 10,
  });

  const [paymentPage, setPaymentPage] = React.useState(1);
  const { data: paymentData, isLoading: paymentLoading } = useAgentPaymentList({
    firmId,
    agentId: agent?.id,
    sort: "-payment_date",
    page: paymentPage,
    limit: 10,
  });

  const biltiColumns = React.useMemo<ColumnDef<Bilti, any>[]>(
    () => [
      { id: "bilti_date", accessorKey: "bilti_date", header: "Date", enableSorting: true, cell: (ctx) => formatDate(ctx.getValue<string>()) },
      { id: "bilti_no", accessorKey: "bilti_no", header: "Bilti", enableSorting: false },
      { id: "dalali", accessorKey: "dalali", header: "Dalali", enableSorting: false, cell: (ctx) => rupees(ctx.getValue<string>()) },
      { id: "freight_difference", accessorKey: "freight_difference", header: "FD", enableSorting: false, cell: (ctx) => rupees(ctx.getValue<string>()) },
      {
        id: "total",
        header: "Total",
        enableSorting: false,
        cell: ({ row }) =>
          rupees(Number(row.original.dalali) + Number(row.original.freight_difference)),
      },
    ],
    [],
  );

  const paymentColumns = React.useMemo<ColumnDef<AgentPayment, any>[]>(
    () => [
      { id: "payment_date", accessorKey: "payment_date", header: "Date", enableSorting: false, cell: (ctx) => formatDate(ctx.getValue<string>()) },
      { id: "amount", accessorKey: "amount", header: "Amount", enableSorting: false, cell: (ctx) => rupees(ctx.getValue<string>()) },
      { id: "mode", accessorKey: "mode", header: "Mode", enableSorting: false, cell: (ctx) => ctx.getValue<string | null>() ?? "—" },
      { id: "remarks", accessorKey: "remarks", header: "Remarks", enableSorting: false, cell: (ctx) => ctx.getValue<string | null>() ?? "—" },
    ],
    [],
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-start justify-between">
        <div>
          <button
            onClick={onBack}
            className="mb-1 flex items-center gap-1 text-xs font-semibold text-muted hover:text-navy"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> All Agents
          </button>
          <h1 className="text-[19px] font-bold text-navy">{agent.name}</h1>
        </div>
        <Button asChild variant="secondary">
          <Link to={`/agent-ledger/${agent.id}/print`}>Print Statement</Link>
        </Button>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <BalanceCard label="Total Accrued" value={balance?.total_accrued} />
        <BalanceCard label="Total Paid" value={balance?.total_paid} />
        <BalanceCard label="Balance" value={balance?.balance} emphasize />
      </div>

      <div>
        <h2 className="mb-2 text-sm font-bold text-navy">Bilti Ledger</h2>
        <DataTable
          columns={biltiColumns}
          data={biltiData?.items ?? []}
          total={biltiData?.total ?? 0}
          page={biltiData?.page ?? biltiPage}
          limit={biltiData?.limit ?? 10}
          onPageChange={setBiltiPage}
          sorting={biltiSorting}
          onSortingChange={setBiltiSorting}
          hideSearch
          isLoading={biltiLoading}
        />
      </div>

      {can("create", "agent-payment") && <RecordPaymentForm firmId={firmId} agentId={agent.id} />}

      <div>
        <h2 className="mb-2 text-sm font-bold text-navy">Recent Payments</h2>
        <DataTable
          columns={paymentColumns}
          data={paymentData?.items ?? []}
          total={paymentData?.total ?? 0}
          page={paymentData?.page ?? paymentPage}
          limit={paymentData?.limit ?? 10}
          onPageChange={setPaymentPage}
          sorting={[]}
          onSortingChange={() => {}}
          hideSearch
          isLoading={paymentLoading}
        />
      </div>
    </div>
  );
}

function BalanceCard({ label, value, emphasize }: { label: string; value?: string; emphasize?: boolean }) {
  return (
    <div className="rounded border-l-4 border-gold bg-white px-4 py-3">
      <div className="text-[10.5px] font-semibold uppercase tracking-wide text-muted">{label}</div>
      <div className={emphasize ? "mt-1 text-xl font-extrabold text-navy" : "mt-1 text-lg font-bold text-foreground"}>
        {value !== undefined ? rupees(value) : "—"}
      </div>
    </div>
  );
}

interface PaymentFormValues {
  amount: string;
  payment_date: string;
  mode: string;
  remarks: string;
}

function RecordPaymentForm({ firmId, agentId }: { firmId: string | undefined; agentId: string }) {
  const createPayment = useCreateAgentPayment();
  const {
    register,
    handleSubmit,
    reset,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<PaymentFormValues>({
    defaultValues: { amount: "", payment_date: todayIso(), mode: "", remarks: "" },
  });

  const onSubmit = handleSubmit(async (values) => {
    if (!firmId) return;
    try {
      await createPayment.mutateAsync({
        firm_id: firmId,
        agent_id: agentId,
        amount: Number(values.amount),
        payment_date: values.payment_date,
        mode: values.mode || null,
        remarks: values.remarks || null,
      });
      reset({ amount: "", payment_date: todayIso(), mode: "", remarks: "" });
    } catch (e) {
      if (e instanceof ApiError) setError("root", { message: e.message });
    }
  });

  return (
    <form onSubmit={onSubmit} className="rounded border border-border bg-white p-4">
      <h2 className="mb-3 text-sm font-bold text-navy">Record Agent Payment</h2>
      <FormError message={errors.root?.message} />
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div>
          <Label>Amount</Label>
          <Input
            type="number"
            step="0.01"
            className="mt-1"
            invalid={!!errors.amount}
            {...register("amount", { required: "Required", min: { value: 0.01, message: "Must be > 0" } })}
          />
        </div>
        <div>
          <Label>Date</Label>
          <Input type="date" className="mt-1" {...register("payment_date", { required: "Required" })} />
        </div>
        <div>
          <Label>Mode</Label>
          <Input className="mt-1" placeholder="cash / bank / upi" {...register("mode")} />
        </div>
        <div>
          <Label>Remarks</Label>
          <Input className="mt-1" {...register("remarks")} />
        </div>
      </div>
      <Button type="submit" variant="primary" className="mt-3" disabled={isSubmitting}>
        {isSubmitting ? "Saving…" : "Record Payment"}
      </Button>
    </form>
  );
}
