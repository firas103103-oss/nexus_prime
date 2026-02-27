/**
 * nexusAiService — Sovereign AI communication layer
 * Zero-data-leakage: all requests via local proxy + authStorage JWT
 * MRF Sovereign Node v1.0
 */
import { getApiUrl } from "@/lib/api-config";
import { getAuthHeader } from "@/lib/authStorage";
import { fetchWithRetry } from "@/lib/fetchWithRetry";

export type SovereignAiErrorCode =
  | "offline"
  | "unauthorized"
  | "proxy_unavailable"
  | "prompt_required"
  | "stream_error"
  | "unknown";

export interface SovereignAiError {
  code: SovereignAiErrorCode;
  message: string;
}

export interface GenerateChunk {
  model?: string;
  response?: string;
  done?: boolean;
  done_reason?: string;
}

export interface AskSovereignAiOptions {
  model?: string;
  prompt: string;
  stream?: boolean;
  onChunk?: (text: string) => void;
  onDone?: () => void;
  signal?: AbortSignal;
}

function isOnline(): boolean {
  return typeof navigator !== "undefined" && navigator.onLine;
}

export async function askSovereignAi(options: AskSovereignAiOptions): Promise<string> {
  const { model = "llama3.2:3b", prompt, stream = true, onChunk, onDone, signal } = options;

  if (!prompt || typeof prompt !== "string" || prompt.trim().length === 0) {
    throw { code: "prompt_required" as SovereignAiErrorCode, message: "Prompt is required" } as SovereignAiError;
  }

  if (!isOnline()) {
    throw { code: "offline" as SovereignAiErrorCode, message: "Network offline" } as SovereignAiError;
  }

  const authHeaders = getAuthHeader();
  const url = getApiUrl("/api/ollama/generate");
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...authHeaders,
  };

  const response = await fetchWithRetry(url, {
    method: "POST",
    headers,
    body: JSON.stringify({ model, prompt, stream }),
    credentials: "include",
    timeoutMs: 30000,
    retries: 2,
  });

  if (response.status === 401) {
    throw { code: "unauthorized" as SovereignAiErrorCode, message: "Unauthorized" } as SovereignAiError;
  }

  if (response.status === 502 || response.status === 503) {
    const data = await response.json().catch(() => ({}));
    throw {
      code: "proxy_unavailable" as SovereignAiErrorCode,
      message: (data as { message?: string }).message ?? "AI service unavailable",
    } as SovereignAiError;
  }

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw {
      code: "unknown" as SovereignAiErrorCode,
      message: (data as { error?: string; message?: string }).message ?? (data as { error?: string }).error ?? `HTTP ${response.status}`,
    } as SovereignAiError;
  }

  if (!stream) {
    const data = (await response.json()) as { response?: string };
    onDone?.();
    return data.response ?? "";
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw { code: "stream_error" as SovereignAiErrorCode, message: "No response body" } as SovereignAiError;
  }

  const decoder = new TextDecoder();
  let fullText = "";
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        try {
          const chunk = JSON.parse(trimmed) as GenerateChunk;
          if (chunk.response) {
            fullText += chunk.response;
            onChunk?.(chunk.response);
          }
          if (chunk.done) {
            onDone?.();
          }
        } catch {
          /* skip malformed line */
        }
      }
    }
    if (buffer.trim()) {
      try {
        const chunk = JSON.parse(buffer.trim()) as GenerateChunk;
        if (chunk.response) {
          fullText += chunk.response;
          onChunk?.(chunk.response);
        }
        if (chunk.done) onDone?.();
      } catch {
        /* skip */
      }
    }
  } finally {
    reader.releaseLock();
  }

  return fullText;
}

export function isSovereignAiError(err: unknown): err is SovereignAiError {
  return (
    typeof err === "object" &&
    err !== null &&
    "code" in err &&
    typeof (err as SovereignAiError).code === "string" &&
    "message" in err &&
    typeof (err as SovereignAiError).message === "string"
  );
}
