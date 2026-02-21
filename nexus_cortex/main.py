#!/usr/bin/env python3
"""
NEXUS CORTEX v2.0.0-sovereign
المركز العصبي المركزي + Redis Pub/Sub
ضابط السير والحركة — يوجه الأوامر، يراقب الوكلاء، يحافظ على المركزية

Port: 8090
"""

import asyncio
import json
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List, Any
from uuid import UUID

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ─────────────────── Config ─────────────────────────────────────
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:nexus_mrf_password_2026@nexus_db:5432/nexus_db"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://nexus_redis:6379/0")
CORTEX_VERSION = "2.0.0-sovereign"

# ─────────────────── Connection Pools ───────────────────────────
pool: asyncpg.Pool = None
redis_pool: aioredis.Redis = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool, redis_pool
    pool = await asyncpg.create_pool(DB_URL, min_size=5, max_size=20)
    print(f"[CORTEX] ✅ Connected to nexus_db")
    # Redis
    redis_pool = aioredis.from_url(REDIS_URL, decode_responses=True)
    await redis_pool.ping()
    print(f"[CORTEX] ✅ Connected to Redis")
    # Start subscriber
    asyncio.create_task(redis_subscriber())
    # register cortex itself as online
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO nexus_core.agent_state (agent_name, status, updated_at)
            VALUES ('nexus_cortex', 'online', now())
            ON CONFLICT (agent_name) DO UPDATE SET status='online', updated_at=now()
        """)
        await conn.execute("""
            UPDATE nexus_core.agents SET status='online', last_seen=now()
            WHERE name='nexus_cortex'
        """)
    yield
    if redis_pool:
        await redis_pool.aclose()
        print(f"[CORTEX] 🛑 Redis closed")
    await pool.close()
    print(f"[CORTEX] 🛑 Pool closed")


# ─────────────────── App ────────────────────────────────────────
app = FastAPI(
    title="NEXUS Cortex",
    description="المركز العصبي المركزي لنظام NEXUS PRIME — ضابط السير والحركة",
    version=CORTEX_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────── WebSocket Manager ──────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for ws in self.active:
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)

ws_manager = ConnectionManager()


# ─────────────────── Redis Subscriber ───────────────────────────
async def redis_subscriber():
    """Subscribe to Redis channels and broadcast to WebSocket clients"""
    try:
        pubsub = redis_pool.pubsub()
        await pubsub.subscribe(
            "nexus:commands", "nexus:events", "nexus:agents",
            "nexus:spine:status", "nexus:spine:phi", "nexus:spine:broadcast"
        )
        print(f"[CORTEX] 📡 Redis subscriber active on 6 channels (incl. spine)")
        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    channel = message.get("channel", "")
                    data = json.loads(message["data"])
                    # Tag spine messages for frontend filtering
                    if channel.startswith("nexus:spine:"):
                        spine_type = channel.split(":")[-1]  # status, phi, broadcast
                        data = {"type": f"spine_{spine_type}", "data": data}
                    await ws_manager.broadcast(data)
                except Exception as e:
                    print(f"[CORTEX] ⚠️ Broadcast error: {e}")
    except Exception as e:
        print(f"[CORTEX] ❌ Redis subscriber failed: {e}")


# ─────────────────── Pydantic Models ────────────────────────────
class CommandRequest(BaseModel):
    command_type: str
    origin: str = "human"
    target_agent: Optional[str] = None
    payload: dict = {}
    priority: int = 5

class CommandUpdate(BaseModel):
    status: str
    result: Optional[dict] = None
    error_msg: Optional[str] = None

class AgentRegister(BaseModel):
    name: str
    display_name: Optional[str] = None
    agent_type: str = "planet"
    capabilities: List[str] = []
    endpoint: Optional[str] = None

class EventPost(BaseModel):
    agent_name: str
    event_type: str
    severity: str = "info"
    title: Optional[str] = None
    body: dict = {}
    command_id: Optional[str] = None

class HeartbeatPost(BaseModel):
    current_task: Optional[str] = None
    metrics: dict = {}

# ─────────────────── Routes ─────────────────────────────────────

@app.get("/", tags=["Core"])
async def root():
    return {
        "service": "NEXUS Cortex",
        "version": CORTEX_VERSION,
        "status": "online",
        "role": "ضابط السير والحركة",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health", tags=["Core"])
async def health():
    async with pool.acquire() as conn:
        db_ok = await conn.fetchval("SELECT 1") == 1
    redis_ok = await redis_pool.ping() if redis_pool else False
    return {
        "cortex": "online",
        "version": CORTEX_VERSION,
        "db": "ok" if db_ok else "error",
        "redis": "ok" if redis_ok else "error"
    }

# ─── Dashboard ──────────────────────────────────────────────────

@app.get("/dashboard", tags=["Dashboard"])
async def dashboard():
    """لوحة التحكم المركزية — حالة كل وكيل وكوكب"""
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM nexus_core.cortex_dashboard")
        agents = [dict(r) for r in rows]

        # إحصائيات عامة
        stats = await conn.fetchrow("""
            SELECT
              (SELECT COUNT(*) FROM nexus_core.agents WHERE status='online') AS online_count,
              (SELECT COUNT(*) FROM nexus_core.commands WHERE status='queued') AS queued_commands,
              (SELECT COUNT(*) FROM nexus_core.commands WHERE status='running') AS running_commands,
              (SELECT COUNT(*) FROM nexus_core.events WHERE created_at > now() - INTERVAL '1 hour') AS recent_events
        """)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stats": dict(stats),
        "agents": agents
    }

# ─── Agents ─────────────────────────────────────────────────────

@app.get("/agents", tags=["Agents"])
async def list_agents():
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM nexus_core.agents ORDER BY agent_type, name")
    return {"agents": [dict(r) for r in rows]}

@app.post("/agent/register", tags=["Agents"])
async def register_agent(body: AgentRegister):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO nexus_core.agents (name, display_name, agent_type, capabilities, endpoint, status, last_seen)
            VALUES ($1,$2,$3,$4,$5,'online',now())
            ON CONFLICT (name) DO UPDATE SET
              display_name=EXCLUDED.display_name,
              capabilities=EXCLUDED.capabilities,
              endpoint=EXCLUDED.endpoint,
              status='online',
              last_seen=now()
        """, body.name, body.display_name or body.name, body.agent_type,
            json.dumps(body.capabilities), body.endpoint)

        await conn.execute("""
            INSERT INTO nexus_core.agent_state (agent_name, status, updated_at)
            VALUES ($1,'online',now())
            ON CONFLICT (agent_name) DO UPDATE SET status='online', updated_at=now()
        """, body.name)

    await redis_pool.publish("nexus:agents", json.dumps({"type": "agent_online", "agent": body.name}))
    return {"registered": body.name, "status": "online"}

@app.post("/agent/{agent_name}/heartbeat", tags=["Agents"])
async def agent_heartbeat(agent_name: str, body: HeartbeatPost):
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE nexus_core.agents SET status='online', last_seen=now()
            WHERE name=$1
        """, agent_name)
        await conn.execute("""
            INSERT INTO nexus_core.agent_state (agent_name, status, current_task, metrics, updated_at)
            VALUES ($1,'online',$2,$3,now())
            ON CONFLICT (agent_name) DO UPDATE SET
              status='online', current_task=$2, metrics=$3, updated_at=now()
        """, agent_name, body.current_task, json.dumps(body.metrics))
    return {"agent": agent_name, "heartbeat": "ok"}

@app.get("/agent/{agent_name}", tags=["Agents"])
async def get_agent(agent_name: str):
    async with pool.acquire() as conn:
        agent = await conn.fetchrow("SELECT * FROM nexus_core.agents WHERE name=$1", agent_name)
        if not agent:
            raise HTTPException(404, f"Agent '{agent_name}' not found")
        state = await conn.fetchrow("SELECT * FROM nexus_core.agent_state WHERE agent_name=$1", agent_name)
        cmds = await conn.fetch("""
            SELECT id, command_type, status, priority, created_at
            FROM nexus_core.commands
            WHERE target_agent=$1 ORDER BY created_at DESC LIMIT 10
        """, agent_name)
    return {
        "agent": dict(agent),
        "state": dict(state) if state else None,
        "recent_commands": [dict(c) for c in cmds]
    }

# ─── Commands ───────────────────────────────────────────────────

@app.post("/command", tags=["Commands"])
async def issue_command(body: CommandRequest, bg: BackgroundTasks):
    """إصدار أمر — يُوجَّه تلقائياً للوكيل المناسب"""
    target = body.target_agent

    async with pool.acquire() as conn:
        # إذا لم يحدد الهدف → ابحث في routing_rules
        if not target:
            row = await conn.fetchrow("""
                SELECT target_agent FROM nexus_core.routing_rules
                WHERE command_type=$1 AND is_active=true
                ORDER BY priority LIMIT 1
            """, body.command_type)
            target = row["target_agent"] if row else None

        # أنشئ الأمر
        cmd_id = await conn.fetchval("""
            INSERT INTO nexus_core.commands
              (command_type, origin, target_agent, payload, priority, status, created_at)
            VALUES ($1,$2,$3,$4,$5,'queued',now())
            RETURNING id
        """, body.command_type, body.origin, target,
            json.dumps(body.payload), body.priority)

        # سجّل حدث
        await conn.execute("""
            INSERT INTO nexus_core.events (agent_name, event_type, severity, title, body, command_id)
            VALUES ('nexus_cortex','command_issued','info',$1,$2,$3)
        """, f"Command {body.command_type} → {target or 'broadcast'}",
            json.dumps({"origin": body.origin, "target": target}),
            cmd_id)

    await redis_pool.publish("nexus:commands", json.dumps({
        "type": "command_issued",
        "command_id": str(cmd_id),
        "command_type": body.command_type,
        "target": target,
        "priority": body.priority
    }))

    return {
        "command_id": str(cmd_id),
        "status": "queued",
        "target_agent": target,
        "command_type": body.command_type
    }

@app.get("/command/{command_id}", tags=["Commands"])
async def get_command(command_id: str):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM nexus_core.commands WHERE id=$1", UUID(command_id)
        )
        if not row:
            raise HTTPException(404, "Command not found")
    return dict(row)

@app.patch("/command/{command_id}", tags=["Commands"])
async def update_command(command_id: str, body: CommandUpdate):
    """الوكيل يُحدّث حالة الأمر بعد تنفيذه"""
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            UPDATE nexus_core.commands
            SET status=$2, result=$3, error_msg=$4,
                completed_at = CASE WHEN $2 IN ('done','failed') THEN now() ELSE completed_at END,
                updated_at=now()
            WHERE id=$5
            RETURNING *
        """, None, body.status, json.dumps(body.result) if body.result else None,
            body.error_msg, UUID(command_id))
        if not row:
            raise HTTPException(404, "Command not found")
    await redis_pool.publish("nexus:commands", json.dumps({"type": "command_updated", "command_id": command_id, "status": body.status}))
    return dict(row)

@app.get("/commands", tags=["Commands"])
async def list_commands(
    status: Optional[str] = None,
    agent: Optional[str] = None,
    limit: int = 50
):
    filters = []
    params: List[Any] = []
    if status:
        params.append(status)
        filters.append(f"status=${len(params)}")
    if agent:
        params.append(agent)
        filters.append(f"target_agent=${len(params)}")
    params.append(limit)
    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            f"SELECT * FROM nexus_core.commands {where} ORDER BY created_at DESC LIMIT ${len(params)}",
            *params
        )
    return {"commands": [dict(r) for r in rows], "count": len(rows)}

# ─── Events ─────────────────────────────────────────────────────

@app.post("/event", tags=["Events"])
async def post_event(body: EventPost):
    """أي وكيل يرسل حدث هنا"""
    async with pool.acquire() as conn:
        eid = await conn.fetchval("""
            INSERT INTO nexus_core.events
              (agent_name, event_type, severity, title, body, command_id, created_at)
            VALUES ($1,$2,$3,$4,$5,$6,now())
            RETURNING id
        """, body.agent_name, body.event_type, body.severity,
            body.title, json.dumps(body.body),
            UUID(body.command_id) if body.command_id else None)

        # تحديث last_seen للوكيل
        await conn.execute(
            "UPDATE nexus_core.agents SET last_seen=now() WHERE name=$1",
            body.agent_name
        )
    await redis_pool.publish("nexus:events", json.dumps({
        "type": "event",
        "event_id": eid,
        "agent": body.agent_name,
        "event_type": body.event_type,
        "severity": body.severity,
        "title": body.title
    }))
    return {"event_id": eid, "recorded": True}

@app.get("/events", tags=["Events"])
async def list_events(
    agent: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100
):
    filters = []
    params: List[Any] = []
    if agent:
        params.append(agent)
        filters.append(f"agent_name=${len(params)}")
    if severity:
        params.append(severity)
        filters.append(f"severity=${len(params)}")
    params.append(limit)
    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            f"SELECT * FROM nexus_core.events {where} ORDER BY created_at DESC LIMIT ${len(params)}",
            *params
        )
    return {"events": [dict(r) for r in rows], "count": len(rows)}

# ─── Routing Rules ───────────────────────────────────────────────

@app.get("/routing", tags=["Routing"])
async def get_routing_rules():
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM nexus_core.routing_rules WHERE is_active=true ORDER BY command_type")
    return {"routing_rules": [dict(r) for r in rows]}

@app.post("/routing", tags=["Routing"])
async def add_routing_rule(command_type: str, target_agent: str, priority: int = 5):
    async with pool.acquire() as conn:
        rid = await conn.fetchval("""
            INSERT INTO nexus_core.routing_rules (command_type, target_agent, priority)
            VALUES ($1,$2,$3) RETURNING id
        """, command_type, target_agent, priority)
    return {"rule_id": rid, "command_type": command_type, "target_agent": target_agent}

# ─── WebSocket ──────────────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time feed — كل حدث وأمر يُبث هنا"""
    await ws_manager.connect(websocket)
    try:
        # أرسل الحالة الأولية
        await websocket.send_json({"type": "connected", "cortex": CORTEX_VERSION})
        while True:
            data = await websocket.receive_text()
            # الوكيل يمكن أن يرسل heartbeat عبر WS
            try:
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except Exception:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# ─── Neural Spine Integration ───────────────────────────────────

import httpx

SPINE_URL = os.getenv("SPINE_URL", "http://neural_spine:8300")

@app.get("/spine/status", tags=["Neural Spine"])
async def spine_status():
    """Proxy to Neural Spine server for cognitive backbone status"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{SPINE_URL}/status")
            return resp.json()
    except Exception as e:
        return {"status": "offline", "error": str(e)}

@app.get("/spine/metrics", tags=["Neural Spine"])
async def spine_metrics():
    """Proxy to Neural Spine Prometheus metrics"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{SPINE_URL}/metrics")
            return {"metrics": resp.text}
    except Exception as e:
        return {"status": "offline", "error": str(e)}

@app.get("/spine/phi", tags=["Neural Spine"])
async def spine_phi():
    """Get latest Phi* consciousness metric from Redis"""
    try:
        phi_data = await redis_pool.get("nexus:spine:phi:latest")
        if phi_data:
            return json.loads(phi_data)
        return {"phi_star": None, "status": "no_data"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=False)
