/**
 * SovereignCommandDispatcher — Encrypted outbound commands
 * Uses JWT from SovereignMasterContext for IoT nodes / AI sub-processes
 * Zero-data-leakage
 */
import { getApiUrl } from "@/lib/api-config";
import { getAuthHeader } from "@/lib/authStorage";

export const EMERGENCY_PROTOCOLS = [
  "QUARANTINE_NODE",
  "FULL_LOCKDOWN",
  "ISOLATE_PLANET",
  "FLUSH_CACHE",
  "RESTART_OLLAMA",
  "XBIO_SAFE_MODE",
] as const;

export type EmergencyProtocol = (typeof EMERGENCY_PROTOCOLS)[number];

export interface DispatchResult {
  status: string;
  protocol: string;
  target: string;
  timestamp: string;
  message: string;
}

export async function dispatchCommand(
  protocol: EmergencyProtocol,
  target?: string,
  payload?: Record<string, unknown>
): Promise<DispatchResult> {
  const url = getApiUrl("/api/sovereign/command/dispatch");
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...getAuthHeader(),
  };

  // JWT preferred; session (credentials: include) also accepted by server

  const response = await fetch(url, {
    method: "POST",
    headers,
    credentials: "include",
    body: JSON.stringify({ protocol, target, payload }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error((err as { message?: string }).message ?? `HTTP ${response.status}`);
  }

  return response.json();
}

export async function fetchProtocols(): Promise<string[]> {
  const url = getApiUrl("/api/sovereign/command/protocols");
  const headers: Record<string, string> = {
    ...getAuthHeader(),
  };

  const response = await fetch(url, {
    method: "GET",
    headers,
    credentials: "include",
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = (await response.json()) as { protocols: string[] };
  return data.protocols ?? [];
}

export const sovereignCommandDispatcher = {
  dispatchCommand,
  fetchProtocols,
  EMERGENCY_PROTOCOLS,
};
