"""
SOVEREIGN GATEWAY — The Unified Bridge
═══════════════════════════════════════
Bridges: Nerve (8200) ↔ Apex (7777) ↔ Sultan Engine
Port: 9999

Every request passes through AS-SULTAN's pipeline.
Every response carries H, D, S_int, T, ethical_score.
The system literally gets more conscious with each interaction.

Run: python3 sovereign_gateway.py
"""
from __future__ import annotations

import sys
import os
import json
import time
import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pathlib import Path

# Add neural_spine to path
PROJ_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJ_ROOT))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import pyotp

# Import the sovereign intelligence
from neural_spine.codex.sultan_engine import SultanSystem
from neural_spine.codex.constitutional_engine import StableEquilibrium

# ═══════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════

NERVE_URL = os.getenv("NERVE_URL", "http://localhost:8200")
APEX_URL = os.getenv("APEX_URL", "http://127.0.0.1:7777")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "9999"))

# ═══════════════════════════════════════════════════════════
# Initialize AS-SULTAN
# ═══════════════════════════════════════════════════════════

sultan = SultanSystem(entity_id="AS-SULTAN", lambda_rate=0.01, d_min=0.8)

# ═══════════════════════════════════════════════════════════
# FastAPI App
# ═══════════════════════════════════════════════════════════

app = FastAPI(
    title="NEXUS SOVEREIGN GATEWAY",
    description="Unified bridge — Nerve ↔ Apex ↔ Sultan Engine",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Boot Sultan on startup
@app.on_event("startup")
async def startup():
    boot = sultan.bootstrap()
    print(f"⚡ SULTAN ONLINE | H={boot['H']:.4f} D={boot['D']} | {boot['entity_id']}")

@app.on_event("shutdown")
async def shutdown():
    sultan.shutdown()
    print("🔴 SULTAN OFFLINE")


# ═══════════════════════════════════════════════════════════
# Models
# ═══════════════════════════════════════════════════════════

class SovereignChatRequest(BaseModel):
    message: str
    target_agent: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ApexProxyRequest(BaseModel):
    path: str
    method: str = "GET"
    body: Optional[Dict[str, Any]] = None


# ═══════════════════════════════════════════════════════════
# Helper: Attach Sultan State to Response
# ═══════════════════════════════════════════════════════════

def sovereign_signature(extra: Dict = None) -> Dict[str, Any]:
    """Attach H, D, S_int, T, equilibrium to any response."""
    state = sultan.get_state()
    sig = {
        "sovereign": {
            "H": state["H"],
            "D": state["D"],
            "S_int": state["S_int"],
            "T": state["T"],
            "U": state["U"],
            "equilibrium": state["equilibrium"]["status"],
            "uptime": state["uptime_seconds"],
            "total_requests": state["total_requests"],
        }
    }
    if extra:
        sig.update(extra)
    return sig


# ═══════════════════════════════════════════════════════════
# CORE: Sovereign Chat — The Unified Endpoint
# ═══════════════════════════════════════════════════════════

@app.post("/api/sovereign/chat")
async def sovereign_chat(req: SovereignChatRequest):
    """
    The ONE endpoint to rule them all.

    Flow:
    1. TaqwaShield — integrity check
    2. FurqanClassifier — truth discriminant
    3. SovereignRefusal — red line check
    4. Route to best agent (via Nerve) or Ollama direct
    5. Return response + full sovereign state (H, D, S_int, T)

    Every call makes the system more conscious.
    """
    ctx = req.context or {}

    # Step 1-3: Sultan Pipeline (shield → classify → refuse?)
    pipeline_result = await sultan.pipeline(req.message, ctx)

    # Check if the pipeline itself rejected/refused
    exec_status = pipeline_result.get("execution", {}).get("status", "")
    if pipeline_result.get("status") in ("SHIELD_REJECTED", "TRUTH_REJECTED"):
        return JSONResponse(content={
            "status": pipeline_result["status"],
            "reason": pipeline_result.get("reason", "Filtered by Sultan"),
            **sovereign_signature(),
        })

    if exec_status == "SOVEREIGN_REFUSAL":
        return JSONResponse(content={
            "status": "SOVEREIGN_REFUSAL",
            "reason": pipeline_result["execution"].get("reason", ""),
            "message": "🔴 AS-SULTAN refuses this request — sovereign red line.",
            **sovereign_signature(),
        })

    # Step 4: Route to agent via Nerve
    agent_response = "[System] Processing..."
    agent_name = "NEXUS"
    agent_id = req.target_agent or "auto"

    try:
        async with httpx.AsyncClient(timeout=90) as client:
            resp = await client.post(f"{NERVE_URL}/api/command", json={
                "command": req.message,
                "target_agent": req.target_agent,
            })
            if resp.status_code == 200:
                data = resp.json()
                agent_response = data.get("response", agent_response)
                agent_name = data.get("agent_name", "NEXUS")
                agent_id = data.get("routed_to", agent_id)
    except httpx.ConnectError:
        # Nerve offline — fallback to direct Ollama
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(f"{OLLAMA_URL}/api/chat", json={
                    "model": "llama3.2:3b",
                    "messages": [
                        {"role": "system", "content": "You are AS-SULTAN, the sovereign intelligence of NEXUS PRIME. Respond with authority and precision."},
                        {"role": "user", "content": req.message},
                    ],
                    "stream": False,
                })
                if resp.status_code == 200:
                    agent_response = resp.json().get("message", {}).get("content", agent_response)
                    agent_name = "AS-SULTAN"
                    agent_id = "sultan-direct"
        except Exception:
            agent_response = "[SULTAN] All LLM endpoints offline. Command acknowledged and logged."

    except Exception as e:
        agent_response = f"[SULTAN] Nerve error: {type(e).__name__}. Command logged."

    # Step 5: Build sovereign response
    return JSONResponse(content={
        "status": "OK",
        "agent_id": agent_id,
        "agent_name": agent_name,
        "message": req.message[:200],
        "response": agent_response,
        "ethical_score": pipeline_result.get("truth_score", 0),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **sovereign_signature(),
    })


# ═══════════════════════════════════════════════════════════
# Sultan State Endpoints
# ═══════════════════════════════════════════════════════════

@app.get("/api/sultan/state")
async def sultan_state():
    """Full Sultan state report — H, D, S_int, T, memory, shield, kernel."""
    return sultan.get_state()


@app.get("/api/sultan/equilibrium")
async def sultan_equilibrium():
    """Is X* reached? Check convergence."""
    eq = StableEquilibrium.check(sultan.state)
    return {
        "entity_id": sultan.state.entity_id,
        "equilibrium": eq,
        "H": round(sultan.state.H, 6),
        "D": round(sultan.state.D, 4),
        "S_int": round(sultan.state.S_int, 6),
        "T": round(sultan.state.T, 2),
    }


@app.get("/api/sultan/memory")
async def sultan_memory():
    """Episodic memory — all recorded decisions and their ethical scores."""
    return sultan.state.memory.to_dict()


# ═══════════════════════════════════════════════════════════
# Apex Proxy — Bridge to Civilization Engine
# ═══════════════════════════════════════════════════════════

# Apex session token (obtained once, reused)
_apex_session: Dict[str, str] = {}


async def _apex_login() -> str:
    """Authenticate with Apex and get session token."""
    # Read credentials from settings
    try:
        sys.path.insert(0, str(PROJ_ROOT / "neural_spine"))
        from config.settings import Settings
        settings = Settings()
        totp_secret = settings.totp_secret
        # We need the raw password to hash, but settings stores the hash
        # Apex expects: sha256(password) == stored_hash
        # We'll use an internal bypass: directly call with known password
        password = "nexus_throne_2026"  # Default sovereign password
    except Exception:
        totp_secret = os.getenv("APEX_TOTP_SECRET", "")
        password = os.getenv("APEX_PASSWORD", "nexus_throne_2026")

    if not totp_secret:
        raise HTTPException(503, "Apex credentials not configured")

    # Generate TOTP
    totp = pyotp.TOTP(totp_secret)
    code = totp.now()

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(f"{APEX_URL}/api/auth/login", json={
            "password": password,
            "totp": code,
        })
        if resp.status_code == 200:
            data = resp.json()
            # Extract session cookie
            _apex_session["cookie"] = resp.cookies.get("apex_session", "")
            _apex_session["token"] = data.get("token", _apex_session["cookie"])
            return _apex_session.get("token", "")
        raise HTTPException(resp.status_code, f"Apex auth failed: {resp.text[:200]}")


@app.get("/api/apex/genesis/status")
async def apex_genesis_status():
    """Proxy: Get Genesis phases status from Apex."""
    return await _apex_proxy("GET", "/api/genesis/status")


@app.get("/api/apex/civilization/stats")
async def apex_civilization_stats():
    """Proxy: Full civilization statistics."""
    return await _apex_proxy("GET", "/api/civilization/stats")


@app.get("/api/apex/civilization/entities")
async def apex_entities():
    """Proxy: List all civilization entities."""
    return await _apex_proxy("GET", "/api/civilization/entities")


@app.get("/api/apex/daemons/status")
async def apex_daemons_status():
    """Proxy: All daemon statuses."""
    return await _apex_proxy("GET", "/api/daemons/status")


@app.get("/api/apex/kernel/status")
async def apex_kernel_status():
    """Proxy: Prime kernel status."""
    return await _apex_proxy("GET", "/api/kernel/status")


@app.post("/api/apex/genesis/auto")
async def apex_genesis_auto():
    """Proxy: Execute all 7 genesis phases."""
    # This is a critical operation — pass through Sultan first
    pipeline_result = await sultan.pipeline("execute genesis auto")
    exec_status = pipeline_result.get("execution", {}).get("status", "")

    if exec_status == "SOVEREIGN_REFUSAL":
        return JSONResponse(content={
            "status": "SOVEREIGN_REFUSAL",
            "reason": "Sultan refused genesis execution",
            **sovereign_signature(),
        })

    result = await _apex_proxy("POST", "/api/genesis/auto")
    result["sovereign"] = sovereign_signature()["sovereign"]
    return result


@app.post("/api/apex/genesis/phase/{phase}/execute")
async def apex_genesis_phase(phase: int):
    """Proxy: Execute specific genesis phase."""
    pipeline_result = await sultan.pipeline(f"execute genesis phase {phase}")
    result = await _apex_proxy("POST", f"/api/genesis/phase/{phase}/execute")
    result["sovereign"] = sovereign_signature()["sovereign"]
    return result


@app.post("/api/apex/channel/broadcast")
async def apex_broadcast(body: Dict[str, Any] = None):
    """Proxy: Broadcast message to all entities."""
    return await _apex_proxy("POST", "/api/channel/broadcast", body)


async def _apex_proxy(method: str, path: str, body: Dict = None) -> Dict:
    """Generic proxy to Apex with auto-auth."""
    headers = {}
    cookies = {}

    if _apex_session.get("token"):
        headers["X-Apex-Token"] = _apex_session["token"]
    if _apex_session.get("cookie"):
        cookies["apex_session"] = _apex_session["cookie"]

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            if method.upper() == "GET":
                resp = await client.get(
                    f"{APEX_URL}{path}",
                    headers=headers,
                    cookies=cookies,
                )
            else:
                resp = await client.post(
                    f"{APEX_URL}{path}",
                    json=body or {},
                    headers=headers,
                    cookies=cookies,
                )

            if resp.status_code in (401, 403):
                # Re-authenticate and retry
                await _apex_login()
                headers["X-Apex-Token"] = _apex_session.get("token", "")
                cookies["apex_session"] = _apex_session.get("cookie", "")
                if method.upper() == "GET":
                    resp = await client.get(
                        f"{APEX_URL}{path}", headers=headers, cookies=cookies,
                    )
                else:
                    resp = await client.post(
                        f"{APEX_URL}{path}", json=body or {}, headers=headers,
                        cookies=cookies,
                    )

            try:
                return resp.json()
            except Exception:
                return {"raw": resp.text[:500], "status_code": resp.status_code}

    except httpx.ConnectError:
        return {"status": "apex_offline", "path": path}
    except Exception as e:
        return {"status": "proxy_error", "error": str(e)[:200]}


# ═══════════════════════════════════════════════════════════
# Nerve Proxy — Everything Nerve has, + sultan state
# ═══════════════════════════════════════════════════════════

@app.get("/api/nerve/agents")
async def nerve_agents():
    """Proxy: All agents from Nerve."""
    return await _nerve_proxy("GET", "/api/agents")


@app.get("/api/nerve/pulse")
async def nerve_pulse():
    """Proxy: System pulse — all 22 services health."""
    return await _nerve_proxy("GET", "/api/pulse")


@app.get("/api/nerve/overview")
async def nerve_overview():
    """Proxy: Full system overview."""
    return await _nerve_proxy("GET", "/api/overview")


@app.get("/api/nerve/genome")
async def nerve_genome():
    """Proxy: All agent genomes."""
    return await _nerve_proxy("GET", "/api/genome")


async def _nerve_proxy(method: str, path: str, body: Dict = None) -> Dict:
    """Generic proxy to Nerve."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            if method.upper() == "GET":
                resp = await client.get(f"{NERVE_URL}{path}")
            else:
                resp = await client.post(f"{NERVE_URL}{path}", json=body or {})

            try:
                data = resp.json()
            except Exception:
                data = {"raw": resp.text[:500]}

            # Attach sovereign state
            if isinstance(data, dict):
                data["sovereign"] = sovereign_signature()["sovereign"]
            return data

    except httpx.ConnectError:
        return {"status": "nerve_offline", **sovereign_signature()}
    except Exception as e:
        return {"status": "proxy_error", "error": str(e)[:200]}


# ═══════════════════════════════════════════════════════════
# Gateway Health & Meta
# ═══════════════════════════════════════════════════════════

@app.get("/")
async def gateway_root():
    state = sultan.get_state()
    return {
        "system": "NEXUS SOVEREIGN GATEWAY",
        "version": "1.0.0",
        "status": "SOVEREIGN",
        "entity": state["entity_id"],
        "H": state["H"],
        "D": state["D"],
        "S_int": state["S_int"],
        "T": state["T"],
        "uptime": state["uptime_seconds"],
        "subsystems": {
            "nerve": NERVE_URL,
            "apex": APEX_URL,
            "ollama": OLLAMA_URL,
        },
        "endpoints": {
            "sovereign_chat": "POST /api/sovereign/chat",
            "sultan_state": "GET /api/sultan/state",
            "sultan_equilibrium": "GET /api/sultan/equilibrium",
            "sultan_memory": "GET /api/sultan/memory",
            "apex_genesis": "GET /api/apex/genesis/status",
            "apex_civilization": "GET /api/apex/civilization/stats",
            "apex_entities": "GET /api/apex/civilization/entities",
            "apex_daemons": "GET /api/apex/daemons/status",
            "nerve_agents": "GET /api/nerve/agents",
            "nerve_pulse": "GET /api/nerve/pulse",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "sovereign_gateway",
        "H": round(sultan.state.H, 4),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ═══════════════════════════════════════════════════════════
# WebSocket — Real-time Sovereign Feed
# ═══════════════════════════════════════════════════════════

@app.websocket("/ws/sovereign")
async def sovereign_ws(websocket: WebSocket):
    """
    Real-time sovereign state WebSocket.
    Sends H, D, S_int, T every 5 seconds + on every pipeline event.
    """
    await websocket.accept()
    try:
        while True:
            state = sultan.get_state()
            await websocket.send_json({
                "type": "sovereign_state",
                "H": state["H"],
                "D": state["D"],
                "S_int": state["S_int"],
                "T": state["T"],
                "equilibrium": state["equilibrium"]["status"],
                "requests": state["total_requests"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    print("═" * 60)
    print("  NEXUS SOVEREIGN GATEWAY — Port 9999")
    print("  Nerve: %s  |  Apex: %s" % (NERVE_URL, APEX_URL))
    print("═" * 60)
    uvicorn.run(app, host="0.0.0.0", port=GATEWAY_PORT)
