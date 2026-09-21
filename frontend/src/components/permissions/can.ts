/** Auth is not wired up yet (Supabase integration is planned separately --
 * see backend/app/deps.py::get_current_actor()). Every screen routes its
 * edit/delete affordances through this one function so that turning on
 * real roles later is a change here, not a rewrite of every module.
 */
export type Action = "view" | "create" | "edit" | "delete";
export type Resource =
  | "bilti"
  | "loading-slip"
  | "agent"
  | "truck-owner"
  | "vehicle"
  | "agent-payment"
  | "truck-owner-payment"
  | "receipt"
  | "firm";

export function can(_action: Action, _resource: Resource): boolean {
  return true;
}
