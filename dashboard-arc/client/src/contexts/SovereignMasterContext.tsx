/**
 * SovereignMasterContext — Zero-trust master context
 * Auth (JWT/LocalStorage + session), WebSocket status, global error, collaboration
 * MRF Sovereign Node v1.0 — local-only, no external API calls
 */
import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useMemo,
  useEffect,
  type ReactNode,
} from "react";
import { useAuth } from "@/hooks/useAuth";
import * as authStorage from "@/lib/authStorage";

export interface WsStatus {
  nerve: "disconnected" | "connecting" | "connected";
  xbio: "disconnected" | "connecting" | "connected";
}

export interface CollaborationState {
  activeUsers: Array<{ userId: string; timestamp: string }>;
  currentDocument: string | null;
  changes: Array<Record<string, unknown> & { timestamp: string }>;
}

export interface SovereignState {
  auth: {
    user: { id: string; email?: string; firstName?: string; lastName?: string } | null;
    isAuthenticated: boolean;
    isLoading: boolean;
  };
  ws: WsStatus;
  globalError: Error | null;
  collaboration: CollaborationState;
}

export interface SovereignActions {
  setGlobalError: (err: Error | null) => void;
  clearGlobalError: () => void;
  setWsStatus: (key: "nerve" | "xbio", status: WsStatus["nerve"] | WsStatus["xbio"]) => void;
  initCollaboration: (documentId: string, userId: string) => void;
  endCollaboration: () => void;
  broadcastChange: (change: Record<string, unknown>) => void;
  loginMutation: ReturnType<typeof useAuth>["loginMutation"];
  getToken: () => string | null;
  setToken: (token: string) => void;
  clearToken: () => void;
}

const defaultWs: WsStatus = {
  nerve: "disconnected",
  xbio: "disconnected",
};

const defaultCollaboration: CollaborationState = {
  activeUsers: [],
  currentDocument: null,
  changes: [],
};

const SovereignContext = createContext<(SovereignState & SovereignActions) | null>(null);

export function useSovereign() {
  const ctx = useContext(SovereignContext);
  if (!ctx) {
    throw new Error("useSovereign must be used within SovereignMasterProvider");
  }
  return ctx;
}

export function SovereignMasterProvider({ children }: { children: ReactNode }) {
  const { user, isAuthenticated, isLoading, loginMutation } = useAuth();
  const [ws, setWsState] = useState<WsStatus>(defaultWs);
  const [globalError, setGlobalErrorState] = useState<Error | null>(null);
  const [collaboration, setCollaboration] = useState<CollaborationState>(defaultCollaboration);

  const setGlobalError = useCallback((err: Error | null) => {
    setGlobalErrorState(err);
  }, []);

  const clearGlobalError = useCallback(() => {
    setGlobalErrorState(null);
  }, []);

  const setWsStatus = useCallback((key: "nerve" | "xbio", status: WsStatus["nerve"] | WsStatus["xbio"]) => {
    setWsState((prev) => ({ ...prev, [key]: status }));
  }, []);

  const initCollaboration = useCallback((documentId: string, userId: string) => {
    setCollaboration({
      currentDocument: documentId,
      activeUsers: [{ userId, timestamp: new Date().toISOString() }],
      changes: [],
    });
  }, []);

  const endCollaboration = useCallback(() => {
    setCollaboration(defaultCollaboration);
  }, []);

  const broadcastChange = useCallback((change: Record<string, unknown>) => {
    setCollaboration((prev) => ({
      ...prev,
      changes: [...prev.changes, { ...change, timestamp: new Date().toISOString() }],
    }));
  }, []);

  useEffect(() => {
    if (!isAuthenticated) authStorage.clearToken();
  }, [isAuthenticated]);

  const value = useMemo(
    () => ({
      auth: {
        user: user
          ? {
            id: user.id,
            email: user.email ?? undefined,
            firstName: user.firstName ?? undefined,
            lastName: user.lastName ?? undefined,
          }
          : null,
        isAuthenticated,
        isLoading,
      },
      ws,
      globalError,
      collaboration,
      setGlobalError,
      clearGlobalError,
      setWsStatus,
      initCollaboration,
      endCollaboration,
      broadcastChange,
      loginMutation,
      getToken: authStorage.getToken,
      setToken: authStorage.setToken,
      clearToken: authStorage.clearToken,
    }),
    [
      user,
      isAuthenticated,
      isLoading,
      ws,
      globalError,
      collaboration,
      setGlobalError,
      clearGlobalError,
      setWsStatus,
      initCollaboration,
      endCollaboration,
      broadcastChange,
      loginMutation,
    ]
  );

  return (
    <SovereignContext.Provider value={value}>
      {children}
    </SovereignContext.Provider>
  );
}

export default SovereignMasterProvider;
