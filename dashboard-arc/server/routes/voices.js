/* eslint-disable no-undef */
import express from "express";

const router = express.Router();

const VOICE_ENGINE_URL = process.env.VOICE_ENGINE_URL || process.env.ELEVENLABS_API_URL?.replace(/\/v1$/, "") || "http://nexus_voice:8000";

const EDGE_TTS_VOICES = [
  { voice_id: "alloy", name: "Alloy", category: "premade" },
  { voice_id: "echo", name: "Echo", category: "premade" },
  { voice_id: "fable", name: "Fable", category: "premade" },
  { voice_id: "onyx", name: "Onyx", category: "premade" },
  { voice_id: "nova", name: "Nova", category: "premade" },
  { voice_id: "shimmer", name: "Shimmer", category: "premade" },
  { voice_id: "ar-male", name: "Arabic Male", category: "premade" },
  { voice_id: "ar-female", name: "Arabic Female", category: "premade" },
];

router.get("/api/arc/voices", async (_req, res) => {
  try {
    const ELEVEN_KEY = process.env.ELEVENLABS_API_KEY;

    if (ELEVEN_KEY) {
      const response = await fetch("https://api.elevenlabs.io/v1/voices", {
        headers: { "xi-api-key": ELEVEN_KEY },
      });
      const data = await response.json();
      const voices = (data.voices || []).map((v) => ({
        voice_id: v.voice_id,
        name: v.name,
        category: v.category || "premade",
      }));
      return res.json({ voices });
    }

    // nexus_voice (Edge-TTS) fallback
    try {
      const response = await fetch(`${VOICE_ENGINE_URL}/v1/voices`);
      const data = await response.json();
      const voices = (data.voices || []).map((id) => {
        const known = EDGE_TTS_VOICES.find((v) => v.voice_id === id);
        return known || { voice_id: id, name: id, category: "premade" };
      });
      return res.json({ voices: voices.length ? voices : EDGE_TTS_VOICES });
    } catch (e) {
      return res.json({ voices: EDGE_TTS_VOICES });
    }
  } catch (err) {
    console.error("Voice list error:", err);
    res.status(500).json({ error: "Failed to fetch voices" });
  }
});

export default router;