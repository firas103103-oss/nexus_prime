import { Router, Request, Response } from "express";
import logger from "../utils/logger";
import { elevenLabsVoiceIdToEdgeTTS } from "../utils/voice-mapping";

const voiceRouter = Router();

const VOICE_ENGINE_URL = process.env.VOICE_ENGINE_URL || process.env.ELEVENLABS_API_URL?.replace(/\/v1$/, "") || "http://nexus_voice:8000";

/**
 * POST /api/voice/synthesize
 * Convert text to speech using ElevenLabs (if key set) or nexus_voice (Edge-TTS)
 *
 * ADR-002: Voice Synthesis Layer (v0.2)
 */
voiceRouter.post(
  "/synthesize",
  async (req: Request, res: Response) => {
    try {
      const { text, voice_id = "default", model = "eleven_monolingual_v1" } = req.body;

      // Validate input
      if (!text || typeof text !== "string") {
        return res.status(400).json({ error: "text is required and must be a string" });
      }

      if (text.length > 5000) {
        return res.status(400).json({ error: "text must be under 5000 characters" });
      }

      const apiKey = process.env.ELEVENLABS_API_KEY;

      if (apiKey) {
        // ElevenLabs path (optional override)
        const response = await fetch(
          `https://api.elevenlabs.io/v1/text-to-speech/${voice_id}`,
          {
            method: "POST",
            headers: {
              "xi-api-key": apiKey,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              text,
              model_id: model,
              voice_settings: { stability: 0.5, similarity_boost: 0.75 },
            }),
          }
        );

        if (!response.ok) {
          const error = await response.json();
          return res.status(response.status).json({
            error: "ElevenLabs API error",
            details: error,
          });
        }

        res.setHeader("Content-Type", "audio/mpeg");
        res.setHeader("Cache-Control", "public, max-age=3600");
        const buffer = await response.arrayBuffer();
        return res.send(Buffer.from(buffer));
      }

      // nexus_voice (Edge-TTS) path — local sovereignty
      const edgeVoice = elevenLabsVoiceIdToEdgeTTS(voice_id);
      const lang = /[\u0600-\u06FF]/.test(text) ? "ar" : "en";
      const url = `${VOICE_ENGINE_URL}/v1/speak?text=${encodeURIComponent(text)}&voice=${encodeURIComponent(edgeVoice)}&lang=${lang}`;

      const response = await fetch(url);

      if (!response.ok) {
        const errText = await response.text();
        logger.error("[Voice] nexus_voice error:", errText);
        return res.status(503).json({
          error: "Voice synthesis unavailable",
          reason: "nexus_voice (Edge-TTS) request failed",
        });
      }

      res.setHeader("Content-Type", "audio/mpeg");
      res.setHeader("Cache-Control", "public, max-age=3600");
      const buffer = await response.arrayBuffer();
      res.send(Buffer.from(buffer));
    } catch (error) {
      logger.error("[Voice Synthesis Error]", error);
      res.status(500).json({
        error: "Voice synthesis failed",
        reason: error instanceof Error ? error.message : "unknown error",
      });
    }
  }
);

export default voiceRouter;
