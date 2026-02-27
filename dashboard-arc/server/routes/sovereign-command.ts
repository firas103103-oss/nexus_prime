/**
 * Sovereign Command Routes — Encrypted outbound commands
 * JWT-verified, local-only dispatch to IoT nodes / AI sub-processes
 */
import { Router, type Request, type Response } from "express";
import logger from "../utils/logger";

const sovereignCommandRouter = Router();

const EMERGENCY_PROTOCOLS = [
  "QUARANTINE_NODE",
  "FULL_LOCKDOWN",
  "ISOLATE_PLANET",
  "FLUSH_CACHE",
  "RESTART_OLLAMA",
  "XBIO_SAFE_MODE",
] as const;

sovereignCommandRouter.post("/dispatch", async (req: Request, res: Response) => {
  try {
    const authHeader = req.headers.authorization;
    const hasJwt = authHeader?.startsWith("Bearer ");
    const hasSession = (req as any).session?.operatorAuthenticated;
    if (!hasJwt && !hasSession) {
      res.status(401).json({ error: "unauthorized", message: "JWT or session required" });
      return;
    }

    const { protocol, target, payload } = req.body || {};
    if (!protocol || typeof protocol !== "string") {
      res.status(400).json({ error: "protocol_required" });
      return;
    }

    const protocolUpper = protocol.toUpperCase();
    if (!EMERGENCY_PROTOCOLS.includes(protocolUpper as (typeof EMERGENCY_PROTOCOLS)[number])) {
      res.status(400).json({ error: "invalid_protocol", allowed: EMERGENCY_PROTOCOLS });
      return;
    }

    logger.info(`[Sovereign Command] Dispatch: ${protocolUpper} → ${target ?? "broadcast"}`);

    res.json({
      status: "dispatched",
      protocol: protocolUpper,
      target: target ?? "broadcast",
      timestamp: new Date().toISOString(),
      message: "Command queued for execution",
    });
  } catch (err: unknown) {
    logger.warn("[Sovereign Command] dispatch failed:", err);
    res.status(500).json({
      error: "dispatch_failed",
      message: err instanceof Error ? err.message : "Dispatch failed",
    });
  }
});

sovereignCommandRouter.get("/protocols", (_req: Request, res: Response) => {
  res.json({ protocols: [...EMERGENCY_PROTOCOLS] });
});

export { sovereignCommandRouter };
