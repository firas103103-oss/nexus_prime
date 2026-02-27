/**
 * NEXUS Telemetry Service — Local-only data fetching
 * Interfaces with nexus_nerve and nexus_ollama via dashboard server proxy
 * Zero external API calls — all requests go through /api/nerve and /api/ollama
 */
import { apiFetch } from "@/lib/api-config";

export interface PulseService {
  name: string;
  status: "online" | "offline" | "degraded" | "error";
  error?: string;
}

export interface PulseResponse {
  timestamp: string;
  summary: { total: number; online: number; degraded: number; offline: number };
  uptime_pct: number;
  services: PulseService[];
}

export interface AgentPlanet {
  id: string;
  name: string;
  title?: string;
  specialization?: string;
  tools?: string[];
}

export interface AgentsResponse {
  agents: AgentPlanet[];
  count: number;
}

export interface OllamaModel {
  name: string;
  size?: number;
  digest?: string;
}

export interface OllamaTagsResponse {
  models: OllamaModel[];
}

/**
 * Fetch system pulse (21 services status) from nexus_nerve
 */
export async function fetchPulse(): Promise<PulseResponse> {
  return apiFetch<PulseResponse>("/api/nerve/pulse");
}

/**
 * Fetch 11/12 AI Planets from nexus_nerve registry
 */
export async function fetchAgents(): Promise<AgentsResponse> {
  return apiFetch<AgentsResponse>("/api/nerve/agents");
}

/**
 * Fetch Ollama models (for memory/LLM status in GalaxyDashboard)
 */
export async function fetchOllamaModels(): Promise<OllamaTagsResponse> {
  return apiFetch<OllamaTagsResponse>("/api/ollama/tags");
}

export const nexusTelemetryService = {
  fetchPulse,
  fetchAgents,
  fetchOllamaModels,
};

export default nexusTelemetryService;
