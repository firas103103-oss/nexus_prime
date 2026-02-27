import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { runSystemHealthCheck, type HealthCheckResult } from "@/utils/SystemHealthCheck";
import { Activity, CheckCircle2, Loader2 } from "lucide-react";

export function SystemStatusModal() {
  const [open, setOpen] = useState(false);
  const [result, setResult] = useState<HealthCheckResult | null>(null);
  const [loading, setLoading] = useState(false);

  const runCheck = async () => {
    setLoading(true);
    setResult(null);
    try {
      setResult(await runSystemHealthCheck());
    } catch (err) {
      setResult({
        localStorage: { ok: false, error: (err as Error).message },
        ollama: { ok: false },
        xbioWebSocket: { ok: false },
        timestamp: new Date().toISOString(),
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => { setOpen(o); if (o && !result && !loading) runCheck(); }}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground">
          <Activity className="h-4 w-4" />
          System Status
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>System Health Check</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          {loading && <div className="flex items-center gap-2"><Loader2 className="h-4 w-4 animate-spin" />Running...</div>}
          {result && !loading && (
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span>Local Storage</span>{result.localStorage.ok ? <CheckCircle2 className="h-4 w-4 text-emerald-500" /> : <span className="text-red-500">{result.localStorage.error}</span>}</div>
              <div className="flex justify-between"><span>Ollama</span>{result.ollama.ok ? <span className="text-emerald-500">OK</span> : <span className="text-red-500">{result.ollama.error}</span>}</div>
              <div className="flex justify-between"><span>X-Bio WS</span>{result.xbioWebSocket.ok ? <CheckCircle2 className="h-4 w-4 text-emerald-500" /> : <span className="text-red-500">{result.xbioWebSocket.error}</span>}</div>
            </div>
          )}
          <Button variant="outline" size="sm" onClick={runCheck} disabled={loading}>Re-run</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
