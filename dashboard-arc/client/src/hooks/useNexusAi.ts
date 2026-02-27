/**
 * useNexusAi — React hook for Sovereign AI integration
 * Integrates with useSovereign, attaches JWT via nexusAiService
 * Zero-data-leakage, MRF Sovereign Node v1.0
 */
import { useState, useCallback } from "react";
import { useSovereign } from "@/contexts/SovereignMasterContext";
import {
  askSovereignAi,
  isSovereignAiError,
  type SovereignAiError,
  type AskSovereignAiOptions,
} from "@/services/nexusAiService";

export interface UseNexusAiReturn {
  ask: (prompt: string, options?: Partial<AskSovereignAiOptions>) => Promise<string>;
  isStreaming: boolean;
  error: SovereignAiError | null;
  clearError: () => void;
  isAuthenticated: boolean;
}

export function useNexusAi(): UseNexusAiReturn {
  const { auth, setGlobalError, clearGlobalError } = useSovereign();
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<SovereignAiError | null>(null);

  const clearError = useCallback(() => {
    setError(null);
    clearGlobalError();
  }, [clearGlobalError]);

  const ask = useCallback(
    async (prompt: string, opts?: Partial<Omit<AskSovereignAiOptions, "prompt">>): Promise<string> => {
      setError(null);
      setIsStreaming(true);
      try {
        return await askSovereignAi({
          prompt,
          stream: true,
          ...opts,
        });
      } catch (err) {
        const aiErr: SovereignAiError = isSovereignAiError(err)
          ? err
          : { code: "unknown", message: err instanceof Error ? err.message : "Unknown error" };
        setError(aiErr);
        setGlobalError(new Error(aiErr.message));
        throw err;
      } finally {
        setIsStreaming(false);
      }
    },
    [setGlobalError]
  );

  return {
    ask,
    isStreaming,
    error,
    clearError,
    isAuthenticated: auth.isAuthenticated,
  };
}
