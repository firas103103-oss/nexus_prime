/**
 * NexusCoreRouter — Dynamic lazy-loading of 11 AI Planets
 * MRF Sovereign Node v1.0 — isolated nodes, zero-trust routing
 */
import { lazy, Suspense } from "react";
import { useRoute } from "wouter";
import { EnhancedLoadingFallback } from "@/components/EnhancedLoadingFallback";

const XBioSentinel = lazy(() => import("@/pages/XBioSentinel"));
const SultanPage = lazy(() => import("@/pages/SultanPage"));
const GalaxyDashboard = lazy(() => import("@/pages/GalaxyDashboard"));
const PlanetPlaceholder = lazy(() => import("@/pages/PlanetPlaceholder"));

const PLANET_ROUTES: Record<string, React.LazyExoticComponent<React.ComponentType<any>>> = {
  "X-BIO": XBioSentinel,
  "XBIO": XBioSentinel,
  "xbio": XBioSentinel,
  "AS-SULTAN": SultanPage,
  "ASSULTAN": SultanPage,
  "sultan": SultanPage,
  "SHADOW-7-PLANET": PlanetPlaceholder,
  "N-TARGET": PlanetPlaceholder,
  "SEC-GUARD": PlanetPlaceholder,
  "OPS-CTRL": PlanetPlaceholder,
  "AI-ARCH": PlanetPlaceholder,
  "CLONE-HUB": PlanetPlaceholder,
  "RAG-CORE": PlanetPlaceholder,
  "NAV-ORACLE": PlanetPlaceholder,
  "NEXUS-ANALYST": PlanetPlaceholder,
  "LEGAL-EAGLE": PlanetPlaceholder,
};

export function NexusCoreRouter() {
  const [, params] = useRoute("/galaxy/:planetId");
  const planetId = params?.planetId;

  if (!planetId) {
    return (
      <Suspense fallback={<EnhancedLoadingFallback timeout={5000} />}>
        <GalaxyDashboard />
      </Suspense>
    );
  }

  const key = planetId.toUpperCase().replace(/\s/g, "-");
  const Component =
    PLANET_ROUTES[planetId] ?? PLANET_ROUTES[key] ?? PlanetPlaceholder;

  return (
    <Suspense fallback={<EnhancedLoadingFallback timeout={5000} />}>
      <Component />
    </Suspense>
  );
}

export default NexusCoreRouter;
