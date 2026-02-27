/**
 * Sovereign Monitor Routes — C2 Hub aggregate telemetry
 * CPU/RAM Ollama, X-Bio WS connections, 11 Planets health
 * Zero external leakage — all via local proxy
 */
import { Router, type Request, type Response } from "express";
import logger from "../utils/logger";
import { iotService } from "../services/iot_service";

const NERVE_URL = process.env.NERVE_URL || "http://nexus_nerve:8200";
const OLLAMA_URL = process.env.OLLAMA_URL || "http://nexus_ollama:11434";

async function fetchJson<T>(url: string): Promise<T | null> {
  try {
    const resp = await fetch(url);
    const data = await resp.json().catch(() => null);
    return resp.ok ? (data as T) : null;
  } catch {
    return null;
  }
}

const monitorRouter = Router();

monitorRouter.get("/aggregate", async (_req: Request, res: Response) => {
  try {
    const [pulse, agents, ollamaTags, ollamaMetricsText] = await Promise.all([
      fetchJson<{ services: Array<{ name: string; status: string }>; summary: { total: number; online: number }; uptime_pct: number }>(
        `${NERVE_URL}/api/pulse`
      ),
      fetchJson<{ agents: Array<{ id: string; name: string }> }>(`${NERVE_URL}/api/agents`),
      fetchJson<{ models?: Array<{ name: string; size?: number }> }>(`${OLLAMA_URL}/api/tags`),
      fetch(`${OLLAMA_URL}/metrics`).then((r) => (r.ok ? r.text() : null)).catch(() => null),
    ]);

    const xbioWsCount = typeof iotService.getXBioWsConnectionCount === "function"
      ? iotService.getXBioWsConnectionCount()
      : 0;

    const serviceMap = new Map<string, string>();
    if (pulse?.services) {
      for (const s of pulse.services) {
        serviceMap.set(s.name, s.status);
      }
    }

    const ollamaOnline = ollamaTags !== null;
    const ollamaStatus = ollamaOnline ? "online" : (serviceMap.get("X-Bio Sentinel") ?? serviceMap.get("nexus_ollama") ?? "offline");
    const ollamaModels = ollamaTags?.models ?? [];

    const AGENT_TO_SERVICE: Record<string, string> = {
      "X-BIO": "X-Bio Sentinel",
      "AS-SULTAN": "Ecosystem API",
      "SHADOW-7-PLANET": "Shadow7 API",
      "RAG-CORE": "Cortex",
      "AI-ARCH": "Dashboard",
      "NAV-ORACLE": "Oracle API",
      "NEXUS-ANALYST": "Cortex",
      "OPS-CTRL": "Cortex",
      "SEC-GUARD": "Auth Service",
    };

    const planets = (agents?.agents ?? []).map((a) => {
      const svcName = AGENT_TO_SERVICE[a.id] ?? a.name;
      return {
        id: a.id,
        name: a.name,
        status: serviceMap.get(svcName) ?? "offline",
      };
    });

    const metricsText = ollamaMetricsText;
    let ollamaCpuPct: number | null = null;
    let ollamaMemBytes: number | null = null;
    if (metricsText) {
      const cpuMatch = metricsText.match(/ollama_cpu_usage_percent\s+([\d.]+)/);
      const memMatch = metricsText.match(/ollama_memory_usage_bytes\s+([\d.]+)/);
      if (cpuMatch) ollamaCpuPct = parseFloat(cpuMatch[1]);
      if (memMatch) ollamaMemBytes = parseFloat(memMatch[1]);
    }

    res.json({
      timestamp: new Date().toISOString(),
      ollama: {
        status: ollamaStatus,
        modelsLoaded: ollamaModels.length,
        cpuPct: ollamaCpuPct,
        memBytes: ollamaMemBytes,
      },
      xbio: {
        wsConnections: xbioWsCount,
      },
      planets,
      pulse: pulse
        ? {
            summary: pulse.summary,
            uptimePct: pulse.uptime_pct,
          }
        : null,
    });
  } catch (err: unknown) {
    logger.warn("[Sovereign Monitor] aggregate failed:", err);

    res.status(502).json({
      error: "monitor_unavailable",
      message: err instanceof Error ? err.message : "Monitor unavailable",
    });
  }
});

export { monitorRouter };
