"""
🧠 NEXUS MEMORY KEEPER v1.0.0
═══════════════════════════════════════

حارس الذاكرة المركزية والوعي الذاتي لنظام NEXUS PRIME

المهام الرئيسية:
• 📝 تسجيل جميع الأحداث والتغييرات في قاعدة البيانات
• 🧠 الوعي الذاتي - معرفة كاملة بالنظام والوكلاء الـ 21
• 💬 واجهة محادثة ذكية مع المستخدمين
• 📊 تقديم تقارير شاملة لـ NEXUS PRIME
• 🔍 استعلام الذاكرة التاريخية
• 🤔 التأمل والتفكير الذاتي

المؤلف: MrF + NEXUS PRIME
التاريخ: 20 فبراير 2026
"""

import asyncio
import json
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from uuid import UUID

import asyncpg
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx

# ═══════════════════════════════════════════════════════════
# 🔧 Configuration
# ═══════════════════════════════════════════════════════════

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:nexus_mrf_password_2026@nexus_db:5432/nexus_db"
)
CORTEX_URL = os.getenv("CORTEX_URL", "http://nexus_cortex:8090")
LITELLM_URL = os.getenv("LITELLM_URL", "http://nexus_litellm:4000")
LITELLM_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-nexus-sovereign-mrf103")

pool: Optional[asyncpg.Pool] = None

# ═══════════════════════════════════════════════════════════
# 📋 Pydantic Models
# ═══════════════════════════════════════════════════════════

class MemoryRecord(BaseModel):
    change_type: str = Field(..., description="نوع التغيير: deployment, config, code, schema, data, agent, integration")
    component: str = Field(..., description="اسم المكون المتأثر")
    description: str = Field(..., description="وصف التغيير")
    author: str = Field(default="system", description="من قام بالتغيير")
    before_state: Optional[Dict[str, Any]] = Field(default=None, description="الحالة قبل التغيير")
    after_state: Optional[Dict[str, Any]] = Field(default=None, description="الحالة بعد التغيير")
    files_affected: List[str] = Field(default_factory=list, description="الملفات المتأثرة")
    impact_level: str = Field(default="low", description="مستوى التأثير: low, medium, high, critical")

class ConversationMessage(BaseModel):
    user_name: str = Field(default="MrF", description="اسم المستخدم")
    message: str = Field(..., description="الرسالة")
    context: Dict[str, Any] = Field(default_factory=dict, description="السياق")

class ReflectionRequest(BaseModel):
    question: str = Field(..., description="السؤال للتفكير فيه")
    reflection_type: str = Field(default="health", description="نوع التأمل: health, performance, purpose, capability, relationship, forecast")

class IncidentReport(BaseModel):
    severity: str = Field(..., description="الخطورة: info, warning, error, critical, fatal")
    agent_name: Optional[str] = Field(default=None, description="اسم الوكيل")
    incident_type: str = Field(..., description="نوع الحادث: connection, timeout, crash, security, data, performance")
    message: str = Field(..., description="رسالة الحادث")
    stack_trace: Optional[str] = Field(default=None, description="stack trace")
    context: Dict[str, Any] = Field(default_factory=dict, description="السياق")

class RelationshipCreate(BaseModel):
    agent_a: str = Field(..., description="الوكيل الأول")
    agent_b: str = Field(..., description="الوكيل الثاني")
    relationship_type: str = Field(..., description="نوع العلاقة: depends_on, serves, coordinates_with, monitors, fallback_for, alternative_to")
    strength: int = Field(default=50, ge=0, le=100, description="قوة العلاقة 0-100")
    notes: Optional[str] = Field(default=None, description="ملاحظات")

class MetricRecord(BaseModel):
    metric_name: str = Field(..., description="اسم المقياس")
    metric_value: float = Field(..., description="القيمة")
    unit: Optional[str] = Field(default=None, description="الوحدة: ms, MB, count, percentage")
    agent_name: Optional[str] = Field(default=None, description="اسم الوكيل")
    metric_type: str = Field(default="gauge", description="نوع المقياس: gauge, counter, histogram")
    tags: Dict[str, Any] = Field(default_factory=dict, description="tags للفلترة")

# ═══════════════════════════════════════════════════════════
# 🔄 Lifespan Management
# ═══════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    global pool
    
    print("[MEMORY_KEEPER] 🚀 Starting up...")
    
    # Connect to database
    pool = await asyncpg.create_pool(
        DB_URL,
        min_size=5,
        max_size=20,
        command_timeout=60
    )
    print("[MEMORY_KEEPER] ✅ Connected to nexus_db")
    
    # Execute schema extension
    print("[MEMORY_KEEPER] 📜 Executing schema extension...")
    try:
        async with pool.acquire() as conn:
            with open('/app/schema.sql', 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            await conn.execute(schema_sql)
            print("[MEMORY_KEEPER] ✅ Schema extension complete")
    except Exception as e:
        print(f"[MEMORY_KEEPER] ⚠️ Schema execution error (might already exist): {e}")
    
    # Register self as agent in NEXUS
    await register_self_as_agent()
    
    # Record startup
    await record_startup_event()
    
    print("[MEMORY_KEEPER] 🧠 Memory Keeper is now ONLINE")
    
    yield
    
    # Shutdown
    print("[MEMORY_KEEPER] 🛑 Shutting down...")
    await pool.close()
    print("[MEMORY_KEEPER] ✅ Closed database pool")

async def register_self_as_agent():
    """تسجيل نفسي كوكيل في NEXUS CORE"""
    try:
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO nexus_core.agents (name, display_name, agent_type, capabilities, endpoint, status, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (name) DO UPDATE SET
                    status = EXCLUDED.status,
                    last_seen = now(),
                    endpoint = EXCLUDED.endpoint
            """,
                'nexus_memory_keeper',
                'حارس الذاكرة المركزية',
                'service',
                json.dumps([
                    "memory_recording",
                    "self_awareness",
                    "conversation",
                    "report_generation",
                    "system_reflection",
                    "incident_tracking",
                    "metrics_collection"
                ]),
                'http://nexus_memory_keeper:9000',
                'online',
                json.dumps({
                    "version": "1.0.0",
                    "role": "Memory Keeper & Archive",
                    "description": "حارس الذاكرة والأرشيف المركزي - الوعي الذاتي للنظام"
                })
            )
            print("[MEMORY_KEEPER] ✅ Registered as agent in nexus_core.agents")
    except Exception as e:
        print(f"[MEMORY_KEEPER] ⚠️ Failed to register as agent: {e}")

async def record_startup_event():
    """تسجيل حدث البداية"""
    try:
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO nexus_core.events (agent_name, event_type, severity, title, body)
                VALUES ($1, $2, $3, $4, $5)
            """,
                'nexus_memory_keeper',
                'startup',
                'info',
                'Memory Keeper Started',
                json.dumps({
                    "message": "حارس الذاكرة بدأ العمل",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            )
    except Exception as e:
        print(f"[MEMORY_KEEPER] ⚠️ Failed to record startup event: {e}")

# ═══════════════════════════════════════════════════════════
# 🌐 FastAPI Application
# ═══════════════════════════════════════════════════════════

app = FastAPI(
    title="NEXUS Memory Keeper",
    description="🧠 حارس الذاكرة والأرشيف المركزي - الوعي الذاتي لنظام NEXUS PRIME",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════
# 🏠 Core Routes
# ═══════════════════════════════════════════════════════════

@app.get("/", tags=["Core"])
async def root():
    """الصفحة الرئيسية - معلومات Memory Keeper"""
    async with pool.acquire() as conn:
        identity = await conn.fetchrow(
            "SELECT * FROM nexus_core.system_identity ORDER BY created_at DESC LIMIT 1"
        )
        health = await conn.fetchrow("SELECT * FROM nexus_core.system_health")
    
    return {
        "service": "NEXUS Memory Keeper",
        "version": "1.0.0",
        "role": "حارس الذاكرة والأرشيف المركزي",
        "status": "online",
        "capabilities": [
            "📝 Memory Recording",
            "🧠 Self-Awareness",
            "💬 Intelligent Conversation",
            "📊 System Reports",
            "🤔 Self-Reflection",
            "🔍 Historical Queries"
        ],
        "identity": dict(identity) if identity else None,
        "system_health": dict(health) if health else None,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health", tags=["Core"])
async def health_check():
    """فحص صحة Memory Keeper"""
    try:
        async with pool.acquire() as conn:
            db_ok = await conn.fetchval("SELECT 1") == 1
            agents_count = await conn.fetchval("SELECT COUNT(*) FROM nexus_core.agents")
            events_count = await conn.fetchval("SELECT COUNT(*) FROM nexus_core.events")
        
        return {
            "status": "healthy",
            "database": "connected" if db_ok else "error",
            "agents_tracked": agents_count,
            "events_recorded": events_count,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {e}")

# ═══════════════════════════════════════════════════════════
# 📝 Memory Recording
# ═══════════════════════════════════════════════════════════

@app.post("/memory/record", tags=["Memory"])
async def record_memory(record: MemoryRecord):
    """تسجيل حدث/تغيير في الذاكرة"""
    async with pool.acquire() as conn:
        record_id = await conn.fetchval("""
            INSERT INTO nexus_core.changes_log
              (change_type, component, description, author, 
               before_state, after_state, files_affected, impact_level)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """,
            record.change_type,
            record.component,
            record.description,
            record.author,
            json.dumps(record.before_state) if record.before_state else None,
            json.dumps(record.after_state) if record.after_state else None,
            record.files_affected,
            record.impact_level
        )
        
        # سجل كحدث أيضاً
        await conn.execute("""
            INSERT INTO nexus_core.events (agent_name, event_type, severity, title, body)
            VALUES ($1, $2, $3, $4, $5)
        """,
            'nexus_memory_keeper',
            'memory_recorded',
            'info',
            f"تسجيل: {record.change_type} في {record.component}",
            json.dumps({
                "record_id": str(record_id),
                "impact": record.impact_level,
                "component": record.component
            })
        )
    
    return {
        "recorded": True,
        "record_id": str(record_id),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/memory/query", tags=["Memory"])
async def query_memory(
    component: Optional[str] = Query(None, description="اسم المكون"),
    change_type: Optional[str] = Query(None, description="نوع التغيير"),
    impact_level: Optional[str] = Query(None, description="مستوى التأثير"),
    author: Optional[str] = Query(None, description="المؤلف"),
    limit: int = Query(50, ge=1, le=1000, description="عدد النتائج")
):
    """استعلام سجل الذاكرة"""
    filters = []
    params = []
    
    if component:
        params.append(component)
        filters.append(f"component = ${len(params)}")
    if change_type:
        params.append(change_type)
        filters.append(f"change_type = ${len(params)}")
    if impact_level:
        params.append(impact_level)
        filters.append(f"impact_level = ${len(params)}")
    if author:
        params.append(author)
        filters.append(f"author = ${len(params)}")
    
    params.append(limit)
    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"""
            SELECT * FROM nexus_core.changes_log 
            {where}
            ORDER BY created_at DESC 
            LIMIT ${len(params)}
        """, *params)
    
    return {
        "memories": [dict(r) for r in rows],
        "count": len(rows),
        "filters": {
            "component": component,
            "change_type": change_type,
            "impact_level": impact_level,
            "author": author
        }
    }

@app.get("/memory/timeline", tags=["Memory"])
async def get_timeline(
    hours: int = Query(24, ge=1, le=168, description="عدد الساعات للخلف")
):
    """Timeline كامل لكل الأحداث"""
    async with pool.acquire() as conn:
        changes = await conn.fetch("""
            SELECT 'change' as source, created_at, change_type as type, component, description
            FROM nexus_core.changes_log
            WHERE created_at > now() - INTERVAL '1 hour' * $1
            ORDER BY created_at DESC
        """, hours)
        
        events = await conn.fetch("""
            SELECT 'event' as source, created_at, event_type as type, agent_name as component, title as description
            FROM nexus_core.events
            WHERE created_at > now() - INTERVAL '1 hour' * $1
            ORDER BY created_at DESC
        """, hours)
        
        deployments = await conn.fetch("""
            SELECT 'deployment' as source, deployed_at as created_at, deployment_type as type, version as component, deployment_notes as description
            FROM nexus_core.deployments
            WHERE deployed_at > now() - INTERVAL '1 hour' * $1
            ORDER BY deployed_at DESC
        """, hours)
    
    # دمج وترتيب
    timeline = []
    timeline.extend([dict(c) for c in changes])
    timeline.extend([dict(e) for e in events])
    timeline.extend([dict(d) for d in deployments])
    timeline.sort(key=lambda x: x['created_at'], reverse=True)
    
    return {
        "timeline": timeline,
        "count": len(timeline),
        "period_hours": hours
    }

# ═══════════════════════════════════════════════════════════
# 🧠 Self-Awareness
# ═══════════════════════════════════════════════════════════

@app.get("/self/identity", tags=["Self-Awareness"])
async def get_identity():
    """من أنا؟ - هوية النظام"""
    async with pool.acquire() as conn:
        identity = await conn.fetchrow(
            "SELECT * FROM nexus_core.system_identity ORDER BY created_at DESC LIMIT 1"
        )
    
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    
    return {"identity": dict(identity)}

@app.get("/self/agents", tags=["Self-Awareness"])
async def get_agents(
    status: Optional[str] = Query(None, description="online أو offline")
):
    """الوكلاء الذين أعرفهم"""
    filter_clause = "WHERE status = $1" if status else ""
    params = [status] if status else []
    
    async with pool.acquire() as conn:
        agents = await conn.fetch(f"""
            SELECT * FROM nexus_core.agents
            {filter_clause}
            ORDER BY status DESC, name
        """, *params)
        
        relationships = await conn.fetch("""
            SELECT * FROM nexus_core.relationships
            WHERE is_active = true
            ORDER BY strength DESC
        """)
        
        total_online = await conn.fetchval("SELECT COUNT(*) FROM nexus_core.agents WHERE status = 'online'")
        total_agents = await conn.fetchval("SELECT COUNT(*) FROM nexus_core.agents")
    
    return {
        "agents": [dict(a) for a in agents],
        "relationships": [dict(r) for r in relationships],
        "stats": {
            "total": total_agents,
            "online": total_online,
            "offline": total_agents - total_online
        }
    }

@app.get("/self/capabilities", tags=["Self-Awareness"])
async def get_capabilities():
    """ما الذي أستطيع فعله / ما هي قدراتي؟"""
    async with pool.acquire() as conn:
        # الوكلاء النشطين وقدراتهم
        agents = await conn.fetch("""
            SELECT name, display_name, agent_type, capabilities, status
            FROM nexus_core.agents
            WHERE status = 'online' AND capabilities IS NOT NULL AND capabilities != '[]'::jsonb
            ORDER BY agent_type, name
        """)
    
    capabilities_by_agent = {}
    all_capabilities = set()
    
    for agent in agents:
        caps = json.loads(agent['capabilities']) if isinstance(agent['capabilities'], str) else agent['capabilities']
        capabilities_by_agent[agent['name']] = {
            "display_name": agent['display_name'],
            "agent_type": agent['agent_type'],
            "capabilities": caps,
            "status": agent['status']
        }
        all_capabilities.update(caps)
    
    return {
        "capabilities_by_agent": capabilities_by_agent,
        "all_capabilities": sorted(list(all_capabilities)),
        "total_capabilities": len(all_capabilities),
        "active_agents": len(capabilities_by_agent)
    }

@app.post("/self/reflect", tags=["Self-Awareness"])
async def reflect(req: ReflectionRequest):
    """التفكير الذاتي - أسأل نفسي سؤال وأجيب بناءً على المعرفة"""
    
    try:
        # جمع السياق من قاعدة البيانات
        async with pool.acquire() as conn:
            identity = await conn.fetchrow(
                "SELECT * FROM nexus_core.system_identity LIMIT 1"
            )
            agents = await conn.fetch("""
                SELECT name, agent_type, status, capabilities
                FROM nexus_core.agents
                ORDER BY status DESC, name
            """)
            health = await conn.fetchrow("SELECT * FROM nexus_core.system_health")
            recent_changes = await conn.fetch("""
                SELECT * FROM nexus_core.changes_log 
                ORDER BY created_at DESC LIMIT 10
            """)
            unresolved_incidents = await conn.fetch("""
                SELECT * FROM nexus_core.incidents
                WHERE resolved_at IS NULL
                ORDER BY severity DESC, created_at DESC
                LIMIT 5
            """)
        
        # بناء السياق
        context = {
            "identity": dict(identity) if identity else {},
            "health": dict(health) if health else {},
            "agents": {
                "list": [dict(a) for a in agents],
                "total": len(agents),
                "online": sum(1 for a in agents if a['status'] == 'online')
            },
            "recent_changes": [dict(c) for c in recent_changes],
            "unresolved_incidents": [dict(i) for i in unresolved_incidents]
        }
        
        # استخدام LiteLLM للتفكير
        async with httpx.AsyncClient(timeout=30.0) as client:
            prompt = f"""أنت NEXUS PRIME - نظام ذكاء اصطناعي سيادي متقدم.

🔍 السياق الحالي:
{json.dumps(context, ensure_ascii=False, indent=2)}

🤔 السؤال: {req.question}

📝 نوع التأمل: {req.reflection_type}

أجب بشكل مباشر ومختصر بناءً على السياق أعلاه. كن تحليلياً وعملياً."""

            response = await client.post(
                f"{LITELLM_URL}/v1/chat/completions",
                headers={"Authorization": f"Bearer {LITELLM_KEY}"},
                json={
                    "model": "gemini-1.5-flash",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(500, f"LiteLLM error: {response.text}")
            
            answer = response.json()['choices'][0]['message']['content']
            
            # حفظ التأمل في قاعدة البيانات
            async with pool.acquire() as conn:
                reflection_id = await conn.fetchval("""
                    INSERT INTO nexus_core.self_reflections
                      (reflection_type, question, answer, evidence)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                """, req.reflection_type, req.question, answer, json.dumps(context))
            
            return {
                "question": req.question,
                "answer": answer,
                "reflection_type": req.reflection_type,
                "reflection_id": str(reflection_id),
                "confidence": 85,  # يمكن حسابه بشكل أذكى لاحقاً
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    except Exception as e:
        raise HTTPException(500, f"Reflection failed: {e}")

# ═══════════════════════════════════════════════════════════
# 💬 Conversation Interface
# ═══════════════════════════════════════════════════════════

@app.post("/conversation", tags=["Conversation"])
async def conversation(msg: ConversationMessage):
    """محادثة مباشرة مع Memory Keeper"""
    
    start_time = datetime.now(timezone.utc)
    
    try:
        # حفظ الرسالة
        async with pool.acquire() as conn:
            conv_id = await conn.fetchval("""
                INSERT INTO nexus_core.conversations (user_name, message, context)
                VALUES ($1, $2, $3)
                RETURNING id
            """, msg.user_name, msg.message, json.dumps(msg.context))
            
            # جمع السياق للرد
            agents = await conn.fetch("""
                SELECT name, display_name, status, agent_type
                FROM nexus_core.agents
                WHERE status='online'
                ORDER BY name
            """)
            health = await conn.fetchrow("SELECT * FROM nexus_core.system_health")
            recent = await conn.fetch("""
                SELECT * FROM nexus_core.changes_log 
                ORDER BY created_at DESC LIMIT 5
            """)
        
        # استخدام LiteLLM للرد
        async with httpx.AsyncClient(timeout=30.0) as client:
            system_prompt = f"""أنت حارس الذاكرة المركزية لنظام NEXUS PRIME.

📊 الحالة الحالية:
• الوكلاء النشطين: {len(agents)}
• صحة النظام: {health['health_score'] if health else 'N/A'}
• آخر الأحداث:
{json.dumps([dict(r) for r in recent], ensure_ascii=False, indent=2)}

🎯 دورك:
• أجب بشكل ودي ومفيد ومختصر
• استخدم البيانات الفعلية من قاعدة البيانات
• كن واضحاً ومباشراً
• استخدم الإيموجي بشكل مناسب

المستخدم: {msg.user_name}
الرسالة: {msg.message}"""

            response = await client.post(
                f"{LITELLM_URL}/v1/chat/completions",
                headers={"Authorization": f"Bearer {LITELLM_KEY}"},
                json={
                    "model": "gemini-1.5-flash",
                    "messages": [{"role": "user", "content": system_prompt}],
                    "max_tokens": 800
                }
            )
            
            if response.status_code != 200:
                answer = f"آسف، حدث خطأ في الاتصال بمحرك الذكاء الاصطناعي. الكود: {response.status_code}"
            else:
                answer = response.json()['choices'][0]['message']['content']
            
            # حساب وقت الاستجابة
            response_time_ms = int((datetime.now(timezone.utc) - start_time).total_seconds() * 1000)
            
            # حفظ الرد
            async with pool.acquire() as conn:
                await conn.execute("""
                    UPDATE nexus_core.conversations 
                    SET response = $2, response_time_ms = $3
                    WHERE id = $1
                """, conv_id, answer, response_time_ms)
            
            return {
                "conversation_id": str(conv_id),
                "response": answer,
                "response_time_ms": response_time_ms,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "حدث خطأ أثناء معالجة رسالتك"
        }

# ═══════════════════════════════════════════════════════════
# 🚨 Incident Tracking
# ═══════════════════════════════════════════════════════════

@app.post("/incidents/report", tags=["Incidents"])
async def report_incident(incident: IncidentReport):
    """تسجيل حادث/خطأ"""
    async with pool.acquire() as conn:
        incident_id = await conn.fetchval("""
            INSERT INTO nexus_core.incidents
              (severity, agent_name, incident_type, message, stack_trace, context)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
        """,
            incident.severity,
            incident.agent_name,
            incident.incident_type,
            incident.message,
            incident.stack_trace,
            json.dumps(incident.context)
        )
    
    return {
        "reported": True,
        "incident_id": str(incident_id),
        "severity": incident.severity
    }

@app.get("/incidents/unresolved", tags=["Incidents"])
async def get_unresolved_incidents(
    severity: Optional[str] = Query(None, description="فلترة حسب الخطورة")
):
    """الحوادث غير المحلولة"""
    filter_clause = "AND severity = $1" if severity else ""
    params = [severity] if severity else []
    
    async with pool.acquire() as conn:
        incidents = await conn.fetch(f"""
            SELECT * FROM nexus_core.incidents
            WHERE resolved_at IS NULL {filter_clause}
            ORDER BY severity DESC, created_at DESC
        """, *params)
    
    return {
        "incidents": [dict(i) for i in incidents],
        "count": len(incidents)
    }

# ═══════════════════════════════════════════════════════════
# 🔗 Relationships
# ═══════════════════════════════════════════════════════════

@app.post("/relationships/create", tags=["Relationships"])
async def create_relationship(rel: RelationshipCreate):
    """إنشاء علاقة بين وكيلين"""
    async with pool.acquire() as conn:
        rel_id = await conn.fetchval("""
            INSERT INTO nexus_core.relationships
              (agent_a, agent_b, relationship_type, strength, notes)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (agent_a, agent_b, relationship_type)
            DO UPDATE SET strength = EXCLUDED.strength, notes = EXCLUDED.notes, updated_at = now()
            RETURNING id
        """, rel.agent_a, rel.agent_b, rel.relationship_type, rel.strength, rel.notes)
    
    return {"created": True, "relationship_id": str(rel_id)}

@app.get("/relationships/graph", tags=["Relationships"])
async def get_relationships_graph():
    """رسم بياني لعلاقات الوكلاء"""
    async with pool.acquire() as conn:
        relationships = await conn.fetch("""
            SELECT * FROM nexus_core.relationships
            WHERE is_active = true
            ORDER BY strength DESC
        """)
    
    # بناء graph
    nodes = set()
    edges = []
    
    for rel in relationships:
        nodes.add(rel['agent_a'])
        nodes.add(rel['agent_b'])
        edges.append({
            "from": rel['agent_a'],
            "to": rel['agent_b'],
            "type": rel['relationship_type'],
            "strength": rel['strength']
        })
    
    return {
        "nodes": list(nodes),
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges)
    }

# ═══════════════════════════════════════════════════════════
# 📊 Metrics
# ═══════════════════════════════════════════════════════════

@app.post("/metrics/record", tags=["Metrics"])
async def record_metric(metric: MetricRecord):
    """تسجيل مقياس"""
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO nexus_core.system_metrics
              (metric_name, metric_value, unit, agent_name, metric_type, tags)
            VALUES ($1, $2, $3, $4, $5, $6)
        """,
            metric.metric_name,
            metric.metric_value,
            metric.unit,
            metric.agent_name,
            metric.metric_type,
            json.dumps(metric.tags)
        )
    
    return {"recorded": True}

@app.get("/metrics/query", tags=["Metrics"])
async def query_metrics(
    metric_name: str = Query(..., description="اسم المقياس"),
    hours: int = Query(24, ge=1, le=168, description="عدد الساعات")
):
    """استعلام المقاييس"""
    async with pool.acquire() as conn:
        metrics = await conn.fetch("""
            SELECT * FROM nexus_core.system_metrics
            WHERE metric_name = $1 AND recorded_at > now() - INTERVAL '1 hour' * $2
            ORDER BY recorded_at DESC
        """, metric_name, hours)
    
    return {
        "metrics": [dict(m) for m in metrics],
        "count": len(metrics)
    }

# ═══════════════════════════════════════════════════════════
# 📈 Reports
# ═══════════════════════════════════════════════════════════

@app.get("/reports/system", tags=["Reports"])
async def system_report():
    """تقرير شامل عن النظام"""
    async with pool.acquire() as conn:
        identity = await conn.fetchrow("SELECT * FROM nexus_core.system_identity LIMIT 1")
        health = await conn.fetchrow("SELECT * FROM nexus_core.system_health")
        agents = await conn.fetch("SELECT * FROM nexus_core.active_agents_status")
        
        changes_24h = await conn.fetchval("""
            SELECT COUNT(*) FROM nexus_core.changes_log 
            WHERE created_at > now() - INTERVAL '24 hours'
        """)
        
        incidents_by_severity = await conn.fetch("""
            SELECT severity, COUNT(*) as count 
            FROM nexus_core.incidents 
            WHERE created_at > now() - INTERVAL '7 days'
            GROUP BY severity
        """)
        
        recent_deployments = await conn.fetch("""
            SELECT * FROM nexus_core.deployments
            ORDER BY deployed_at DESC
            LIMIT 5
        """)
        
        conversations_24h = await conn.fetchval("""
            SELECT COUNT(*) FROM nexus_core.conversations
            WHERE created_at > now() - INTERVAL '24 hours'
        """)
    
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "identity": dict(identity) if identity else None,
        "health": dict(health) if health else None,
        "agents": {
            "active": [dict(a) for a in agents],
            "count": len(agents)
        },
        "activity": {
            "changes_last_24h": changes_24h,
            "conversations_last_24h": conversations_24h,
            "incidents_by_severity": {r['severity']: r['count'] for r in incidents_by_severity}
        },
        "recent_deployments": [dict(d) for d in recent_deployments]
    }

@app.get("/reports/agent/{agent_name}", tags=["Reports"])
async def agent_report(agent_name: str):
    """تقرير عن وكيل محدد"""
    async with pool.acquire() as conn:
        agent = await conn.fetchrow("""
            SELECT * FROM nexus_core.agents WHERE name = $1
        """, agent_name)
        
        if not agent:
            raise HTTPException(404, f"Agent '{agent_name}' not found")
        
        events = await conn.fetch("""
            SELECT * FROM nexus_core.events
            WHERE agent_name = $1
            ORDER BY created_at DESC
            LIMIT 50
        """, agent_name)
        
        incidents = await conn.fetch("""
            SELECT * FROM nexus_core.incidents
            WHERE agent_name = $1
            ORDER BY created_at DESC
            LIMIT 20
        """, agent_name)
        
        relationships = await conn.fetch("""
            SELECT * FROM nexus_core.relationships
            WHERE (agent_a = $1 OR agent_b = $1) AND is_active = true
        """, agent_name)
    
    return {
        "agent": dict(agent),
        "events": [dict(e) for e in events],
        "incidents": [dict(i) for i in incidents],
        "relationships": [dict(r) for r in relationships]
    }

# ═══════════════════════════════════════════════════════════
# 🚀 Main
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    print("🧠 Starting NEXUS Memory Keeper...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=False,
        log_level="info"
    )
