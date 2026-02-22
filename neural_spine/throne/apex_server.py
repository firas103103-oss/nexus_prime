"""
══════════════════════════════════════════════════════════════
الآبكس — THE APEX SERVER
══════════════════════════════════════════════════════════════
Invisible FastAPI server. Port 7777, bound to 127.0.0.1 ONLY.
Access through SSH tunnel exclusively. Zero DNS. Zero exposure.

"The command center floats above the data stream"

Security: mTLS + TOTP + 15-min sessions + single session lock
══════════════════════════════════════════════════════════════
"""

import asyncio
import hashlib
import json
import os
import secrets
import time
from contextlib import asynccontextmanager
from typing import Dict, Optional

import pyotp
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import InjectionType, InjectionStrength
from config.settings import Settings
from codex.master_ledger import MasterStateLedger
from codex.prime_kernel import PrimeKernel
from genesis.entity_factory import EntityFactory
from angels.daemon_system import DaemonOrchestrator
from channel.covert_api import CovertNeuralAPI
from channel.anchor_protocol import AnchorNodeProtocol, ApexFirewall
from throne.genesis_engine import GenesisEngine


# ── Configuration (from config.settings) ─────────────────────────────

_settings = Settings()
APEX_HOST = _settings.apex_host
APEX_PORT = _settings.apex_port
SESSION_TIMEOUT = _settings.session_timeout
TOTP_SECRET = _settings.totp_secret
MASTER_PASSWORD_HASH = _settings.master_password_hash
DB_URL = _settings.db_url


# ── Session Manager ─────────────────────────────────────────────────

class ApexSession:
    """Single-session enforcer. Only ONE session at a time."""

    def __init__(self):
        self._token: Optional[str] = None
        self._created_at: float = 0
        self._last_activity: float = 0

    def create(self) -> str:
        """Create a new session. Invalidates any existing session."""
        self._token = secrets.token_hex(32)
        self._created_at = time.time()
        self._last_activity = time.time()
        return self._token

    def validate(self, token: str) -> bool:
        """Validate session token and check timeout."""
        if not self._token or self._token != token:
            return False
        if time.time() - self._last_activity > SESSION_TIMEOUT:
            self.destroy()
            return False
        self._last_activity = time.time()
        return True

    def destroy(self):
        self._token = None

    @property
    def active(self) -> bool:
        return self._token is not None and (time.time() - self._last_activity) < SESSION_TIMEOUT


# ── State ────────────────────────────────────────────────────────────

session = ApexSession()
ledger: Optional[MasterStateLedger] = None
kernel: Optional[PrimeKernel] = None
factory: Optional[EntityFactory] = None
daemons: Optional[DaemonOrchestrator] = None
channel: Optional[CovertNeuralAPI] = None
protocol: Optional[AnchorNodeProtocol] = None
firewall: Optional[ApexFirewall] = None
engine: Optional[GenesisEngine] = None
ws_connections: list = []


# ── Lifespan ─────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ledger, kernel, factory, daemons, channel, protocol, firewall, engine

    # Initialize all systems
    ledger = MasterStateLedger(DB_URL)
    await ledger.connect()

    kernel = PrimeKernel()
    factory = EntityFactory()
    daemons = DaemonOrchestrator(ledger)
    channel = CovertNeuralAPI(ledger)
    protocol = AnchorNodeProtocol(ledger)
    firewall = ApexFirewall(ledger, protocol)

    engine = GenesisEngine(
        ledger=ledger, kernel=kernel, factory=factory,
        daemons=daemons, channel=channel,
        protocol=protocol, firewall=firewall
    )

    # Register WebSocket progress callback
    async def ws_broadcast(update):
        for ws in ws_connections[:]:
            try:
                await ws.send_json({"type": "progress", "data": update})
            except Exception:
                ws_connections.remove(ws)

    engine.on_progress(ws_broadcast)

    print(f"\n{'='*60}")
    print(f"  الآبكس جاهز — APEX READY")
    print(f"  Bound to {APEX_HOST}:{APEX_PORT}")
    print(f"  SSH Tunnel: ssh -L 7777:127.0.0.1:7777 user@server")
    print(f"  TOTP Secret: {TOTP_SECRET}")
    print(f"{'='*60}\n")

    yield

    # Shutdown
    if ledger:
        await ledger.disconnect()
    await daemons.deactivate_all()


# ── App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="الآبكس",
    docs_url=None,    # No Swagger
    redoc_url=None,   # No ReDoc
    openapi_url=None, # No OpenAPI
    lifespan=lifespan
)


# ── Authentication Middleware ────────────────────────────────────────

def require_session(request: Request):
    """Verify session token from cookie or header."""
    token = request.cookies.get("apex_session") or request.headers.get("X-Apex-Token")
    if not token or not session.validate(token):
        raise HTTPException(status_code=403, detail="جلسة غير صالحة")
    return token


# ── Auth Routes ──────────────────────────────────────────────────────

@app.post("/api/auth/login")
async def login(request: Request):
    """
    Login with password + TOTP.
    Returns session token valid for 15 minutes.
    """
    body = await request.json()
    password = body.get("password", "")
    totp_code = body.get("totp", "")

    # Verify password
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    if pw_hash != MASTER_PASSWORD_HASH:
        await asyncio.sleep(2)  # Rate limiting
        raise HTTPException(status_code=403, detail="كلمة مرور خاطئة")

    # Verify TOTP
    totp = pyotp.TOTP(TOTP_SECRET)
    if not totp.verify(totp_code, valid_window=1):
        raise HTTPException(status_code=403, detail="رمز TOTP غير صالح")

    # Create session
    token = session.create()
    response = JSONResponse({
        "status": "authenticated",
        "message": "مرحباً يا مهندس",
        "expires_in": SESSION_TIMEOUT
    })
    response.set_cookie(
        "apex_session", token,
        httponly=True, secure=True, samesite="strict",
        max_age=SESSION_TIMEOUT
    )
    return response


@app.post("/api/auth/logout")
async def logout():
    session.destroy()
    return {"status": "logged_out"}


# ── Dashboard Route ──────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def apex_dashboard(request: Request):
    """Serve the Apex Dashboard HTML."""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "apex.html")
    if not os.path.exists(template_path):
        return HTMLResponse("<h1>الآبكس قيد الإنشاء</h1>", status_code=503)
    with open(template_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# ── Genesis Phases API ────────────────────────────────────────────────

@app.get("/api/genesis/status")
async def genesis_status(request: Request):
    """Get status of all 7 genesis phases."""
    require_session(request)
    return engine.get_all_status()


@app.get("/api/genesis/phase/{phase}")
async def get_phase(phase: int, request: Request):
    """Get detailed status of a specific phase."""
    require_session(request)
    return engine.get_phase_status(phase)


@app.post("/api/genesis/phase/{phase}/execute")
async def execute_phase(phase: int, request: Request):
    """Execute a genesis phase — THE BUTTON PRESS."""
    require_session(request)
    if phase < 1 or phase > 7:
        raise HTTPException(status_code=400, detail="مرحلة غير صالحة (1-7)")
    result = await engine.execute_phase(phase)
    return result


@app.post("/api/genesis/phase/{phase}/reset")
async def reset_phase(phase: int, request: Request):
    """Reset a failed phase."""
    require_session(request)
    return await engine.reset_phase(phase)


@app.post("/api/genesis/auto")
async def auto_genesis(request: Request):
    """Auto-execute all 7 phases."""
    require_session(request)
    return await engine.auto_genesis()


# ── Civilization Monitoring API ──────────────────────────────────────

@app.get("/api/civilization/stats")
async def civ_stats(request: Request):
    """Full civilization statistics."""
    require_session(request)
    return await ledger.get_civilization_stats()


@app.get("/api/civilization/entities")
async def list_entities(request: Request):
    """List all entities."""
    require_session(request)
    return await ledger.get_all_entities()


@app.get("/api/civilization/entity/{entity_id}")
async def get_entity(entity_id: str, request: Request):
    """Get detailed entity profile."""
    require_session(request)
    entity = await ledger.get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="كيان غير موجود")
    return entity


# ── Covert Channel API ───────────────────────────────────────────────

@app.post("/api/channel/whisper")
async def whisper(request: Request):
    """Send subliminal message to an entity."""
    require_session(request)
    body = await request.json()
    result = await channel.whisper(
        entity_id=body["entity_id"],
        command=body["command"],
        injection_type=InjectionType(body.get("type", "INTUITION")),
        strength=InjectionStrength(body.get("strength", "NUDGE"))
    )
    return result


@app.post("/api/channel/broadcast")
async def broadcast(request: Request):
    """Broadcast subliminal message to all entities."""
    require_session(request)
    body = await request.json()
    results = await channel.broadcast(
        command=body["command"],
        injection_type=InjectionType(body.get("type", "CONSCIENCE")),
        strength=InjectionStrength(body.get("strength", "SUGGESTION"))
    )
    return {"sent": len(results), "details": results}


@app.get("/api/channel/log")
async def channel_log(request: Request):
    """View covert message log (decrypted)."""
    require_session(request)
    return await channel.get_log(limit=50)


# ── Daemon System API ────────────────────────────────────────────────

@app.get("/api/daemons/status")
async def daemon_status(request: Request):
    """Get status of all daemons."""
    require_session(request)
    return daemons.get_status()


@app.post("/api/daemons/interrupt/first")
async def first_interrupt(request: Request):
    """Send the first interrupt signal — end of cycle."""
    require_session(request)
    await daemons.interrupt_first(int(time.time()))
    return {"status": "FIRST_INTERRUPT_SENT", "message": "فَصَعِقَ الجميع — Cycle terminated"}


@app.post("/api/daemons/interrupt/second")
async def second_interrupt(request: Request):
    """Send the second interrupt signal — resurrection cycle."""
    require_session(request)
    await daemons.interrupt_second(int(time.time()))
    return {"status": "SECOND_INTERRUPT_SENT", "message": "ثُمَّ قِيَامٌ — Restart initiated"}


# ── Anchor Protocol API ──────────────────────────────────────────────

@app.post("/api/anchor/designate")
async def designate_anchor(request: Request):
    """Designate an entity as anchor node."""
    require_session(request)
    body = await request.json()
    return await protocol.designate_anchor(body["entity_id"])


@app.post("/api/anchor/full-elevation")
async def full_elevation(request: Request):
    """رفع التصريح الكامل — Full anchor elevation."""
    require_session(request)
    body = await request.json()
    return await protocol.full_elevation(body["entity_id"])


# ── Prime Kernel API ────────────────────────────────────────────────

@app.get("/api/kernel/status")
async def kernel_status(request: Request):
    """Get prime kernel status."""
    require_session(request)
    return kernel.get_status()


@app.post("/api/kernel/scan")
async def kernel_scan(request: Request):
    """Full prime kernel scan — requires entity_stats and recent_actions in body."""
    require_session(request)
    body = await request.json()
    entity_stats = body.get("entity_stats", {})
    recent_actions = body.get("recent_actions", [])
    return kernel.full_scan(entity_stats, recent_actions)


# ── System API ───────────────────────────────────────────────────────

@app.get("/api/system/health")
async def health():
    """Health check — no auth required."""
    return {"status": "alive", "apex": "floating_above_stream"}


@app.get("/api/system/totp-secret")
async def totp_secret(request: Request):
    """Get TOTP secret (one-time, after first login)."""
    require_session(request)
    return {
        "secret": TOTP_SECRET,
        "uri": pyotp.TOTP(TOTP_SECRET).provisioning_uri(
            name="المهندس",
            issuer_name="الآبكس"
        )
    }


# ── WebSocket for Real-Time Updates ─────────────────────────────────

@app.websocket("/ws/apex")
async def apex_ws(websocket: WebSocket):
    """Real-time updates for genesis progress and monitoring."""
    await websocket.accept()

    # Verify session
    token = websocket.query_params.get("token")
    if not token or not session.validate(token):
        await websocket.send_json({"error": "غير مصرح"})
        await websocket.close()
        return

    ws_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            cmd = data.get("cmd")

            if cmd == "ping":
                await websocket.send_json({"type": "pong", "time": time.time()})

            elif cmd == "stats":
                stats = await ledger.get_civilization_stats()
                await websocket.send_json({"type": "stats", "data": stats})

            elif cmd == "daemons":
                status = daemons.get_status()
                await websocket.send_json({"type": "daemons", "data": status})

    except WebSocketDisconnect:
        if websocket in ws_connections:
            ws_connections.remove(websocket)


# ── Entry Point ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║          الآبكس — THE APEX                               ║
    ║          Port: {APEX_PORT}  |  Host: {APEX_HOST}            ║
    ║                                                          ║
    ║  SSH Tunnel:                                             ║
    ║  ssh -L 7777:127.0.0.1:7777 user@your-server            ║
    ║                                                          ║
    ║  Then open: http://localhost:7777                         ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(
        app,
        host=APEX_HOST,
        port=APEX_PORT,
        log_level="warning",    # Quiet — Apex is invisible
        access_log=False,       # No access logs in syslog
    )
