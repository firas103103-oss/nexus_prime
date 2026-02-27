/**
 * XBioGateway — Secure X-Bio API wrapper
 * Ingest, telemetry, algorithms — local-only via configured base URL
 */
const XBIO_BASE = import.meta.env.VITE_XBIO_API_URL || "https://xbio.mrf103.com";

export interface XBioHealth {
  status?: string;
  service?: string;
}

export interface XBioPatents {
  patents?: string[];
  implemented?: string[];
}

export interface TelemetryRow {
  device_id?: string;
  temperature?: number;
  humidity?: number;
  pressure?: number;
  gas_resistance?: number;
  iaq?: number;
  sri?: number;
  msi?: number;
  spi?: number;
  truth_score?: number;
  state?: string;
  alert?: boolean;
  created_at?: string;
}

export interface IngestPayload {
  device_id: string;
  temperature?: number;
  humidity?: number;
  pressure?: number;
  gas_resistance?: number;
  iaq?: number;
  metadata?: Record<string, unknown>;
}

async function fetchXBio<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${XBIO_BASE}${path.startsWith("/") ? path : `/${path}`}`;
  const res = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error((err as { error?: string }).error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function getHealth(): Promise<XBioHealth> {
  return fetchXBio<XBioHealth>("/health");
}

export async function getPatents(): Promise<XBioPatents> {
  return fetchXBio<XBioPatents>("/api/patents");
}

export async function getLatestTelemetry(limit = 5): Promise<{ data: TelemetryRow[] }> {
  return fetchXBio<{ data: TelemetryRow[] }>(`/api/telemetry/latest?limit=${limit}`);
}

export async function ingestTelemetry(payload: IngestPayload): Promise<{ ok?: boolean }> {
  return fetchXBio<{ ok?: boolean }>("/api/ingest", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export const XBioGateway = {
  getHealth,
  getPatents,
  getLatestTelemetry,
  ingestTelemetry,
  baseUrl: XBIO_BASE,
};

export default XBioGateway;
