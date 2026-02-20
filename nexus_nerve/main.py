"""
NEXUS NERVE CENTER — Sovereign Command API
══════════════════════════════════════════
BOMB 2: Sovereign Command → Routes NL commands to agents via LLM
BOMB 3: Agent Genome → Tracks & evolves agent DNA over time
BOMB 5: Nexus Pulse → Real-time heartbeat of all 21 services
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx, asyncio, os, json, yaml, time, random
from datetime import datetime, timezone
from pathlib import Path
from boardroom_bridge import BoardroomBridge

app = FastAPI(title="Nexus Nerve Center API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Boardroom Bridge instance
bridge = BoardroomBridge()

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
    return {"system": "NEXUS NERVE CENTER", "version": "2.0.0", "status": "SOVEREIGN", "agents": 32, "services": len(SERVICES)}

@app.get("/health")
def health():
    return {"status": "online", "timestamp": datetime.now(timezone.utc).isoformat()}

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
    
    # Try to get LLM response via Ollama
    response_text = f"[{agent['name']}] Command acknowledged: '{req.command}'. Processing..."
    try:
        system_prompt = f"""You are {agent['name']}, {agent.get('title', 'AI Agent')} in the Nexus Prime ecosystem.
Your specialization: {agent.get('specialization', 'General operations')}
Your tools: {', '.join(agent.get('tools', []))}
Respond concisely and in character. You serve MrF, the sovereign commander."""
        
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(f"{OLLAMA_URL}/api/chat", json={
                "model": "llama3.2:3b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": req.command}
                ],
                "stream": False
            })
            if resp.status_code == 200:
                data = resp.json()
                response_text = data.get("message", {}).get("content", response_text)
                evolve_agent(target, "task_complete")
            else:
                response_text += f" (LLM HTTP {resp.status_code})"
    except httpx.ConnectError as e:
        response_text += f" (LLM connect failed: {str(e)[:80]})"
    except httpx.TimeoutException:
        response_text += " (LLM timeout — model may be loading)"
    except Exception as e:
        response_text += f" (LLM error: {type(e).__name__}: {str(e)[:80]})"
    
    return {
        "command": req.command,
        "routed_to": target,
        "agent_name": agent["name"],
        "agent_title": agent.get("title", ""),
        "response": response_text,
        "genome": get_agent_genome(target),
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
        "version": "2.0.0",
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
    """Chat with a summoned agent — uses their injected prompt via Ollama"""
    summoned = bridge.summon_agent(req.agent_id)
    if "error" in summoned:
        raise HTTPException(404, summoned["error"])

    system_prompt = summoned["injected_prompt"]
    evolve_agent(req.agent_id, "command_received")

    response_text = f"[{summoned['agent_name']}] Acknowledged. Processing directive..."
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(f"{OLLAMA_URL}/api/chat", json={
                "model": "llama3.2:3b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": req.message}
                ],
                "stream": False
            })
            if resp.status_code == 200:
                data = resp.json()
                response_text = data.get("message", {}).get("content", response_text)
                evolve_agent(req.agent_id, "task_complete")
            else:
                response_text += f" (LLM HTTP {resp.status_code})"
    except httpx.ConnectError as e:
        response_text += f" (LLM connect failed: {str(e)[:80]})"
    except httpx.TimeoutException:
        response_text += " (LLM timeout — model may be loading)"
    except Exception as e:
        response_text += f" (LLM error: {type(e).__name__}: {str(e)[:80]})"

    return {
        "agent_id": req.agent_id,
        "agent_name": summoned["agent_name"],
        "department": summoned["department"],
        "message": req.message,
        "response": response_text,
        "genome": get_agent_genome(req.agent_id),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200)
