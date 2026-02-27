/**
 * SultanPage — Sovereign Quranic Study System
 * Embeds or links to SULTAN (AS-SULTAN planet)
 */
import { useState } from "react";
import { Link } from "wouter";
import { BookOpen, ExternalLink, Loader2 } from "lucide-react";

const SULTAN_URL = import.meta.env.VITE_SULTAN_URL || "https://sultan.mrf103.com";

export default function SultanPage() {
  const [iframeLoaded, setIframeLoaded] = useState(false);

  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Link href="/galaxy">
              <span className="text-slate-400 hover:text-cyan-400 cursor-pointer">
                ← Galaxy
              </span>
            </Link>
            <h1 className="text-2xl font-bold flex items-center gap-2">
              <BookOpen className="h-7 w-7 text-amber-500" />
              AS-SULTAN — السلطان
            </h1>
          </div>
          <a
            href={SULTAN_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300 text-sm"
          >
            <ExternalLink className="h-4 w-4" />
            فتح في نافذة جديدة
          </a>
        </div>

        <div className="relative rounded-lg overflow-hidden border border-slate-700/50 bg-slate-900/50">
          {!iframeLoaded && (
            <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80">
              <Loader2 className="h-10 w-10 animate-spin text-cyan-500" />
            </div>
          )}
          <iframe
            src={SULTAN_URL}
            title="SULTAN — Sovereign Quranic Study"
            className="w-full h-[calc(100vh-12rem)] min-h-[500px] border-0"
            onLoad={() => setIframeLoaded(true)}
          />
        </div>
      </div>
    </div>
  );
}
