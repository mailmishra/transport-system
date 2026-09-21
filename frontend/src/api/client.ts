/** Thin fetch wrapper. Ports the error-shape handling proven in the old
 * concept/index.html's apiRequest(): FastAPI/Pydantic 422s arrive as
 * {detail: [{loc:[...,"field"], msg:"..."}]} -- keep that structured
 * (ApiError.fields) so a form can show each message under its own input
 * instead of joining them into one bottom-of-form string.
 */
const API_BASE = "/api";

export class ApiError extends Error {
  status: number;
  fields: Record<string, string> | null;

  constructor(message: string, status: number, fields: Record<string, string> | null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.fields = fields;
  }
}

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: body !== undefined ? { "Content-Type": "application/json" } : undefined,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (res.status === 204) {
    return undefined as T;
  }

  let data: unknown = null;
  try {
    data = await res.json();
  } catch {
    // no body (e.g. some error responses) -- fall through to status text
  }

  if (!res.ok) {
    const detail = (data as { detail?: unknown } | null)?.detail;
    let message = typeof detail === "string" ? detail : res.statusText;
    let fields: Record<string, string> | null = null;
    if (Array.isArray(detail)) {
      fields = {};
      for (const e of detail as Array<{ loc?: unknown[]; msg: string }>) {
        const key = String((e.loc ?? []).at(-1));
        fields[key] = e.msg;
      }
      message = Object.entries(fields).map(([f, m]) => `${f}: ${m}`).join("; ");
    }
    throw new ApiError(message || "Request failed", res.status, fields);
  }

  return data as T;
}

export function buildQuery(params: Record<string, string | number | boolean | undefined | null>): string {
  const usp = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== "") usp.set(k, String(v));
  }
  const qs = usp.toString();
  return qs ? `?${qs}` : "";
}

export const api = {
  get: <T>(path: string) => request<T>("GET", path),
  post: <T>(path: string, body?: unknown) => request<T>("POST", path, body),
  patch: <T>(path: string, body?: unknown) => request<T>("PATCH", path, body),
  delete: (path: string) => request<void>("DELETE", path),
};
