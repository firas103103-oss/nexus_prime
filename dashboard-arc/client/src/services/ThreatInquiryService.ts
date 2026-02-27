/**
 * ThreatInquiryService — Sultan Semantic Engine integration
 * Converts logs/data to embeddings (nomic-embed-text), compares to Security-Vector-Store
 * Real-time anomaly and pattern detection
 */
import { getApiUrl } from "@/lib/api-config";
import { getAuthHeader } from "@/lib/authStorage";
import { fetchWithRetry } from "@/lib/fetchWithRetry";

export interface SecurityVector {
  id: string;
  text: string;
  embedding: number[];
  category: "threat" | "anomaly" | "pattern" | "baseline";
}

export interface InquiryResult {
  input: string;
  embedding: number[];
  matches: Array<{
    vectorId: string;
    category: string;
    score: number;
    isAnomaly: boolean;
  }>;
  anomalyDetected: boolean;
}

const SECURITY_VECTORS: Array<{ id: string; text: string; category: SecurityVector["category"] }> = [
  { id: "sv-1", text: "unauthorized access attempt failed login", category: "threat" },
  { id: "sv-2", text: "suspicious network traffic port scan", category: "threat" },
  { id: "sv-3", text: "unusual CPU spike memory exhaustion", category: "anomaly" },
  { id: "sv-4", text: "database connection timeout error", category: "anomaly" },
  { id: "sv-5", text: "normal heartbeat ping response ok", category: "baseline" },
  { id: "sv-6", text: "repeated failed authentication attempts", category: "pattern" },
];

let vectorStore: SecurityVector[] = [];
let storeInitialized = false;

function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  let dot = 0,
    normA = 0,
    normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

async function embed(text: string): Promise<number[]> {
  const url = getApiUrl("/api/ollama/embed");
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...getAuthHeader(),
  };

  const response = await fetchWithRetry(url, {
    method: "POST",
    headers,
    credentials: "include",
    body: JSON.stringify({ model: "nomic-embed-text", input: text }),
    timeoutMs: 15000,
    retries: 2,
  });

  if (!response.ok) throw new Error(`Embed failed: ${response.status}`);
  const data = (await response.json()) as { embeddings?: number[][] };
  const vec = data.embeddings?.[0];
  if (!vec) throw new Error("No embedding returned");
  return vec;
}

async function ensureVectorStore(): Promise<void> {
  if (storeInitialized) return;
  const embeddings = await Promise.all(
    SECURITY_VECTORS.map(async (v) => ({
      ...v,
      embedding: await embed(v.text),
    }))
  );
  vectorStore = embeddings;
  storeInitialized = true;
}

const ANOMALY_THRESHOLD = 0.75;
const THREAT_THRESHOLD = 0.7;

export async function analyzeIncomingData(
  logOrData: string,
  topK = 5
): Promise<InquiryResult> {
  await ensureVectorStore();

  const inputEmbedding = await embed(logOrData);

  const scored = vectorStore.map((v) => ({
    vectorId: v.id,
    category: v.category,
    score: cosineSimilarity(inputEmbedding, v.embedding),
    isAnomaly:
      v.category === "threat" && cosineSimilarity(inputEmbedding, v.embedding) >= THREAT_THRESHOLD,
  }));

  scored.sort((a, b) => b.score - a.score);
  const matches = scored.slice(0, topK);

  const anomalyDetected =
    matches.some((m) => m.isAnomaly) ||
    matches.some((m) => m.category === "anomaly" && m.score >= ANOMALY_THRESHOLD);

  return {
    input: logOrData,
    embedding: inputEmbedding,
    matches,
    anomalyDetected,
  };
}

export const threatInquiryService = {
  analyzeIncomingData,
  getSecurityVectorCount: () => SECURITY_VECTORS.length,
};
