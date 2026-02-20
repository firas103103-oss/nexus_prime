from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Software Ready", "mode": "Non-Defense", "owner": "Mr. Firas"}

@app.get("/system/info")
def info():
    # عرض معلومات النظام كما وردت في وثائق الأرشفة
    return {
        "IDE": "Visual Studio Code + PlatformIO",
        "Framework": "Arduino Framework (C++)",
        "Core": "ESP32-S3 (16MB Flash / 8MB PSRAM)"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
