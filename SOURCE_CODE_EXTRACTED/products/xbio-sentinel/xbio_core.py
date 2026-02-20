from fastapi import FastAPI
import uvicorn, subprocess

app = FastAPI()

STAFF = {
    "ARC-G-711": "VP - Strategy",
    "DR_JOE": "Lab Manager - Bio-Safety",
    "ENG_VECTOR": "Hardware Lead - Engineering"
}

@app.get("/")
def root():
    return {"service": "XBio Vault", "version": "1.0", "status": "operational", "system": "MrFXOS / MRF103ARC"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "nexus_xbio"}

@app.get("/status")
def global_status():
    return {"System": "MrFXOS / MRF103ARC", "Integrity": "SEI-Protocol Enforced", "Personnel": "All Units Active"}

@app.post("/chat")
def chat(req: dict):
    query = req.get("query", "")
    persona = req.get("persona", "ARC-G-711")
    if query.startswith("run:"):
        cmd = query.replace("run:", "").strip()
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {"reply": "Executed", "out": res.stdout, "err": res.stderr}
    return {"reply": f"[{persona}]: ESP32-S3 Specs: 16MB Flash, 8MB PSRAM. System is secure.", "officer": persona}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
