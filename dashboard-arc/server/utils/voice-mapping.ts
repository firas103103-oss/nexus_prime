/**
 * Map ElevenLabs voice IDs to Edge-TTS (nexus_voice) voice names.
 * Used when ELEVENLABS_API_KEY is empty and we fall back to local nexus_voice.
 */
const ELEVENLABS_TO_EDGE_TTS: Record<string, string> = {
  "21m00Tcm4TlvDq8ikWAM": "nova",      // Rachel - professional
  "EXAVITQu4vr4xnSDxMaL": "nova",      // Bella - efficient
  "pNInz6obpgDQGcFmaJgB": "alloy",     // Adam - friendly
  "ErXwobaYiN019PkySvjV": "onyx",      // Antoni - analytical
  "MF3mGyEYCl7XYWbV9V6O": "shimmer",   // Elli - caring
  "N2lVS1w4EtoT3dr4eOWO": "echo",      // Callum - energetic
  "VR6AewLTigWG4xSOukaG": "onyx",      // Arnold - authoritative
  "onwK4e9ZLuTAKqWW03F9": "alloy",     // Daniel - precise
  "iP95p4xoKVk53GoZ742B": "fable",     // Chris - calm
  "pqHfZKP75CvOlQylNhV4": "alloy",     // Bill - technical
  default: "alloy",
};

export function elevenLabsVoiceIdToEdgeTTS(voiceId: string): string {
  if (!voiceId || voiceId === "default") return "alloy";
  return ELEVENLABS_TO_EDGE_TTS[voiceId] ?? ELEVENLABS_TO_EDGE_TTS.default ?? "alloy";
}
