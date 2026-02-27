/**
 * SystemHealthCheck — Hidden diagnostic utility
 * Local Storage, Ollama, X-Bio WebSocket
 */
import { getApiUrl } from "@/lib/api-config";

export interface HealthCheckResult {
  localStorage: { ok: boolean; error?: string };
  ollama: { ok: boolean; error?: string; models?: number };
  xbioWebSocket: { ok: boolean; error?: string };
  timestamp: string;
}

const STORAGE_TEST_KEY = "_nexus_health_check";

export async function runSystemHealthCheck(): Promise<HealthCheckResult> {
  const result: HealthCheckResult = {
    localStorage: { ok: false },
    ollama: { ok: false },
    xbioWebSocket: { ok: false },
    timestamp: new Date().toISOString(),
  };

  try {
    localStorage.setItem(STORAGE_TEST_KEY, "1");
    const v = localStorage.getItem(STORAGE_TEST_KEY);
    localStorage.removeItem(STORAGE_TEST_KEY);
    result.localStorage = { ok: v === "1" };
  } catch (e) {
    result.localStorage = { ok: false, error: (e as Error).message };
  }

  try {
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), 10000);
    const r = await fetch(getApiUrl("/api/ollama/tags"), {
      signal: controller.signal,
      credentials: "include",
    });
    clearTimeout(t);
    if (r.ok) {
      const d = (await r.json()) as { models?: unknown[] };
      result.ollama = { ok: true, models: d.models?.length ?? 0 };
    } else {
      result.ollama = { ok: false, error: `HTTP ${r.status}` };
    }
  } catch (e) {
    result.ollama = { ok: false, error: (e as Error).message };
  }

  const wsPort = import.meta.env.VITE_IOT_WS_PORT || "8081";
  const wsUrl = `ws://${window.location.hostname}:${wsPort}`;
  await new Promise<void>((resolve) => {
    const ws = new WebSocket(wsUrl);
    const done = () => {
      try {
        ws.close();
      } catch {
        /* ignore */
      }
      resolve();
    };
    ws.onopen = () => {
      result.xbioWebSocket = { ok: true };
      done();
    };
    ws.onerror = () => {
      result.xbioWebSocket = { ok: false, error: "Handshake failed" };
      done();
    };
    ws.onclose = () => {
      if (!result.xbioWebSocket.error) result.xbioWebSocket = { ok: false, error: "Closed" };
      done();
    };
    setTimeout(done, 5000);
  });

  return result;
}
