/**
 * SovereignMonitor — C2 Hub observability layer
 * Tracks: Ollama CPU/RAM, X-Bio WS connections, 11 Planets health
 * Zero-data-leakage — all via local proxy + JWT
 */
import { getApiUrl } from "@/lib/api-config";
import { getAuthHeader } from "@/lib/authStorage";

export interface PlanetHealth {
  id: string;
  name: string;
  status: string;
}

export interface MonitorAggregate {
  timestamp: string;
  ollama: {
    status: string;
    modelsLoaded: number;
    cpuPct: number | null;
    memBytes: number | null;
  };
  xbio: {
    wsConnections: number;
  };
  planets: PlanetHealth[];
  pulse: {
    summary: { total: number; online: number };
    uptimePct: number;
  } | null;
}

export async function fetchMonitorAggregate(): Promise<MonitorAggregate> {
  const url = getApiUrl("/api/sovereign/monitor/aggregate");
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...getAuthHeader(),
  };

  const response = await fetch(url, {
    method: "GET",
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error((err as { message?: string }).message ?? `HTTP ${response.status}`);
  }

  return response.json();
}

export const sovereignMonitor = {
  fetchMonitorAggregate,
};
