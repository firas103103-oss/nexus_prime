import uvicorn
from fastapi import FastAPI
import os

app = FastAPI(title="NEXUS Voice Engine")

@app.get("/")
async def health():
    return {"status": "Voice Engine Active", "version": "1.0.0"}

@app.get("/v1/speak")
async def speak(text: str, voice: str = "ar-SA-ZariyahNeural"):
    # هنا سنضيف منطق التحويل لاحقاً، المهم الآن أن يظل السيرفر Up
    return {"message": "Voice synthesis logic ready", "text": text}

if __name__ == "__main__":
    print("🚀 NEXUS Voice Engine is starting on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
