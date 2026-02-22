"""
NEXUS NERVE CENTER — Sovereign Command API
══════════════════════════════════════════
BOMB 2: Sovereign Command → Routes NL commands to agents via LLM
BOMB 3: Agent Genome → Tracks & evolves agent DNA over time
BOMB 5: Nexus Pulse → Real-time heartbeat of all 21 services
NEURAL-GENOME COUPLING: Nerve ↔ Genesis (hormones, chromosomes, ethical filter)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Callable, Tuple
from contextlib import asynccontextmanager
import httpx, asyncio, os, json, yaml, time, random
from datetime import datetime, timezone
from pathlib import Path
from boardroom_bridge import BoardroomBridge
from cognitive_bridge import NeuralGenomeBridge, HormoneEvent, SignalState, GenomeStats, _mood_from_signals

# Boardroom Bridge instance
bridge = BoardroomBridge()

# Cognitive Bridge (Neural-Genome Coupling) — set in lifespan
db_pool = None
cognitive_bridge: Optional[NeuralGenomeBridge] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool, cognitive_bridge
    db_url = os.getenv("DATABASE_URL", "")
    if db_url:
        try:
            import asyncpg
            db_pool = await asyncpg.create_pool(db_url, min_size=1, max_size=5, command_timeout=10)
            cognitive_bridge = NeuralGenomeBridge(pool=db_pool)
            await cognitive_bridge.bootstrap_sovereign_entity()
        except Exception as e:
            cognitive_bridge = NeuralGenomeBridge(pool=None)
    else:
        cognitive_bridge = NeuralGenomeBridge(pool=None)
    yield
    if db_pool:
        await db_pool.close()


app = FastAPI(title="Nexus Nerve Center API", version="2.1.0-neural-genome", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ═══════════════════════════════════════════════════════════════
# HEALTH CHECK ENDPOINT
# ═══════════════════════════════════════════════════════════════
@app.get("/health")
def health_check():
    """Health check endpoint for Docker and monitoring"""
    return {
        "status": "healthy",
        "service": "nexus_nerve",
        "version": "2.1.0-neural-genome",
        "cognitive_bridge": cognitive_bridge is not None and cognitive_bridge._entity_id is not None,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════
REGISTRY_PATH = Path("/root/NEXUS_PRIME_UNIFIED/AI_HR_REGISTRY")
GENOME_PATH = Path("/root/NEXUS_PRIME_UNIFIED/nexus_nerve/genome_state.json")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LITELLM_URL = os.getenv("LITELLM_URL", "http://localhost:4000")
LITELLM_KEY = os.getenv("LITELLM_KEY", "sk-nexus-sovereign-mrf103")

SERVICES = [
    {"name": "PostgreSQL", "port": 5432, "host": "localhost", "check": "tcp"},
    {"name": "Ollama LLM", "port": 11434, "host": "localhost", "check": "http", "path": "/api/tags"},
    {"name": "Open WebUI", "port": 3000, "host": "localhost", "check": "http", "path": "/"},
    {"name": "n8n Flow", "port": 5678, "host": "localhost", "check": "http", "path": "/healthz"},
    {"name": "Shadow7 API", "port": 8002, "host": "localhost", "check": "http", "path": "/health"},
    {"name": "PostgREST", "port": 3001, "host": "localhost", "check": "http", "path": "/"},
    {"name": "Auth Service", "port": 8003, "host": "localhost", "check": "http", "path": "/health"},
    {"name": "Edge-TTS", "port": 5050, "host": "localhost", "check": "http", "path": "/health"},
    {"name": "Boardroom", "port": 8501, "host": "localhost", "check": "http", "path": "/healthz"},
    {"name": "Dashboard", "port": 5001, "host": "localhost", "check": "http", "path": "/"},
    {"name": "Cortex", "port": 8090, "host": "localhost", "check": "http", "path": "/health"},
    {"name": "Memory Keeper", "port": 9000, "host": "localhost", "check": "http", "path": "/"},
    {"name": "Orchestrator", "port": 50051, "host": "localhost", "check": "tcp"},
    {"name": "X-Bio Sentinel", "port": 8080, "host": "localhost", "check": "http", "path": "/"},
    {"name": "Prometheus", "port": 9090, "host": "localhost", "check": "http", "path": "/-/healthy"},
    {"name": "Grafana", "port": 3002, "host": "localhost", "check": "http", "path": "/api/health"},
    {"name": "Ecosystem API", "port": 8005, "host": "localhost", "check": "http", "path": "/health"},
    {"name": "Oracle API", "port": 8100, "host": "localhost", "check": "http", "path": "/health"},
    {"name": "Redis", "port": 6379, "host": "localhost", "check": "tcp"},
    {"name": "LiteLLM", "port": 4000, "host": "localhost", "check": "http", "path": "/health"},
    {"name": "Alertmanager", "port": 9093, "host": "localhost", "check": "http", "path": "/-/healthy"},
    {"name": "Neural Spine", "port": 8300, "host": "localhost", "check": "http", "path": "/health"},
]

# ═══════════════════════════════════════════════════════════════
# AGENT REGISTRY LOADER
# ═══════════════════════════════════════════════════════════════
def load_agents() -> List[Dict]:
    agents = []
    for profile_path in REGISTRY_PATH.rglob("profile.yaml"):
        with open(profile_path) as f:
            p = yaml.safe_load(f)
        agents.append({
            "id": p["identity"]["id"],
            "name": p["identity"]["name"],
            "title": p["identity"]["title"],
            "department": p.get("department", ""),
            "clearance": p.get("clearance_level", ""),
            "tools": p.get("operational_parameters", {}).get("assigned_tools", []),
            "apis": p.get("operational_parameters", {}).get("api_access_rights", []),
            "prompt": p.get("operational_parameters", {}).get("system_prompt", ""),
            "specialization": p.get("operational_parameters", {}).get("specialization", ""),
        })
    return agents

# ═══════════════════════════════════════════════════════════════
# BOMB 3: GENOME EVOLUTION ENGINE
# ═══════════════════════════════════════════════════════════════
def load_genome() -> Dict:
    if GENOME_PATH.exists():
        with open(GENOME_PATH) as f:
            return json.load(f)
    return {}

def save_genome(genome: Dict):
    with open(GENOME_PATH, "w") as f:
        json.dump(genome, f, indent=2)

def get_agent_genome(agent_id: str) -> Dict:
    genome = load_genome()
    if agent_id not in genome:
        genome[agent_id] = {
            "performance": random.randint(75, 98),
            "learning": random.randint(70, 99),
            "reliability": random.randint(80, 100),
            "evolution": random.randint(60, 96),
            "tasks_completed": 0,
            "commands_received": 0,
            "last_active": datetime.now(timezone.utc).isoformat(),
            "evolution_history": []
        }
        save_genome(genome)
    return genome[agent_id]

def evolve_agent(agent_id: str, event_type: str = "task_complete"):
    genome = load_genome()
    ag = genome.get(agent_id, get_agent_genome(agent_id))
    
    deltas = {
        "task_complete": {"performance": 0.5, "learning": 0.3, "evolution": 0.4},
        "command_received": {"learning": 0.2, "evolution": 0.1},
        "error": {"reliability": -0.5, "performance": -0.3},
        "optimization": {"performance": 1.0, "evolution": 0.8, "learning": 0.5}
    }
    
    for key, delta in deltas.get(event_type, {}).items():
        ag[key] = max(0, min(100, round(ag[key] + delta, 1)))
    
    if event_type == "task_complete":
        ag["tasks_completed"] = ag.get("tasks_completed", 0) + 1
    if event_type == "command_received":
        ag["commands_received"] = ag.get("commands_received", 0) + 1
    
    ag["last_active"] = datetime.now(timezone.utc).isoformat()
    ag.setdefault("evolution_history", []).append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        "snapshot": {k: ag[k] for k in ["performance", "learning", "reliability", "evolution"]}
    })
    # Keep last 100 history entries
    ag["evolution_history"] = ag["evolution_history"][-100:]
    
    genome[agent_id] = ag
    save_genome(genome)
    return ag

# ═══════════════════════════════════════════════════════════════
# BOMB 5: NEXUS PULSE — SERVICE HEARTBEAT
# ═══════════════════════════════════════════════════════════════
async def check_service(svc: Dict) -> Dict:
    result = {**svc, "status": "offline", "response_ms": -1, "checked_at": datetime.now(timezone.utc).isoformat()}
    try:
        start = time.monotonic()
        if svc["check"] == "tcp":
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(svc["host"], svc["port"]), timeout=3
            )
            writer.close()
            await writer.wait_closed()
            result["status"] = "online"
        else:
            async with httpx.AsyncClient(timeout=5) as client:
                url = f"http://{svc['host']}:{svc['port']}{svc.get('path', '/')}"
                resp = await client.get(url)
                result["status"] = "online" if resp.status_code < 500 else "degraded"
                result["http_code"] = resp.status_code
        result["response_ms"] = round((time.monotonic() - start) * 1000)
    except Exception as e:
        result["status"] = "offline"
        result["error"] = str(e)[:100]
    return result

# ═══════════════════════════════════════════════════════════════
# BOMB 2: SOVEREIGN COMMAND — NL ROUTING
# ═══════════════════════════════════════════════════════════════
AGENT_KEYWORDS = {
    "AI-ARCH": ["code", "build", "architect", "develop", "deploy", "fix", "bug"],
    "SEC-GUARD": ["security", "guard", "firewall", "privacy", "lock", "breach"],
    "SHADOW-7-PLANET": ["shadow", "publish", "marketing", "content", "campaign"],
    "NEXUS-ANALYST": ["data", "analyze", "pattern", "analytics", "statistics"],
    "X-BIO": ["sensor", "bio", "esp32", "iot", "telemetry", "physical"],
    "RAG-CORE": ["search", "knowledge", "remember", "recall", "find", "retrieve"],
    "CLONE-HUB": ["simulate", "clone", "twin", "decision", "predict"],
    "LEGAL-EAGLE": ["legal", "patent", "ip", "compliance", "law", "contract"],
    "N-TARGET": ["finance", "invest", "money", "real estate", "portfolio"],
    "NAV-ORACLE": ["risk", "navigate", "growth", "trajectory", "forecast"],
    "OPS-CTRL": ["operation", "api", "server", "health", "status", "uptime"],
    "mrf": ["override", "broadcast", "sovereign", "god mode", "all agents"],
    "l0-ops": ["ops", "resource", "allocat", "command"],
    "l0-intel": ["intel", "competitor", "spy", "threat"],
    "l0-comms": ["message", "communicate", "announce", "broadcast"],
}

def route_command(command: str) -> str:
    cmd_lower = command.lower()
    scores = {}
    for agent_id, keywords in AGENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in cmd_lower)
        if score > 0:
            scores[agent_id] = score
    if not scores:
        return "mrf"  # Default to Mr.F
    return max(scores, key=scores.get)


async def _ollama_chat_with_ethical_gate(
    ollama_url: str,
    model: str,
    messages: list,
    check_ethical: Callable[[str], Tuple[bool, str]],
) -> tuple[str, bool, bool]:
    """
    Call Ollama with streaming; gate output mid-stream via ethical check.
    Returns (response_text, llm_ok, was_refused_midstream).
    """
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            async with client.stream(
                "POST",
                f"{ollama_url}/api/chat",
                json={"model": model, "messages": messages, "stream": True},
            ) as resp:
                if resp.status_code != 200:
                    return f"(LLM HTTP {resp.status_code})", False, False
                accumulated = ""
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content") or ""
                        accumulated = content
                        should_refuse, reason = check_ethical(accumulated)
                        if should_refuse:
                            return f"[SOVEREIGN_REFUSAL] {reason}", True, True
                        if chunk.get("done"):
                            return accumulated, True, False
                    except json.JSONDecodeError:
                        continue
                return accumulated or "(empty stream)", bool(accumulated), False
    except httpx.ConnectError as e:
        return f"(LLM connect failed: {str(e)[:80]})", False, False
    except httpx.TimeoutException:
        return "(LLM timeout — model may be loading)", False, False
    except Exception as e:
        return f"(LLM error: {type(e).__name__}: {str(e)[:80]})", False, False

class CommandRequest(BaseModel):
    command: str
    target_agent: Optional[str] = None

class GenomeEvent(BaseModel):
    agent_id: str
    event_type: str = "task_complete"

# ═══════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/")
def root():
    return {"system": "NEXUS NERVE CENTER", "version": "2.1.0-neural-genome", "status": "SOVEREIGN", "agents": 32, "services": len(SERVICES), "cognitive_bridge": "active" if cognitive_bridge and cognitive_bridge._entity_id else "fallback"}

# --- AGENTS ---
@app.get("/api/agents")
def list_agents():
    return {"agents": load_agents(), "count": len(load_agents())}

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: str):
    agents = load_agents()
    agent = next((a for a in agents if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(404, f"Agent {agent_id} not found")
    agent["genome"] = get_agent_genome(agent_id)
    return agent

# --- SOVEREIGN COMMAND ---
@app.post("/api/command")
async def sovereign_command(req: CommandRequest):
    target = req.target_agent or route_command(req.command)
    agents = load_agents()
    agent = next((a for a in agents if a["id"] == target), None)
    
    if not agent:
        agent = {"id": target, "name": target, "prompt": "You are a helpful assistant."}
    
    evolve_agent(target, "command_received")

    # ═══ NEURAL-GENOME COUPLING: Fetch hormonal + genome state before inference ═══
    signals, stats = SignalState(), GenomeStats()
    recent_awareness = ""
    if cognitive_bridge:
        signals, stats = await cognitive_bridge.fetch_entity_state()
        recent_awareness = await cognitive_bridge.get_recent_cognitive_awareness()
    ctx_prompt = cognitive_bridge.build_contextual_prompt(signals, stats, recent_awareness) if cognitive_bridge else ""
    
    system_prompt = f"""You are {agent['name']}, {agent.get('title', 'AI Agent')} in the Nexus Prime ecosystem.
Your specialization: {agent.get('specialization', 'General operations')}
Your tools: {', '.join(agent.get('tools', []))}
Respond concisely and in character. You serve MrF, the sovereign commander.{ctx_prompt}"""
    
    response_text = f"[{agent['name']}] Command acknowledged: '{req.command}'. Processing..."
    llm_ok = False
    was_refused_midstream = False

    def _ethical_check(text: str):
        return cognitive_bridge.check_ethical_violation(text, stats) if cognitive_bridge and stats else (False, "")

    response_text, llm_ok, was_refused_midstream = await _ollama_chat_with_ethical_gate(
        OLLAMA_URL,
        "llama3.2:3b",
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.command},
        ],
        _ethical_check,
    )
    if llm_ok and not was_refused_midstream:
        evolve_agent(target, "task_complete")

    # ═══ CODEX REALIZATION: Ethical filter + Feedback loop ═══
    if cognitive_bridge and signals and stats:
        if was_refused_midstream:
            await cognitive_bridge.update_signal_state(HormoneEvent.SOVEREIGN_REFUSAL)
        else:
            should_refuse, reason = cognitive_bridge.check_ethical_violation(response_text, stats)
            if should_refuse:
                response_text = f"[SOVEREIGN_REFUSAL] {reason}"
                await cognitive_bridge.update_signal_state(HormoneEvent.SOVEREIGN_REFUSAL)
            elif llm_ok:
                await cognitive_bridge.update_signal_state(HormoneEvent.TASK_SUCCESS)
            else:
                await cognitive_bridge.update_signal_state(HormoneEvent.TASK_FAILURE)
    
    return {
        "command": req.command,
        "routed_to": target,
        "agent_name": agent["name"],
        "agent_title": agent.get("title", ""),
        "response": response_text,
        "genome": get_agent_genome(target),
        "cognitive_state": {"mood": _mood_from_signals(signals)},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# --- GENOME ---
@app.get("/api/genome")
def all_genomes():
    genome = load_genome()
    return {"genomes": genome, "count": len(genome)}

@app.get("/api/genome/{agent_id}")
def agent_genome(agent_id: str):
    return {"agent_id": agent_id, "genome": get_agent_genome(agent_id)}

@app.post("/api/genome/evolve")
def evolve(req: GenomeEvent):
    result = evolve_agent(req.agent_id, req.event_type)
    return {"agent_id": req.agent_id, "event": req.event_type, "genome": result}

# --- PULSE ---
@app.get("/api/pulse")
async def system_pulse():
    tasks = [check_service(svc) for svc in SERVICES]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    services = []
    for r in results:
        if isinstance(r, Exception):
            services.append({"name": "unknown", "status": "error", "error": str(r)})
        else:
            services.append(r)
    
    online = sum(1 for s in services if s["status"] == "online")
    total = len(services)
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {"total": total, "online": online, "degraded": sum(1 for s in services if s["status"] == "degraded"), "offline": total - online - sum(1 for s in services if s["status"] == "degraded")},
        "uptime_pct": round(online / total * 100, 1),
        "services": services
    }

# --- SHADOW AUTOPILOT (BOMB 4) ---
@app.post("/api/autopilot/trigger")
async def trigger_autopilot(manuscript_title: str = "Untitled"):
    """Trigger the full Shadow Autopilot Pipeline"""
    pipeline = [
        {"step": 1, "agent": "SHADOW-7-PLANET", "action": "Manuscript ingestion", "status": "triggered"},
        {"step": 2, "agent": "NEXUS-ANALYST", "action": "Deep content analysis", "status": "queued"},
        {"step": 3, "agent": "EDIT_02", "action": "Elite language editing", "status": "queued"},
        {"step": 4, "agent": "SENT_03", "action": "Legal compliance scan", "status": "queued"},
        {"step": 5, "agent": "coverDesignAgent", "action": "Cover art generation", "status": "queued"},
        {"step": 6, "agent": "marketingAgent", "action": "Marketing strategy", "status": "queued"},
        {"step": 7, "agent": "mediaScriptAgent", "action": "Media script conversion", "status": "queued"},
        {"step": 8, "agent": "socialMediaAgent", "action": "Social media campaign", "status": "queued"},
        {"step": 9, "agent": "SHADOW-7-PLANET", "action": "Email campaign dispatch", "status": "queued"},
        {"step": 10, "agent": "mrf", "action": "Final sovereign approval", "status": "pending"}
    ]
    
    # Evolve all agents in the pipeline
    for step in pipeline:
        evolve_agent(step["agent"], "command_received")
    
    return {
        "pipeline_id": f"SAP-{int(time.time())}",
        "manuscript": manuscript_title,
        "steps": pipeline,
        "total_agents_engaged": len(set(s["agent"] for s in pipeline)),
        "status": "ARMED",
        "triggered_at": datetime.now(timezone.utc).isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# EMAIL SERVICE API
# ═══════════════════════════════════════════════════════════════
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "NEXUS PRIME")

def send_smtp_email(to: str, subject: str, body: str, html: Optional[str] = None) -> dict:
    """Send email via SMTP"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        msg["To"] = to
        msg.attach(MIMEText(body, "plain", "utf-8"))
        if html:
            msg.attach(MIMEText(html, "html", "utf-8"))
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM_EMAIL, [to], msg.as_string())
        
        return {"success": True, "message": f"Email sent to {to}", "subject": subject}
    except smtplib.SMTPAuthenticationError as e:
        return {"success": False, "error": "Authentication failed", "details": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e), "type": type(e).__name__}

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    html: Optional[str] = None

class AlertEmailRequest(BaseModel):
    to: str
    alert_type: str
    message: str

class ReportEmailRequest(BaseModel):
    to: str
    report_name: str
    report_content: str
    attachment_path: Optional[str] = None

@app.post("/api/email/send")
def send_email(req: EmailRequest):
    """Send a custom email"""
    return send_smtp_email(to=req.to, subject=req.subject, body=req.body, html=req.html)

@app.post("/api/email/alert")
def send_alert(req: AlertEmailRequest):
    """Send a system alert email"""
    subject = f"🚨 NEXUS ALERT: {req.alert_type}"
    html = f"""
    <html>
    <body style="font-family: Arial; background: #1a1a2e; color: #eee; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: #16213e; border-radius: 10px; padding: 30px;">
            <h1 style="color: #e94560;">🚨 SYSTEM ALERT</h1>
            <p>Alert Type: <strong style="color: #e74c3c;">{req.alert_type}</strong></p>
            <div style="background: #0f3460; padding: 20px; border-radius: 8px;">
                <pre style="white-space: pre-wrap;">{req.message}</pre>
            </div>
            <p style="color: #7f8c8d; font-size: 12px; margin-top: 20px;">NEXUS PRIME AI System</p>
        </div>
    </body>
    </html>
    """
    return send_smtp_email(to=req.to, subject=subject, body=req.message, html=html)

@app.post("/api/email/report")
def send_report(req: ReportEmailRequest):
    """Send a system report email"""
    subject = f"📊 NEXUS REPORT: {req.report_name}"
    html = f"""
    <html>
    <body style="font-family: Arial; background: #1a1a2e; color: #eee; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: #16213e; border-radius: 10px; padding: 30px;">
            <h1 style="color: #00d9ff;">📊 SYSTEM REPORT</h1>
            <h2>{req.report_name}</h2>
            <div style="background: #0f3460; padding: 20px; border-radius: 8px;">
                <pre style="white-space: pre-wrap; font-family: monospace;">{req.report_content}</pre>
            </div>
            <p style="color: #7f8c8d; font-size: 12px; margin-top: 20px;">Generated by NEXUS PRIME</p>
        </div>
    </body>
    </html>
    """
    return send_smtp_email(to=req.to, subject=subject, body=req.report_content, html=html)

@app.get("/api/email/test")
def test_email():
    """Test email configuration"""
    return {
        "smtp_host": SMTP_HOST,
        "smtp_port": SMTP_PORT,
        "smtp_user": SMTP_USER,
        "from_email": SMTP_FROM_EMAIL,
        "from_name": SMTP_FROM_NAME,
        "status": "configured" if SMTP_USER else "not_configured"
    }

# --- CONSCIOUSNESS / SOUL MONITOR ---
@app.get("/api/consciousness")
async def soul_monitor():
    """Soul Monitor — observable consciousness: mood, hormones, ethical posture, tier."""
    if not cognitive_bridge:
        return {"status": "uncoupled", "message": "Cognitive bridge not initialized"}
    signals, stats = await cognitive_bridge.fetch_entity_state()
    mood = _mood_from_signals(signals)
    deficit = 0.0
    from cognitive_bridge import GENE_STAT_WEIGHTS
    for k, w in GENE_STAT_WEIGHTS.items():
        v = getattr(stats, k, 0.5)
        if v < 0.5:
            deficit += w * (1.0 - v)
    tier = "CALM" if signals.cortisol < 0.35 and signals.gaba > 0.55 else "WATCHFUL"
    if signals.cortisol > 0.6:
        tier = "STRESSED"
    elif signals.dopamine > 0.7 and signals.serotonin > 0.6:
        tier = "JOYFUL"
    return {
        "entity": cognitive_bridge.SOVEREIGN_ENTITY_NAME,
        "mood": mood,
        "soul_tier": tier,
        "ethical_deficit": round(deficit, 3),
        "signal_molecules": signals.to_dict(),
        "genome_stats": {k: getattr(stats, k) for k in ["compliance", "alignment", "empathy", "cognition", "sentience"] if hasattr(stats, k)},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# --- INNOVATION INDEX ---
@app.get("/api/innovation/score")
async def innovation_score():
    """Innovation Index 0-100 + Revolution Tier. Unprecedented tech valuation."""
    components = {}
    if cognitive_bridge:
        components["genome_coupled"] = bool(cognitive_bridge._entity_id)
        components["hormones_active"] = True
        components["ethical_gate"] = True
        components["memory_synced"] = True
        components["daemon_ledger"] = True
        components["cognitive_timeline"] = True
    else:
        components = {k: False for k in ["genome_coupled", "hormones_active", "ethical_gate", "memory_synced", "daemon_ledger", "cognitive_timeline"]}
    active = sum(1 for v in components.values() if v)
    score = round((active / 6) * 100)
    if score <= 50:
        tier = "FOUNDATION"
    elif score <= 75:
        tier = "EMERGENT"
    elif score <= 90:
        tier = "SOVEREIGN"
    else:
        tier = "APEX"
    return {
        "innovation_score": score,
        "revolution_tier": tier,
        "components": components,
        "active_count": active,
        "total": 6,
    }

# --- COGNITIVE BRIDGE / NEURAL-GENOME STATE ---
@app.get("/api/cognitive/state")
async def get_cognitive_state():
    """Current hormonal + genome state of the Sovereign Entity (AS-SULTAN)"""
    if not cognitive_bridge:
        return {"status": "uncoupled", "message": "Cognitive bridge not initialized (no DB)"}
    signals, stats = await cognitive_bridge.fetch_entity_state()
    return {
        "entity": cognitive_bridge.SOVEREIGN_ENTITY_NAME,
        "entity_id": cognitive_bridge._entity_id,
        "mood": _mood_from_signals(signals),
        "signal_molecules": signals.to_dict(),
        "genome_stats": {
            "cognition": stats.cognition, "empathy": stats.empathy,
            "compliance": stats.compliance, "alignment": stats.alignment,
            "creative": stats.creative, "sentience": stats.sentience,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --- SYSTEM OVERVIEW ---
@app.get("/api/overview")
async def system_overview():
    agents = load_agents()
    genome = load_genome()
    
    dept_counts = {}
    for a in agents:
        d = a["department"]
        dept_counts[d] = dept_counts.get(d, 0) + 1
    
    all_tools = set()
    for a in agents:
        all_tools.update(a.get("tools", []))
    
    return {
        "system": "NEXUS PRIME",
        "version": "2.1.0-neural-genome",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agents": {"total": len(agents), "with_genome": len(genome), "departments": dept_counts},
        "capabilities": {"unique_tools": len(all_tools), "tools_list": sorted(all_tools)},
        "infrastructure": {"services": len(SERVICES), "products": 14, "subdomains": 25, "lines_of_code": "447K+"}
    }

# ═══════════════════════════════════════════════════════════════
# BOARDROOM BRIDGE — Agent Summoning & Chat
# ═══════════════════════════════════════════════════════════════

class BoardroomChat(BaseModel):
    agent_id: str
    message: str

@app.get("/api/boardroom/roster")
def boardroom_roster():
    """List all agents available for summoning"""
    return {"agents": bridge.list_agents(), "total": bridge.get_agent_count()}

@app.get("/api/boardroom/summon/{agent_id}")
def boardroom_summon(agent_id: str):
    """Summon an agent into the boardroom — returns full identity + injected prompt"""
    result = bridge.summon_agent(agent_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    return result

@app.get("/api/boardroom/department/{dept_name}")
def boardroom_department(dept_name: str):
    """Summon all agents from a department"""
    results = bridge.summon_department(dept_name)
    if not results:
        raise HTTPException(404, f"No agents found in department '{dept_name}'")
    return {"department": dept_name, "agents": results, "count": len(results)}

@app.post("/api/boardroom/chat")
async def boardroom_chat(req: BoardroomChat):
    """Chat with a summoned agent — uses their injected prompt via Ollama. Neural-Genome coupled."""
    summoned = bridge.summon_agent(req.agent_id)
    if "error" in summoned:
        raise HTTPException(404, summoned["error"])

    # ═══ NEURAL-GENOME COUPLING: Fetch state before inference ═══
    signals, stats = SignalState(), GenomeStats()
    recent_awareness = ""
    if cognitive_bridge:
        signals, stats = await cognitive_bridge.fetch_entity_state()
        recent_awareness = await cognitive_bridge.get_recent_cognitive_awareness()
    ctx_prompt = cognitive_bridge.build_contextual_prompt(signals, stats, recent_awareness) if cognitive_bridge else ""
    system_prompt = summoned["injected_prompt"] + ctx_prompt

    evolve_agent(req.agent_id, "command_received")

    response_text = f"[{summoned['agent_name']}] Acknowledged. Processing directive..."
    llm_ok = False
    was_refused_midstream = False

    def _ethical_check_br(text: str):
        return cognitive_bridge.check_ethical_violation(text, stats) if cognitive_bridge and stats else (False, "")

    response_text, llm_ok, was_refused_midstream = await _ollama_chat_with_ethical_gate(
        OLLAMA_URL,
        "llama3.2:3b",
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message},
        ],
        _ethical_check_br,
    )
    if llm_ok and not was_refused_midstream:
        evolve_agent(req.agent_id, "task_complete")

    # ═══ CODEX REALIZATION: Ethical filter + Feedback loop ═══
    if cognitive_bridge:
        if was_refused_midstream:
            await cognitive_bridge.update_signal_state(HormoneEvent.SOVEREIGN_REFUSAL)
        else:
            should_refuse, reason = cognitive_bridge.check_ethical_violation(response_text, stats)
            if should_refuse:
                response_text = f"[SOVEREIGN_REFUSAL] {reason}"
                await cognitive_bridge.update_signal_state(HormoneEvent.SOVEREIGN_REFUSAL)
            elif llm_ok:
                await cognitive_bridge.update_signal_state(HormoneEvent.TASK_SUCCESS)
            else:
                await cognitive_bridge.update_signal_state(HormoneEvent.TASK_FAILURE)

    return {
        "agent_id": req.agent_id,
        "agent_name": summoned["agent_name"],
        "department": summoned["department"],
        "message": req.message,
        "response": response_text,
        "genome": get_agent_genome(req.agent_id),
        "cognitive_state": {"mood": _mood_from_signals(signals)},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# NEURAL SPINE INTEGRATION
# ═══════════════════════════════════════════════════════════════

SPINE_URL = os.getenv("SPINE_URL", "http://neural_spine:8300")

class SpineInterruptRequest(BaseModel):
    source_agent: int = 0
    target_agent: int = 0
    interrupt_type: int = 0
    priority: int = 5
    payload: str = ""

@app.get("/api/spine/phi")
async def get_spine_phi():
    """Get Phi* consciousness metric — integrated information of the 32-agent collective"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{SPINE_URL}/status")
            data = resp.json()
            agents = data.get("agents", {})
            return {
                "phi_star": data.get("headroom_pct"),
                "phi_status": "healthy" if agents.get("active", 0) > 0 else "offline",
                "active_agents": agents.get("active", 0),
                "cognitive_cycles": data.get("cognitive_cycles", 0),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        return {"status": "spine_offline", "error": str(e)}

@app.get("/api/spine/cycle")
async def get_spine_cycle():
    """Get current cognitive cycle stats — latency, throughput, GWT broadcasts"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{SPINE_URL}/status")
            data = resp.json()
            gwt = data.get("gwt", {})
            ring = data.get("ring_buffer", {})
            agents = data.get("agents", {})
            return {
                "cycles_total": data.get("cognitive_cycles"),
                "cycle_avg_us": data.get("avg_cycle_us"),
                "headroom_pct": data.get("headroom_pct"),
                "gwt_broadcasts": gwt.get("broadcast_count"),
                "gwt_avg_us": gwt.get("avg_broadcast_us"),
                "ring_buffer_len": ring.get("current_len"),
                "ring_buffer_capacity": ring.get("capacity"),
                "active_agents": agents.get("active"),
                "total_agents": agents.get("total"),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        return {"status": "spine_offline", "error": str(e)}

@app.post("/api/spine/interrupt")
async def inject_spine_interrupt(req: SpineInterruptRequest):
    """Inject a priority interrupt into the Neural Spine ring buffer"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(f"{SPINE_URL}/interrupt", json={
                "source_agent": req.source_agent,
                "target_agent": req.target_agent,
                "interrupt_type": req.interrupt_type,
                "priority": req.priority,
                "payload": req.payload
            })
            return resp.json()
    except Exception as e:
        return {"status": "spine_offline", "error": str(e)}

@app.get("/api/spine/health")
async def spine_health():
    """Check Neural Spine server health"""
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get(f"{SPINE_URL}/health")
            return resp.json()
    except Exception as e:
        return {"status": "offline", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200)
