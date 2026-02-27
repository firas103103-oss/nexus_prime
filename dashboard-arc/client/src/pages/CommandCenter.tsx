/**
 * CommandCenter — Sovereign C2 Hub Telemetry Dashboard
 * Aggregates: Ollama CPU/RAM, X-Bio WS, 11 Planets, Threat Inquiry, Manual Override
 */
import { useEffect, useState, useCallback } from "react";
import { useSovereign } from "@/contexts/SovereignMasterContext";
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import {
  sovereignMonitor,
  type MonitorAggregate,
} from "@/services/SovereignMonitor";
import {
  threatInquiryService,
  type InquiryResult,
} from "@/services/ThreatInquiryService";
import {
  sovereignCommandDispatcher,
  type EmergencyProtocol,
} from "@/services/SovereignCommandDispatcher";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Cpu,
  Activity,
  Orbit,
  Shield,
  AlertTriangle,
  RefreshCw,
  Loader2,
  Zap,
  CheckCircle2,
  XCircle,
} from "lucide-react";

const STATUS_COLORS: Record<string, string> = {
  online: "bg-emerald-500/20 text-emerald-400 border-emerald-500/50",
  offline: "bg-red-500/20 text-red-400 border-red-500/50",
  degraded: "bg-amber-500/20 text-amber-400 border-amber-500/50",
};

function StatusBadge({ status }: { status: string }) {
  const color = STATUS_COLORS[status] ?? STATUS_COLORS.offline;
  const Icon = status === "online" ? CheckCircle2 : XCircle;
  return (
    <Badge variant="outline" className={`${color} gap-1`}>
      <Icon className="h-3 w-3" />
      {status}
    </Badge>
  );
}

export default function CommandCenter() {
  const { auth } = useSovereign();
  const [monitor, setMonitor] = useState<MonitorAggregate | null>(null);
  const [monitorLoading, setMonitorLoading] = useState(true);
  const [monitorError, setMonitorError] = useState<string | null>(null);

  const [threatInput, setThreatInput] = useState("");
  const [threatResult, setThreatResult] = useState<InquiryResult | null>(null);
  const [threatLoading, setThreatLoading] = useState(false);

  const [overrideProtocol, setOverrideProtocol] = useState<EmergencyProtocol | "">("");
  const [overrideLoading, setOverrideLoading] = useState(false);
  const [overrideMessage, setOverrideMessage] = useState<string | null>(null);

  const fetchMonitor = useCallback(async () => {
    setMonitorLoading(true);
    setMonitorError(null);
    try {
      const data = await sovereignMonitor.fetchMonitorAggregate();
      setMonitor(data);
    } catch (err) {
      setMonitorError(err instanceof Error ? err.message : "Monitor unavailable");
      setMonitor(null);
    } finally {
      setMonitorLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMonitor();
    const interval = setInterval(fetchMonitor, 15000);
    return () => clearInterval(interval);
  }, [fetchMonitor]);

  const runThreatAnalysis = useCallback(async () => {
    if (!threatInput.trim()) return;
    setThreatLoading(true);
    setThreatResult(null);
    try {
      const result = await threatInquiryService.analyzeIncomingData(
        threatInput.trim(),
        5
      );
      setThreatResult(result);
    } catch (err) {
      setThreatResult({
        input: threatInput,
        embedding: [],
        matches: [],
        anomalyDetected: false,
      });
    } finally {
      setThreatLoading(false);
    }
  }, [threatInput]);

  const triggerOverride = useCallback(async () => {
    if (!overrideProtocol) return;
    setOverrideLoading(true);
    setOverrideMessage(null);
    try {
      const res = await sovereignCommandDispatcher.dispatchCommand(
        overrideProtocol as EmergencyProtocol
      );
      setOverrideMessage(res.message ?? "Dispatched");
    } catch (err) {
      setOverrideMessage(err instanceof Error ? err.message : "Dispatch failed");
    } finally {
      setOverrideLoading(false);
    }
  }, [overrideProtocol]);

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b border-slate-700/50 px-4 bg-[#0a0e17]">
          <SidebarTrigger className="-ml-1 text-slate-300" />
        </header>
        <div className="min-h-[calc(100vh-4rem)] bg-[#0a0e17] text-slate-100">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-violet-500 bg-clip-text text-transparent flex items-center gap-2">
              <Shield className="h-8 w-8" />
              Sovereign Command & Control Hub
            </h1>
            <p className="text-slate-400 mt-1">
              {auth.user?.email ?? "Operator"} · Zero-trust · Local-only
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={fetchMonitor}
            disabled={monitorLoading}
            className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
          >
            {monitorLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="h-4 w-4" />
            )}
            <span className="ml-2">Refresh</span>
          </Button>
        </div>

        {monitorError && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            {monitorError}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Card className="bg-slate-900/50 border-slate-700/50 backdrop-blur-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex items-center gap-2">
                <Cpu className="h-5 w-5 text-cyan-400" />
                Ollama (Local AI)
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Status</span>
                <StatusBadge status={monitor?.ollama?.status ?? "offline"} />
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Models loaded</span>
                <span>{monitor?.ollama?.modelsLoaded ?? "—"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">CPU</span>
                <span>
                  {monitor?.ollama?.cpuPct != null
                    ? `${monitor.ollama.cpuPct.toFixed(1)}%`
                    : "—"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Memory</span>
                <span>
                  {monitor?.ollama?.memBytes != null
                    ? `${(monitor.ollama.memBytes / 1e6).toFixed(1)} MB`
                    : "—"}
                </span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-slate-700/50 backdrop-blur-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex items-center gap-2">
                <Activity className="h-5 w-5 text-violet-400" />
                X-Bio WebSocket
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Active connections</span>
                <span className="text-2xl font-bold text-cyan-400">
                  {monitor?.xbio?.wsConnections ?? "—"}
                </span>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-slate-900/50 border-slate-700/50 backdrop-blur-sm mb-8">
          <CardHeader className="pb-2">
            <CardTitle className="text-lg flex items-center gap-2">
              <Orbit className="h-5 w-5 text-emerald-400" />
              11 Nexus Planets
            </CardTitle>
            {monitor?.pulse && (
              <p className="text-sm text-slate-500">
                {monitor.pulse.summary.online}/{monitor.pulse.summary.total} online ·{" "}
                {monitor.pulse.uptimePct}% uptime
              </p>
            )}
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
              {(monitor?.planets ?? []).map((p) => (
                <div
                  key={p.id}
                  className="flex items-center justify-between gap-2 p-2 rounded bg-slate-800/50"
                >
                  <span className="text-sm truncate">{p.name}</span>
                  <StatusBadge status={p.status} />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Card className="bg-slate-900/50 border-slate-700/50 backdrop-blur-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex items-center gap-2">
                <Shield className="h-5 w-5 text-amber-400" />
                Threat Inquiry (Sultan Semantic)
              </CardTitle>
              <p className="text-xs text-slate-500">
                Logs/data → nomic-embed-text → Security-Vector-Store
              </p>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input
                placeholder="Paste log or data to analyze..."
                value={threatInput}
                onChange={(e) => setThreatInput(e.target.value)}
                className="bg-slate-800/50 border-slate-600"
              />
              <Button
                onClick={runThreatAnalysis}
                disabled={threatLoading || !threatInput.trim()}
                variant="outline"
                className="border-amber-500/50 text-amber-400"
              >
                {threatLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  "Analyze"
                )}
              </Button>
              {threatResult && (
                <div className="mt-4 p-3 rounded bg-slate-800/50 text-sm">
                  <div
                    className={`font-medium mb-2 ${
                      threatResult.anomalyDetected ? "text-red-400" : "text-emerald-400"
                    }`}
                  >
                    {threatResult.anomalyDetected ? "⚠ Anomaly detected" : "✓ No anomaly"}
                  </div>
                  {threatResult.matches.slice(0, 3).map((m) => (
                    <div key={m.vectorId} className="flex justify-between text-slate-400">
                      <span>{m.vectorId}</span>
                      <span>{(m.score * 100).toFixed(0)}%</span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-slate-700/50 backdrop-blur-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex items-center gap-2">
                <Zap className="h-5 w-5 text-red-400" />
                Manual Override
              </CardTitle>
              <p className="text-xs text-slate-500">
                Emergency protocols — JWT-verified dispatch
              </p>
            </CardHeader>
            <CardContent className="space-y-4">
              <select
                value={overrideProtocol}
                onChange={(e) =>
                  setOverrideProtocol(e.target.value as EmergencyProtocol | "")
                }
                className="w-full p-2 rounded bg-slate-800/50 border border-slate-600 text-slate-200"
              >
                <option value="">Select protocol...</option>
                {sovereignCommandDispatcher.EMERGENCY_PROTOCOLS.map((p) => (
                  <option key={p} value={p}>
                    {p}
                  </option>
                ))}
              </select>
              <Button
                onClick={triggerOverride}
                disabled={overrideLoading || !overrideProtocol}
                variant="destructive"
              >
                {overrideLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  "Execute"
                )}
              </Button>
              {overrideMessage && (
                <p className="text-sm text-slate-400">{overrideMessage}</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
