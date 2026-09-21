/** TypeScript mirrors of the Pydantic schemas in backend/app/schemas/.
 * Decimal fields come over the wire as strings (FastAPI's default JSON
 * encoding for Decimal) -- typed as `string` here, not `number`, and
 * formatted for display via lib/money.ts rather than passed to arithmetic
 * directly (same reasoning as the backend never trusting float for money).
 */

export interface Firm {
  id: string;
  name: string;
  address: string | null;
  phone: string | null;
  email: string | null;
  pan_no: string | null;
  bank_account_no: string | null;
  bank_name: string | null;
  bank_branch: string | null;
  bank_ifsc: string | null;
  logo_url: string | null;
  gstin: string | null;
  signatory_name: string | null;
  signatory_designation: string | null;
  jurisdiction_text: string | null;
}

export interface Vehicle {
  id: string;
  vehicle_no: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Agent {
  id: string;
  name: string;
  phone: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TruckOwner {
  id: string;
  name: string;
  phone: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoadingSlip {
  id: string;
  firm_id: string;
  slip_date: string;
  vehicle: Vehicle;
  truck_owner: TruckOwner | null;
  agent: Agent | null;
  loading_point: string;
  destination: string;
  goods_description: string;
  quantity_weight: string;
  package_count: string | null;
  advance_amount: string;
  advance_note: string | null;
  created_at: string;
  updated_at: string;
}

export interface LoadingSlipCreateInput {
  firm_id: string;
  slip_date: string;
  vehicle_no: string;
  truck_owner_name?: string | null;
  agent_name?: string | null;
  loading_point: string;
  destination: string;
  goods_description: string;
  quantity_weight: string;
  package_count?: string | null;
  advance_amount?: number;
  advance_note?: string | null;
}

export type LoadingSlipUpdateInput = Partial<LoadingSlipCreateInput>;

export interface AgentPayment {
  id: string;
  firm_id: string;
  agent: Agent;
  amount: string;
  payment_date: string;
  mode: string | null;
  remarks: string | null;
  created_at: string;
  updated_at: string;
}

export interface AgentPaymentCreateInput {
  firm_id: string;
  agent_id: string;
  amount: number;
  payment_date: string;
  mode?: string | null;
  remarks?: string | null;
}

export interface AgentBalance {
  agent: Agent;
  firm_id: string;
  total_accrued: string;
  total_paid: string;
  balance: string;
}

export interface TruckOwnerPayment {
  id: string;
  firm_id: string;
  truck_owner: TruckOwner;
  amount: string;
  payment_date: string;
  mode: string | null;
  remarks: string | null;
  bilti_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface TruckOwnerPaymentCreateInput {
  firm_id: string;
  truck_owner_id: string;
  amount: number;
  payment_date: string;
  mode?: string | null;
  remarks?: string | null;
  bilti_id?: string | null;
}

export interface TruckOwnerBalance {
  truck_owner: TruckOwner;
  firm_id: string;
  total_freight: string;
  total_advance: string;
  total_paid: string;
  balance: string;
}

export interface LedgerStatementLine {
  date: string;
  particulars: string;
  reference: string | null;
  debit: string;
  credit: string;
  balance: string;
}

export interface AgentStatement {
  agent: Agent;
  firm_id: string;
  lines: LedgerStatementLine[];
  total_accrued: string;
  total_paid: string;
  closing_balance: string;
}

export interface TruckOwnerStatement {
  truck_owner: TruckOwner;
  firm_id: string;
  lines: LedgerStatementLine[];
  total_freight: string;
  total_advance: string;
  total_paid: string;
  closing_balance: string;
}

export interface Receipt {
  id: string;
  firm_id: string;
  bilti_id: string;
  amount: string;
  receipt_date: string;
  received_from: string;
  remarks: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReceiptCreateInput {
  firm_id: string;
  bilti_id: string;
  amount: number;
  receipt_date: string;
  received_from: string;
  remarks?: string | null;
}

export interface AgentUpdateInput {
  name?: string;
  phone?: string | null;
  is_active?: boolean;
}

export interface TruckOwnerUpdateInput {
  name?: string;
  phone?: string | null;
  is_active?: boolean;
}

export interface VehicleUpdateInput {
  vehicle_no?: string;
  is_active?: boolean;
}

export type GstPaidBy = "consignor" | "consignee" | "transporter" | "exempted";

export interface Bilti {
  id: string;
  firm_id: string;
  loading_slip_id: string | null;
  bilti_no: string;
  bilti_date: string;
  consignor: string;
  consignee: string;
  from_location: string;
  to_location: string;
  vehicle: Vehicle;
  palti_vehicle: Vehicle | null;
  truck_owner: TruckOwner;
  agent: Agent | null;
  goods_description: string;
  weight: string;
  charged_weight: string | null;
  package_count: string | null;
  package_unit: string | null;
  freight_rate: string | null;
  freight: string;
  dalali: string;
  freight_difference: string;
  advance_to_owner: string;
  other_charges: string;
  kanta_charges: string;
  bahi_charges: string;
  service_tax: string;
  hamali: string;
  p_freight: string;
  gst_paid_by: GstPaidBy | null;
  eway_bill_no: string | null;
  invoice_value: string | null;
  insured: boolean | null;
  insurance_company: string | null;
  insurance_policy_no: string | null;
  insurance_amount: string | null;
  insurance_date: string | null;
  insurance_risk: string | null;
  insurance_agent_name: string | null;
  goods_value_declared: string | null;
  remark: string | null;
  grand_total: string;
  topay: string;
  created_at: string;
  updated_at: string;
}

/** BiltiPrint omits freight_difference -- the hidden-field rule enforced
 * server-side. See backend/app/schemas/bilti.py::BiltiPrint.
 */
export type BiltiPrint = Omit<Bilti, "freight_difference">;

export interface BiltiCreateInput {
  firm_id: string;
  loading_slip_id?: string | null;
  bilti_no: string;
  bilti_date: string;
  consignor: string;
  consignee: string;
  from_location: string;
  to_location: string;
  vehicle_no: string;
  palti_vehicle_no?: string | null;
  truck_owner_name: string;
  agent_name?: string | null;
  goods_description: string;
  weight: string;
  charged_weight?: string | null;
  package_count?: string | null;
  package_unit?: string | null;
  freight: number;
  freight_rate?: number | null;
  dalali?: number;
  advance_to_owner?: number;
  freight_difference?: number;
  other_charges?: number;
  kanta_charges?: number;
  bahi_charges?: number;
  service_tax?: number;
  hamali?: number;
  p_freight?: number;
  gst_paid_by?: GstPaidBy | null;
  eway_bill_no?: string | null;
  invoice_value?: number | null;
  insured?: boolean | null;
  insurance_company?: string | null;
  insurance_policy_no?: string | null;
  insurance_amount?: number | null;
  insurance_date?: string | null;
  insurance_risk?: string | null;
  insurance_agent_name?: string | null;
  goods_value_declared?: number | null;
  remark?: string | null;
}

export type BiltiUpdateInput = Partial<BiltiCreateInput>;
