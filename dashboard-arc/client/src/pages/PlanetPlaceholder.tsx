/**
 * PlanetPlaceholder — Isolated node view for planets without dedicated pages
 * MRF Sovereign Node v1.0
 */
import { useRoute } from "wouter";
import { Link } from "wouter";
import { Orbit, ArrowLeft } from "lucide-react";

export default function PlanetPlaceholder() {
  const [, params] = useRoute("/galaxy/:planetId");
  const planetId = params?.planetId ?? "unknown";

  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100 flex items-center justify-center">
      <div className="text-center max-w-md px-4">
        <Orbit className="h-16 w-16 mx-auto mb-6 text-cyan-500/60" />
        <h1 className="text-2xl font-bold text-slate-200 mb-2">{planetId}</h1>
        <p className="text-slate-400 mb-8">
          Isolated node coming soon. Sovereign routing active.
        </p>
        <Link href="/galaxy">
          <a className="inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300">
            <ArrowLeft className="h-4 w-4" />
            Back to Galaxy
          </a>
        </Link>
      </div>
    </div>
  );
}
