import uvicorn
import edge_tts
import io
import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI(title="NEXUS Voice Engine")

# Map OpenAI-style voice names to Edge-TTS voices
VOICE_MAP = {
    # English voices
    "alloy": "en-US-GuyNeural",
    "echo": "en-US-EricNeural",
    "fable": "en-GB-RyanNeural",
    "onyx": "en-US-ChristopherNeural",
    "nova": "en-US-JennyNeural",
    "shimmer": "en-US-AriaNeural",
    # Arabic voices
    "ar-male": "ar-SA-HamedNeural",
    "ar-female": "ar-SA-ZariyahNeural",
}

@app.get("/")
async def health():
    return {"status": "Voice Engine Active", "version": "2.0.0", "engine": "edge-tts"}

@app.get("/v1/voices")
async def list_voices():
    return {"voices": list(VOICE_MAP.keys())}

@app.get("/v1/speak")
async def speak(
    text: str = Query(..., description="Text to synthesize"),
    voice: str = Query("alloy", description="Voice name"),
    lang: str = Query("en", description="Language code")
):
    """Synthesize speech using Edge-TTS"""
    # Resolve voice name
    if lang == "ar":
        tts_voice = VOICE_MAP.get(voice, "ar-SA-HamedNeural")
        if voice in VOICE_MAP and not VOICE_MAP[voice].startswith("ar-"):
            tts_voice = "ar-SA-HamedNeural"
    else:
        tts_voice = VOICE_MAP.get(voice, "en-US-GuyNeural")
    
    try:
        communicate = edge_tts.Communicate(text, tts_voice)
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        audio_buffer.seek(0)
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"}
        )
    except Exception as e:
        return {"error": str(e), "voice": tts_voice}

if __name__ == "__main__":
    print("🚀 NEXUS Voice Engine v2.0 starting on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
