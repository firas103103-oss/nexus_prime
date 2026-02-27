/**
 * NEXUS Proxy Routes — Zero-trust local-only proxy
 * Proxies requests to nexus_nerve and nexus_ollama (no external API calls)
 */
import { Router, type Request, type Response } from "express";
import logger from "../utils/logger";

const NERVE_URL = process.env.NERVE_URL || "http://nexus_nerve:8200";
const OLLAMA_URL = process.env.OLLAMA_URL || "http://nexus_ollama:11434";

async function proxyGet(url: string, res: Response, label: string): Promise<void> {
  try {
    const resp = await fetch(url);
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      res.status(resp.status).json(data);
      return;
    }
    res.json(data);
  } catch (err: any) {
    logger.warn(`[Nexus Proxy] ${label} failed:`, err?.message || err);
    res.status(502).json({
      error: "proxy_unavailable",
      service: label,
      message: err?.message || "Service unreachable",
    });
  }
}

const nerveRouter = Router();
nerveRouter.get("/pulse", async (_req: Request, res: Response) => {
  await proxyGet(`${NERVE_URL}/api/pulse`, res, "nerve/pulse");
});
nerveRouter.get("/agents", async (_req: Request, res: Response) => {
  await proxyGet(`${NERVE_URL}/api/agents`, res, "nerve/agents");
});

const ollamaRouter = Router();
ollamaRouter.get("/tags", async (_req: Request, res: Response) => {
  await proxyGet(`${OLLAMA_URL}/api/tags`, res, "ollama/tags");
});
ollamaRouter.post("/embed", async (req: Request, res: Response) => {
  try {
    const { model = "nomic-embed-text", input } = req.body || {};
    const text = Array.isArray(input) ? input : input ? [input] : [];
    if (text.length === 0) {
      res.status(400).json({ error: "input_required" });
      return;
    }
    const resp = await fetch(`${OLLAMA_URL}/api/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model, input: text }),
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      res.status(resp.status).json(data);
      return;
    }
    res.json(data);
  } catch (err: any) {
    logger.warn("[Nexus Proxy] ollama/embed failed:", err?.message || err);
    res.status(502).json({
      error: "proxy_unavailable",
      service: "ollama/embed",
      message: err?.message || "Service unreachable",
    });
  }
});

ollamaRouter.post("/generate", async (req: Request, res: Response) => {
  try {
    const body = req.body || {};
    const { model = "llama3.2:3b", prompt, stream = true } = body;
    if (!prompt || typeof prompt !== "string") {
      res.status(400).json({ error: "prompt_required" });
      return;
    }
    const resp = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model, prompt, stream }),
    });
    if (!resp.ok) {
      const data = await resp.json().catch(() => ({}));
      res.status(resp.status).json(data);
      return;
    }
    if (!stream) {
      const data = await resp.json().catch(() => ({}));
      res.json(data);
      return;
    }
    res.setHeader("Content-Type", "application/x-ndjson");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    res.flushHeaders?.();
    const reader = resp.body;
    if (!reader) {
      res.status(502).json({ error: "no_stream_body" });
      return;
    }
    const pump = async (r: ReadableStream<Uint8Array>) => {
      const streamReader = r.getReader();
      const decoder = new TextDecoder();
      try {
        while (true) {
          const { done, value } = await streamReader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          res.write(chunk);
          if (typeof (res as any).flush === "function") (res as any).flush();
        }
      } finally {
        streamReader.releaseLock();
      }
    };
    await pump(reader);
    res.end();
  } catch (err: any) {
    logger.warn("[Nexus Proxy] ollama/generate failed:", err?.message || err);
    if (!res.headersSent) {
      res.status(502).json({
        error: "proxy_unavailable",
        service: "ollama/generate",
        message: err?.message || "Service unreachable",
      });
    }
  }
});

export { nerveRouter, ollamaRouter };
