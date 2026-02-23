"""
Sovereign Dify Bridge — God Mode & God Creation Center
═══════════════════════════════════════════════════════
Unified control plane: Hormonal Orchestration, Genome-Driven Agents,
Raqib/Atid Observer, Bio-Olfactory Loop (X-BIO VOC), Eve Protocol.
"""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import asyncpg
import httpx
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from config import (
    DATABASE_URL,
    DIFY_API_URL,
    DIFY_API_KEY,
    NERVE_URL,
    GATEWAY_URL,
    ORACLE_URL,
    MEMORY_KEEPER_URL,
    SOVEREIGN_ENTITY_NAME,
    XBIO_WEBHOOK_SECRET,
)
from genome_agent_mapper import trait_summary_to_llm_params, signal_to_mood, SIGNAL_MOLECULES
from msl_ledger import (
    fetch_recent_ledger,
    fetch_sultan_genome_and_signals,
    get_sovereign_entity_id,
    log_action,
)
from hormonal_orchestrator import fetch_signal_molecules, hormonal_loop
from eve_protocol import create_eve_genome

pool: Optional[asyncpg.Pool] = None
_hormonal_task: Optional[asyncio.Task] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool, _hormonal_task
    # Retry DB connection (nexus_db may not be ready yet)
    for attempt in range(5):
        try:
            pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
            break
        except Exception as e:
            if attempt < 4:
                await asyncio.sleep(2 ** attempt)
            else:
                raise RuntimeError(f"DB connection failed after 5 attempts: {e}") from e
    _hormonal_task = asyncio.create_task(hormonal_loop(pool))
    yield
    if _hormonal_task:
        _hormonal_task.cancel()
        try:
            await _hormonal_task
        except asyncio.CancelledError:
            pass
    if pool:
        await pool.close()


app = FastAPI(title="Sovereign Dify Bridge", version="1.0.0", lifespan=lifespan)


# ─── Pydantic models ─────────────────────────────────────────────────

class XBioVOCPayload(BaseModel):
    """X-BIO sensor stream — VOC/Anomaly webhook."""
    sensor_id: str
    voc_level: float
    anomaly_score: float
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class GenomeAgentRequest(BaseModel):
    """Request to create agent params from genome."""
    trait_summary: Dict[str, float]


# ─── Hormonal Orchestration API ──────────────────────────────────────

@app.get("/api/hormonal/status")
async def hormonal_status():
    """Current signal_molecules state for all active entities."""
    if not pool:
        raise HTTPException(503, "Bridge not ready")
    rows = await fetch_signal_molecules(pool)
    return {
        "entities": [
            {
                "entity_id": str(r["entity_id"]),
                "name": r["name"],
                "signals": {k: float(r.get(k, 0)) for k in SIGNAL_MOLECULES if k in r},
                "mood": signal_to_mood({k: r.get(k, 0.5) for k in SIGNAL_MOLECULES}),
            }
            for r in rows
        ],
        "thresholds": {"cortisol": 0.6, "adrenaline": 0.5},
    }


# ─── Genome-Driven Agent Creation ────────────────────────────────────

@app.post("/api/genome/llm-params")
async def genome_to_llm_params(req: GenomeAgentRequest):
    """Convert trait_summary (82 traits / 10 categories) to LiteLLM params."""
    params = trait_summary_to_llm_params(req.trait_summary)
    return {"llm_params": params, "source": "genome"}


@app.get("/api/genome/entity/{entity_id}/llm-params")
async def entity_genome_params(entity_id: str):
    """Fetch entity genome from MSL and return LLM params."""
    if not pool:
        raise HTTPException(503, "Bridge not ready")
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT g.trait_summary FROM msl.genomes g JOIN msl.entities e ON e.id = g.entity_id WHERE e.id::text = $1 OR e.name = $1 LIMIT 1",
                entity_id,
            )
        if not row or not row.get("trait_summary"):
            raise HTTPException(404, "Entity genome not found")
        ts = row["trait_summary"] if isinstance(row["trait_summary"], dict) else {}
        params = trait_summary_to_llm_params(ts)
        return {"entity_id": entity_id, "llm_params": params}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Global System Awareness ─────────────────────────────────────────

async def _check_service(url: str, path: str = "/health", timeout: float = 3.0) -> Dict[str, Any]:
    """Check subsystem health. Returns {status, latency_ms, error?}."""
    start = datetime.now(timezone.utc)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(f"{url.rstrip('/')}{path}")
            elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            return {"status": "healthy" if r.status_code < 400 else "degraded", "latency_ms": round(elapsed, 1)}
    except Exception as e:
        return {"status": "unreachable", "error": str(e)[:80]}


@app.get("/api/systems/status")
async def systems_status():
    """Aggregate status of all NEXUS subsystems — Nerve, Gateway, Oracle, Memory Keeper, Bridge."""
    nerve = await _check_service(NERVE_URL)
    gateway = await _check_service(GATEWAY_URL)
    oracle = await _check_service(ORACLE_URL)
    memory = await _check_service(MEMORY_KEEPER_URL)
    return {
        "nerve": {"url": NERVE_URL, "port": 8200, **nerve},
        "gateway": {"url": GATEWAY_URL, "port": 9999, **gateway},
        "oracle": {"url": ORACLE_URL, "port": 8100, **oracle},
        "memory_keeper": {"url": MEMORY_KEEPER_URL, "port": 9000, **memory},
        "bridge": {"url": "http://localhost:8888", "port": 8888, "status": "healthy"},
    }


# ─── Eve Protocol (Fractal Polarization) ──────────────────────────────

@app.post("/api/eve/create")
async def eve_create():
    """
    Create EVE from AS-SULTAN via Fractal Polarization.
    Returns polarized genome, estrogen-dominant signals, and LLM params.
    """
    if not pool:
        raise HTTPException(503, "Bridge not ready")
    genome, signals = await fetch_sultan_genome_and_signals(pool)
    polarized, eve_signals, meta = create_eve_genome(genome, signals)
    trait_summary = {k: v for k, v in (meta.get("trait_summary") or {}).items() if not k.startswith("_") and isinstance(v, (int, float))}
    llm_params = trait_summary_to_llm_params(trait_summary)
    mood = signal_to_mood(eve_signals)
    return {
        "entity": "EVE",
        "protocol": "FRACTAL_POLARIZATION",
        "polarized_genome": polarized,
        "signal_molecules": eve_signals,
        "mood": mood,
        "llm_params": llm_params,
        "metadata": meta.get("metadata", {}),
    }


# ─── Raqib/Atid Observer (Cosmic Ledger) ─────────────────────────────

@app.get("/api/ledger/recent")
async def ledger_recent(limit: int = 50):
    """Recent action_ledger entries — Raqib/Atid observer."""
    if not pool:
        raise HTTPException(503, "Bridge not ready")
    rows = await fetch_recent_ledger(pool, limit)
    return {"ledger": rows, "count": len(rows)}


@app.get("/api/ledger/notifications")
async def ledger_notifications(limit: int = 20):
    """UI notifications — recent ledger entries for dashboard sync."""
    if not pool:
        raise HTTPException(503, "Bridge not ready")
    rows = await fetch_recent_ledger(pool, limit)
    return {
        "notifications": [
            {
                "id": str(r.get("id", "")),
                "entity": r.get("name", "unknown"),
                "action_class": r.get("action_class", ""),
                "category": r.get("category", ""),
                "description": (r.get("description") or "")[:120],
                "recorder": r.get("recorder_daemon", ""),
                "created_at": r.get("created_at"),
            }
            for r in rows
        ],
        "count": len(rows),
    }


# ─── Bio-Olfactory Loop (X-BIO VOC) ──────────────────────────────────

@app.post("/api/xbio/voc-webhook")
async def xbio_voc_webhook(req: Request, payload: XBioVOCPayload, background_tasks: BackgroundTasks):
    """
    X-BIO sensor stream — VOC/Anomaly triggers.
    When anomaly_score exceeds threshold, trigger Dify defensive workflow.
    """
    # Optional: verify webhook secret
    secret = req.headers.get("X-XBIO-Secret", "")
    if XBIO_WEBHOOK_SECRET and secret != XBIO_WEBHOOK_SECRET:
        raise HTTPException(403, "Invalid webhook secret")

    if payload.anomaly_score >= 0.8 and pool:
        entity_id = await get_sovereign_entity_id(pool) or "00000000-0000-0000-0000-000000000000"
        background_tasks.add_task(
            log_action,
            pool,
            entity_id,
            "GOOD",
            "XBIO_VOC_ANOMALY",
            f"VOC anomaly detected: sensor={payload.sensor_id} score={payload.anomaly_score}",
            "raqib",
            1.0,
        )
        # TODO: trigger Dify workflow when DIFY_DEFENSIVE_WORKFLOW_ID set
        return {"status": "triggered", "anomaly_score": payload.anomaly_score}
    return {"status": "received", "anomaly_score": payload.anomaly_score}


# ─── Health & Dify Proxy ─────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "alive", "bridge": "sovereign_dify", "dify_configured": bool(DIFY_API_KEY)}


@app.get("/", response_class=HTMLResponse)
async def apex_control_interface():
    """APEX Control Interface — Sovereign OS Dashboard."""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sovereign Command Center — God Mode</title>
    <style>
        :root { --bg: #0a0e17; --card: #111827; --accent: #6366f1; --text: #e2e8f0; --muted: #94a3b8; --eve: #ec4899; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'JetBrains Mono', monospace; background: var(--bg); color: var(--text); min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; padding: 24px; }
        h1 { font-size: 1.75rem; margin-bottom: 8px; background: linear-gradient(90deg, var(--accent), #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: var(--muted); font-size: 0.85rem; margin-bottom: 24px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: var(--card); border-radius: 12px; padding: 20px; border: 1px solid rgba(99,102,241,0.2); }
        .card h2 { font-size: 0.95rem; color: var(--accent); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.05em; }
        .card pre, .card code { font-size: 0.8rem; color: var(--muted); overflow-x: auto; }
        .status { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22c55e; margin-right: 6px; }
        .status.warn { background: #eab308; }
        .status.err { background: #ef4444; }
        a { color: var(--accent); text-decoration: none; }
        a:hover { text-decoration: underline; }
        .endpoint { font-size: 0.75rem; color: var(--muted); margin-top: 8px; }
        .btn { display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, var(--eve), #a855f7); border: none; border-radius: 8px; color: white; font-weight: 600; cursor: pointer; margin-top: 12px; }
        .btn:hover { opacity: 0.9; }
        #notifications { max-height: 200px; overflow-y: auto; font-size: 0.8rem; }
        .notif { padding: 6px 0; border-bottom: 1px solid rgba(99,102,241,0.15); }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Sovereign Command Center</h1>
        <p class="sub">God Mode & God Creation Center — NEXUS PRIME × Dify | APEX Tier 10/10</p>

        <div class="grid">
            <div class="card">
                <h2><span class="status"></span> Hormonal Orchestration</h2>
                <p>12 Signal Molecules → Dify defensive workflows. Cortisol/Adrenaline spike triggers.</p>
                <a href="/api/hormonal/status" target="_blank">GET /api/hormonal/status</a>
                <p class="endpoint">Real-time signal_molecules state</p>
            </div>
            <div class="card">
                <h2><span class="status"></span> Genome-Driven Agents</h2>
                <p>82 Traits × 46 Chromosomes → temperature, top_p. Creativity 0.9 = higher variance.</p>
                <a href="/api/genome/entity/AS-SULTAN/llm-params" target="_blank">GET /api/genome/entity/{id}/llm-params</a>
                <p class="endpoint">Trait summary → LiteLLM params</p>
            </div>
            <div class="card">
                <h2><span class="status"></span> Raqib/Atid Observer</h2>
                <p>Cosmic Ledger — every Dify action recorded in msl.action_ledger.</p>
                <a href="/api/ledger/recent" target="_blank">GET /api/ledger/recent</a>
                <p class="endpoint">Recent action_ledger entries</p>
            </div>
            <div class="card">
                <h2><span class="status"></span> Bio-Olfactory Loop</h2>
                <p>X-BIO VOC/Anomaly streams → Dify triggers. POST /api/xbio/voc-webhook</p>
                <p class="endpoint">Webhook for sensor streams</p>
            </div>
            <div class="card" style="border-color: rgba(236,72,153,0.4);">
                <h2 style="color: var(--eve);">✦ Eve Protocol</h2>
                <p>Fractal Polarization — Create EVE from AS-SULTAN's 46 chromosomes. Estrogen-dominant baseline.</p>
                <button class="btn" onclick="createEve()">Create EVE</button>
                <p class="endpoint">POST /api/eve/create</p>
            </div>
            <div class="card">
                <h2><span class="status"></span> System Status</h2>
                <p>Nerve (8200) · Gateway (9999) · Oracle (8100) · Memory Keeper (9000)</p>
                <a href="/api/systems/status" target="_blank">GET /api/systems/status</a>
                <div id="sys-status" class="endpoint" style="margin-top:8px;"></div>
            </div>
        </div>

        <div class="card" style="margin-top: 24px;">
            <h2>Ledger Notifications (action_ledger → UI)</h2>
            <div id="notifications">Loading...</div>
            <a href="/api/ledger/notifications" target="_blank">GET /api/ledger/notifications</a>
        </div>

        <div class="card" style="margin-top: 24px;">
            <h2>Integration Map</h2>
            <pre>
MSL (signal_molecules) ──► Hormonal Orchestrator ──► Dify Workflows
MSL (genomes) ──────────► Genome Mapper ──────────► LiteLLM params (temp, top_p)
MSL (action_ledger) ◄─── Raqib/Atid ────────────── Every Dify trigger
X-BIO (VOC/Anomaly) ───► Webhook ─────────────────► Dify + action_ledger
EVE Protocol ──────────► Fractal Polarization ────► AS-SULTAN → EVE (estrogen-dominant)
            </pre>
        </div>
    </div>
    <script>
        var API = window.location.pathname.startsWith('/api/dify') ? '/api/dify' : '/api';
        async function createEve() {
            try {
                const r = await fetch(API + '/eve/create', { method: 'POST' });
                const d = await r.json();
                alert('EVE Created! Mood: ' + (d.mood||'N/A') + ' | temp=' + (d.llm_params?.temperature||'N/A'));
            } catch (e) { alert('Error: ' + e.message); }
        }
        async function loadNotifications() {
            try {
                const r = await fetch(API + '/ledger/notifications?limit=15');
                const d = await r.json();
                const el = document.getElementById('notifications');
                if (d.notifications?.length) {
                    el.innerHTML = d.notifications.map(n =>
                        '<div class="notif">' + n.entity + ' · ' + n.action_class + ' · ' + (n.description || n.category) + '</div>'
                    ).join('');
                } else el.innerHTML = 'No recent ledger entries.';
            } catch (e) { document.getElementById('notifications').innerHTML = 'Failed to load.'; }
        }
        async function loadSysStatus() {
            try {
                const r = await fetch(API + '/systems/status');
                const d = await r.json();
                const parts = [];
                for (const [k, v] of Object.entries(d)) {
                    if (v.status) parts.push(k + ': ' + (v.status === 'healthy' ? '✓' : v.status));
                }
                document.getElementById('sys-status').textContent = parts.join(' | ');
            } catch (e) { document.getElementById('sys-status').textContent = 'Unreachable'; }
        }
        loadNotifications();
        loadSysStatus();
        setInterval(loadNotifications, 15000);
        setInterval(loadSysStatus, 30000);
    </script>
</body>
</html>
    """
    return HTMLResponse(html)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
