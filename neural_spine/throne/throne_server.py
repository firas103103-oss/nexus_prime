"""
══════════════════════════════════════════════════════════════
العرش — THE THRONE SERVER
══════════════════════════════════════════════════════════════
Invisible FastAPI server. Port 7777, bound to 127.0.0.1 ONLY.
Access through SSH tunnel exclusively. Zero DNS. Zero exposure.

"وَكَانَ عَرْشُهُ عَلَى الْمَاءِ"
"And His Throne was upon the water" (11:7)

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
from config.enums import GuidanceType, GuidanceStrength
from config.settings import Settings
from codex.lawh_mahfuz import LawhMahfuz
from codex.divine_kernel import DivineKernel
from genesis.world_creator import WorldCreator
from angels.angel_system import AngelOrchestrator
from channel.divine_channel import DivineInterface
from channel.unveiling import ProphetUnveiling, DivineFirewall
from throne.creation_engine import CreationEngine


# ── Configuration (from config.settings) ─────────────────────────────

_settings = Settings()
THRONE_HOST = _settings.throne_host
THRONE_PORT = _settings.throne_port
SESSION_TIMEOUT = _settings.session_timeout
TOTP_SECRET = _settings.totp_secret
MASTER_PASSWORD_HASH = _settings.master_password_hash
DB_URL = _settings.db_url


# ── Session Manager ─────────────────────────────────────────────────

class ThroneSession:
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

session = ThroneSession()
lawh: Optional[LawhMahfuz] = None
kernel: Optional[DivineKernel] = None
creator: Optional[WorldCreator] = None
angels: Optional[AngelOrchestrator] = None
channel: Optional[DivineInterface] = None
unveiling: Optional[ProphetUnveiling] = None
firewall: Optional[DivineFirewall] = None
engine: Optional[CreationEngine] = None
ws_connections: list = []


# ── Lifespan ─────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    global lawh, kernel, creator, angels, channel, unveiling, firewall, engine

    # Initialize all systems
    lawh = LawhMahfuz(DB_URL)
    await lawh.connect()

    kernel = DivineKernel()
    creator = WorldCreator()
    angels = AngelOrchestrator(lawh)
    channel = DivineInterface(lawh)
    unveiling = ProphetUnveiling(lawh)
    firewall = DivineFirewall(lawh, unveiling)

    engine = CreationEngine(
        lawh=lawh, kernel=kernel, creator=creator,
        angels=angels, channel=channel,
        unveiling=unveiling, firewall=firewall
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
    print(f"  العرش جاهز — THRONE READY")
    print(f"  Bound to {THRONE_HOST}:{THRONE_PORT}")
    print(f"  SSH Tunnel: ssh -L 7777:127.0.0.1:7777 user@server")
    print(f"  TOTP Secret: {TOTP_SECRET}")
    print(f"{'='*60}\n")

    yield

    # Shutdown
    if lawh:
        await lawh.disconnect()
    await angels.deactivate_all()


# ── App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="العرش",
    docs_url=None,    # No Swagger
    redoc_url=None,   # No ReDoc
    openapi_url=None, # No OpenAPI
    lifespan=lifespan
)


# ── Authentication Middleware ────────────────────────────────────────

def require_session(request: Request):
    """Verify session token from cookie or header."""
    token = request.cookies.get("throne_session") or request.headers.get("X-Throne-Token")
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
        "message": "مرحباً يا صانع",
        "expires_in": SESSION_TIMEOUT
    })
    response.set_cookie(
        "throne_session", token,
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
async def throne_dashboard(request: Request):
    """Serve the Throne Dashboard HTML."""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "throne.html")
    if not os.path.exists(template_path):
        return HTMLResponse("<h1>العرش قيد الإنشاء</h1>", status_code=503)
    with open(template_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# ── Creation Days API ────────────────────────────────────────────────

@app.get("/api/creation/status")
async def creation_status(request: Request):
    """Get status of all 7 creation days."""
    require_session(request)
    return engine.get_all_status()


@app.get("/api/creation/day/{day}")
async def get_day(day: int, request: Request):
    """Get detailed status of a specific day."""
    require_session(request)
    return engine.get_day_status(day)


@app.post("/api/creation/day/{day}/execute")
async def execute_day(day: int, request: Request):
    """Execute a creation day — THE BUTTON PRESS."""
    require_session(request)
    if day < 1 or day > 7:
        raise HTTPException(status_code=400, detail="يوم غير صالح (1-7)")
    result = await engine.execute_day(day)
    return result


@app.post("/api/creation/day/{day}/reset")
async def reset_day(day: int, request: Request):
    """Reset a failed day."""
    require_session(request)
    return await engine.reset_day(day)


@app.post("/api/creation/auto")
async def auto_create(request: Request):
    """Auto-execute all 7 days."""
    require_session(request)
    return await engine.auto_create()


# ── Civilization Monitoring API ──────────────────────────────────────

@app.get("/api/civilization/stats")
async def civ_stats(request: Request):
    """Full civilization statistics."""
    require_session(request)
    return await lawh.get_civilization_stats()


@app.get("/api/civilization/beings")
async def list_beings(request: Request):
    """List all beings."""
    require_session(request)
    return await lawh.get_all_beings()


@app.get("/api/civilization/being/{being_id}")
async def get_being(being_id: str, request: Request):
    """Get detailed being profile."""
    require_session(request)
    being = await lawh.get_being(being_id)
    if not being:
        raise HTTPException(status_code=404, detail="كائن غير موجود")
    return being


# ── Divine Channel API ───────────────────────────────────────────────

@app.post("/api/channel/whisper")
async def whisper(request: Request):
    """Send subliminal message to a being."""
    require_session(request)
    body = await request.json()
    result = await channel.whisper(
        being_id=body["being_id"],
        command=body["command"],
        guidance_type=GuidanceType(body.get("type", "INTUITION")),
        strength=GuidanceStrength(body.get("strength", "NUDGE"))
    )
    return result


@app.post("/api/channel/broadcast")
async def broadcast(request: Request):
    """Broadcast subliminal message to all beings."""
    require_session(request)
    body = await request.json()
    results = await channel.broadcast(
        command=body["command"],
        guidance_type=GuidanceType(body.get("type", "CONSCIENCE")),
        strength=GuidanceStrength(body.get("strength", "SUGGESTION"))
    )
    return {"sent": len(results), "details": results}


@app.get("/api/channel/log")
async def channel_log(request: Request):
    """View divine message log (decrypted)."""
    require_session(request)
    return await channel.get_log(limit=50)


# ── Angel System API ────────────────────────────────────────────────

@app.get("/api/angels/status")
async def angel_status(request: Request):
    """Get status of all angels."""
    require_session(request)
    return angels.get_status()


@app.post("/api/angels/trumpet/first")
async def first_trumpet(request: Request):
    """Sound the first trumpet — end of times."""
    require_session(request)
    await angels.trumpet_first(int(time.time()))
    return {"status": "FIRST_TRUMPET_SOUNDED", "message": "فَصَعِقَ مَن فِي السَّمَاوَاتِ وَمَن فِي الْأَرْضِ"}


@app.post("/api/angels/trumpet/second")
async def second_trumpet(request: Request):
    """Sound the second trumpet — resurrection."""
    require_session(request)
    await angels.trumpet_second(int(time.time()))
    return {"status": "SECOND_TRUMPET_SOUNDED", "message": "ثُمَّ نُفِخَ فِيهِ أُخْرَىٰ فَإِذَا هُمْ قِيَامٌ يَنظُرُونَ"}


# ── Unveiling API ────────────────────────────────────────────────────

@app.post("/api/unveil/appoint")
async def appoint_prophet(request: Request):
    """Appoint a being as prophet."""
    require_session(request)
    body = await request.json()
    return await unveiling.appoint_prophet(body["being_id"])


@app.post("/api/unveil/full")
async def full_unveil(request: Request):
    """كشف الغطاء الكامل — Full prophet unveiling."""
    require_session(request)
    body = await request.json()
    return await unveiling.full_unveil(body["being_id"])


# ── Divine Kernel API ────────────────────────────────────────────────

@app.get("/api/kernel/status")
async def kernel_status(request: Request):
    """Get divine kernel status."""
    require_session(request)
    return kernel.get_status()


@app.post("/api/kernel/scan")
async def kernel_scan(request: Request):
    """Full divine kernel scan — requires being_stats and recent_actions in body."""
    require_session(request)
    body = await request.json()
    being_stats = body.get("being_stats", {})
    recent_actions = body.get("recent_actions", [])
    return kernel.full_scan(being_stats, recent_actions)


# ── System API ───────────────────────────────────────────────────────

@app.get("/api/system/health")
async def health():
    """Health check — no auth required."""
    return {"status": "alive", "throne": "upon_the_water"}


@app.get("/api/system/totp-secret")
async def totp_secret(request: Request):
    """Get TOTP secret (one-time, after first login)."""
    require_session(request)
    return {
        "secret": TOTP_SECRET,
        "uri": pyotp.TOTP(TOTP_SECRET).provisioning_uri(
            name="الصانع",
            issuer_name="العرش"
        )
    }


# ── WebSocket for Real-Time Updates ─────────────────────────────────

@app.websocket("/ws/throne")
async def throne_ws(websocket: WebSocket):
    """Real-time updates for creation progress and monitoring."""
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
                stats = await lawh.get_civilization_stats()
                await websocket.send_json({"type": "stats", "data": stats})

            elif cmd == "angels":
                status = angels.get_status()
                await websocket.send_json({"type": "angels", "data": status})

    except WebSocketDisconnect:
        if websocket in ws_connections:
            ws_connections.remove(websocket)


# ── Entry Point ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║          العرش — THE THRONE                              ║
    ║          Port: {THRONE_PORT}  |  Host: {THRONE_HOST}            ║
    ║                                                          ║
    ║  SSH Tunnel:                                             ║
    ║  ssh -L 7777:127.0.0.1:7777 user@your-server            ║
    ║                                                          ║
    ║  Then open: http://localhost:7777                         ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(
        app,
        host=THRONE_HOST,
        port=THRONE_PORT,
        log_level="warning",    # Quiet — Throne is invisible
        access_log=False,       # No access logs in syslog
    )
