/**
 * GalaxyDashboard — 11-Planet Galaxy View
 * Real-time sync indicators, memory usage, isolated planet states
 * Dark mode, glassmorphism, neon accents
 */
import { useEffect, useState, useCallback } from "react";
import { Link } from "wouter";
import {
  nexusTelemetryService,
  type PulseResponse,
  type AgentsResponse,
  type AgentPlanet,
} from "@/services/nexusTelemetryService";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Activity,
  Cpu,
  RefreshCw,
  AlertCircle,
  CheckCircle2,
  XCircle,
  Loader2,
  Orbit,
} from "lucide-react";

const STATUS_COLORS: Record<string, string> = {
  online: "bg-emerald-500/20 text-emerald-400 border-emerald-500/50",
  offline: "bg-red-500/20 text-red-400 border-red-500/50",
  degraded: "bg-amber-500/20 text-amber-400 border-amber-500/50",
  error: "bg-red-500/20 text-red-400 border-red-500/50",
};

function StatusBadge({ status }: { status: string }) {
  const color = STATUS_COLORS[status] ?? STATUS_COLORS.offline;
  const Icon =
    status === "online"
      ? CheckCircle2
      : status === "degraded"
        ? AlertCircle
        : XCircle;
  return (
    <Badge variant="outline" className={`${color} gap-1`}>
      <Icon className="h-3 w-3" />
      {status}
    </Badge>
  );
}

export default function GalaxyDashboard() {
  const [pulse, setPulse] = useState<PulseResponse | null>(null);
  const [agents, setAgents] = useState<AgentsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [pulseRes, agentsRes] = await Promise.all([
        nexusTelemetryService.fetchPulse(),
        nexusTelemetryService.fetchAgents(),
      ]);
      setPulse(pulseRes);
      setAgents(agentsRes);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load telemetry");
      setPulse(null);
      setAgents(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const serviceMap = new Map<string, string>();
  if (pulse?.services) {
    for (const s of pulse.services) {
      serviceMap.set(s.name, s.status);
    }
  }

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

  const getPlanetStatus = (agent: AgentPlanet): string => {
    const svcName = AGENT_TO_SERVICE[agent.id];
    return svcName ? (serviceMap.get(svcName) ?? "offline") : "offline";
  };

  if (loading && !pulse) {
    return (
      <div className="min-h-screen bg-[#0a0e17] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-12 w-12 animate-spin text-cyan-500" />
          <p className="text-slate-400">Loading galaxy telemetry...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent flex items-center gap-2">
              <Orbit className="h-8 w-8" />
              NEXUS Galaxy
            </h1>
            <p className="text-slate-400 mt-1">
              {pulse
                ? `${pulse.summary.online}/${pulse.summary.total} services online · ${pulse.uptime_pct}% uptime`
                : "11 AI Planets · Sovereign Node v1.0"}
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={fetchData}
            disabled={loading}
            className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="h-4 w-4" />
            )}
            <span className="ml-2">Refresh</span>
          </Button>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 flex items-center gap-2">
            <AlertCircle className="h-5 w-5" />
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {(agents?.agents ?? []).map((agent) => {
            const status = getPlanetStatus(agent);
            const href =
              agent.id === "X-BIO"
                ? "/galaxy/X-BIO"
                : agent.id === "AS-SULTAN"
                  ? "/sultan"
                  : `/galaxy/${agent.id}`;
            return (
              <Link key={agent.id} href={href}>
                <Card
                  className="bg-slate-900/50 border-slate-700/50 hover:border-cyan-500/50 hover:bg-slate-800/50 transition-all cursor-pointer backdrop-blur-sm"
                  style={{ boxShadow: "0 0 20px rgba(6, 182, 212, 0.05)" }}
                >
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg text-slate-200">
                        {agent.name}
                      </CardTitle>
                      <StatusBadge status={status} />
                    </div>
                    <p className="text-xs text-slate-500">{agent.id}</p>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <p className="text-sm text-slate-400 line-clamp-2">
                      {agent.specialization ?? agent.title ?? "—"}
                    </p>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>

        {(!agents?.agents?.length || agents.agents.length === 0) && !loading && (
          <div className="text-center py-16 text-slate-500">
            <Cpu className="h-16 w-16 mx-auto mb-4 opacity-50" />
            <p>No planets in registry. Check nexus_nerve connection.</p>
          </div>
        )}
      </div>
    </div>
  );
}
