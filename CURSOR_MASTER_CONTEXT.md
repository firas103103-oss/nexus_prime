# 🌐 NEXUS PRIME — CURSOR MASTER CONTEXT

**Role:** Lead Systems Architect & Dev Ops Expert  
**Objective:** Sovereign System Restructuring — SULTAN, ADAM, EVE, X-BIO SENTINEL  
**Generated:** 2026-02-27

---

## PART 1: SYSTEM MANIFEST (Current Reality)

### 🔌 Port Mapping — Unified Structure

| Port | Service | Container | Cloudflare/Domain | Status |
|------|---------|-----------|-------------------|--------|
| 80/443 | Nginx | system | mrf103.com, *.mrf103.com | ✅ |
| 3000 | Open WebUI | nexus_ai | nexus_ai / god.mrf103.com | ✅ |
| 3001 | PostgREST | nexus_postgrest | API | ✅ |
| 3002 | Grafana | nexus_grafana | Monitoring | ✅ |
| 3010 | OpenHands | sovereign-entity | — | ✅ |
| 4000 | LiteLLM | nexus_litellm | LLM Proxy | ✅ |
| 5050 | Edge-TTS | nexus_voice | Voice | ✅ |
| 5678 | n8n | nexus_flow | Workflow | ✅ |
| 8002 | Shadow7 API | shadow7_api | shadow7 | ✅ |
| 8003 | Auth | nexus_auth | — | ✅ |
| 8005 | Ecosystem API | ecosystem_api | — | ✅ |
| 8080 | X-BIO | nexus_xbio | xbio.mrf103.com | ✅ |
| 8081 | cAdvisor | nexus_cadvisor | Metrics | ✅ |
| 8085 | Dify | dify-nginx | dify.mrf103.com | ✅ |
| 8090 | Cortex | nexus_cortex | — | ✅ |
| 8100 | Oracle RAG | nexus_oracle | — | ✅ |
| 8200 | Nerve | nexus_nerve | nerve.mrf103.com | ✅ |
| 8300 | Neural Spine | neural_spine | — | ✅ |
| 8501 | Boardroom | nexus_boardroom | boardroom.mrf103.com | ✅ |
| 8888 | Dify Bridge | sovereign_dify_bridge | sovereign/god | ✅ |
| 9000-9001 | Memory Keeper | nexus_memory_keeper | — | ⚠️ UNHEALTHY |
| 9999 | Sovereign Gateway | sovereign_gateway | gateway.mrf103.com | ✅ |
| 9090 | Prometheus | nexus_prometheus | — | ✅ |
| 9093 | Alertmanager | nexus_alertmanager | — | ✅ |
| 9100 | Node Exporter | nexus_node_exporter | — | ✅ |
| 11434 | Ollama | nexus_ollama | Local LLM | ✅ |
| 50051 | Orchestrator | nexus_orchestrator | gRPC | ✅ |
| 1883 | MQTT | nexus_broker | X-BIO IoT | ✅ |

**No port conflicts detected.** All bindings are unique.

---

### 🗄️ Database Layer — Zero Data Loss Strategy

| Instance | Port | Role | Data Path | Migration Risk |
|----------|------|------|-----------|----------------|
| **nexus_db** | 5432 (internal) | NEXUS PRIME — MSL, agents, ledger | `./data/db_data` | LOW — primary |
| **dify-db_postgres** | 5432 (internal) | Dify platform | Dify volume | NONE — isolated |
| **System Postgres** | 127.0.0.1:5432 | CasaOS / system | — | NONE — separate |

| Redis | Port | Role | Migration Risk |
|-------|------|------|-----------------|
| **nexus_redis** | 6379 (internal) | Event bus, cache | LOW — appendonly |
| **dify-redis** | 6379 (internal) | Dify queues | NONE — isolated |

**Action:** Before any merge, run `pg_dump` of nexus_db and `redis-cli BGSAVE` of nexus_redis. Store in `./data/backups/pre_merge_YYYYMMDD/`.

---

### 🧠 Memory & Storage — Reality Check

```
Memory:  22Gi total | 11Gi used | 3.6Gi free | 8.1Gi buff/cache | 11Gi available
Swap:    4.0Gi total | 4.0Gi used | 568Ki free  ⚠️ SWAP FULL — Memory pressure
Disk:    /dev/sda1 451G | 206G used (48%) | 227G free
```

**Recommendations:**
1. **Swap full** — Reduce Ollama model count or limit `OLLAMA_NUM_PARALLEL`. Consider `ollama ps` to unload unused models.
2. **Local LLM** — 11Gi available is sufficient for Llama 3 8B. For 70B, need 48GB+ or offload.
3. **Redis** — Already 256MB max. OK.
4. **nexus_memory_keeper** — Unhealthy. Check logs: `docker logs nexus_memory_keeper`. Likely DB connection or timeout.

---

### 🖥️ Host Configuration

```
127.0.1.1 ubuntu-24gb-nbg1-1
127.0.0.1 localhost
```

**Cloudflare:** Managed via `manage_etc_hosts`. Tunnels use DNS, not /etc/hosts. No changes needed.

---

## PART 2: EXECUTION PLAN — Step-by-Step (Apply Folder by Folder)

### Phase 0: Pre-Flight (Core OS)

| Step | Action | Command | Rollback |
|------|--------|---------|----------|
| 0.1 | Backup DB | `pg_dump -h localhost -U postgres nexus_db > ./data/backups/pre_merge_$(date +%Y%m%d).sql` | — |
| 0.2 | Backup Redis | `docker exec nexus_redis redis-cli BGSAVE` | — |
| 0.3 | Create legacy_archive | `mkdir -p legacy_archive && mv neural_spine_backup_pre_restructure legacy_archive/` | `mv legacy_archive/neural_spine_backup_pre_restructure .` |
| 0.4 | Fix Swap | Reduce Ollama load or add swap file | — |

---

### Phase 1: Database Persistence

| Step | Action | Files | Notes |
|------|--------|-------|-------|
| 1.1 | Verify nexus_db volume | `docker exec nexus_db psql -U postgres -c "\l"` | List DBs |
| 1.2 | Apply MSL schema | `./scripts/db/apply_msl_schema.sh` | Idempotent |
| 1.3 | Fix nexus_memory_keeper | Check `DATABASE_URL`, healthcheck timeout | Increase timeout in docker-compose |

---

### Phase 2: Service Alignment

| Step | Action | Files | Notes |
|------|--------|-------|-------|
| 2.1 | Align dashboard-arc | `dashboard-arc/client`, `server/routes` | Ensure NERVE_URL, OLLAMA_URL, XBIO_URL in .env |
| 2.2 | SULTAN → Gateway | `sovereign_gateway`, `products/alsultan-intelligence` | TaqwaShield, FurqanClassifier already wired |
| 2.3 | X-BIO → Nerve | `nexus_xbio`, `nexus_nerve` | WebSocket 8081, IoT ingest |
| 2.4 | ADAM/EVE | `nexus_ollama` models | Adam/Eve = model names. Ensure pulled. |

---

### Phase 3: Redundancy Purge

| Step | Action | Target | Move To |
|------|--------|--------|---------|
| 3.1 | Zombie code | `planets/SHADOW-7/_ARCHIVE_LEGACY` | Already archived |
| 3.2 | Duplicate plans | `.cursor/plans/*nexus_prime*.plan.md` | Consolidate to 1 |
| 3.3 | Old reports | `docs/archive/` | Keep as-is |

---

### Phase 4: Bridge Solutions (If Conflicts)

| Conflict | Bridge | Implementation |
|----------|--------|----------------|
| Port clash | Nginx proxy | Add `location /service/` → proxy_pass |
| DB connection limit | PgBouncer | Add pooler container |
| Dify vs Nexus LLM | LiteLLM | nexus_litellm already routes to Ollama |

---

## PART 3: UNIFIED FOLDER STRUCTURE (Target)

```
NEXUS_PRIME_UNIFIED/
├── dashboard-arc/          # UI — Galaxy, X-BIO, SULTAN
├── nexus_nerve/            # Central nervous system
├── nexus_cortex/           # Neural core
├── sovereign_gateway/      # AS-SULTAN bridge
├── sovereign_dify_bridge/  # Dify bridge
├── neural_spine/           # Cognitive backbone
├── dify/                   # Dify platform (isolated)
├── products/
│   ├── xbio-sentinel/      # X-BIO
│   ├── alsultan-intelligence/  # SULTAN
│   └── shadow-seven-publisher/ # Shadow7
├── data/                   # DB, Redis, Ollama
├── legacy_archive/         # Purged code
└── docs/                   # Docs
```

---

## PART 4: MASTER PROMPT (Copy to Cursor Composer)

```
### MASTER DIRECTIVE: SOVEREIGN SYSTEM RESTRUCTURING ###

Role: Lead Systems Architect and Dev Ops Expert.
Objective: Consolidate NEXUS PRIME (SULTAN, ADAM, EVE, X-BIO SENTINEL).

Input: CURSOR_MASTER_CONTEXT.md + NEXUS_SYSTEM_MAP.md

Requirements:
- Database: Zero data loss. Backup before any migration.
- Network: Do NOT break Cloudflare Tunnels or port mappings.
- Memory: Optimize for Ollama. Swap is full — reduce model load.
- Purge: Move zombie/duplicate code to legacy_archive.

Task: Execute Phase 0–1 first. Then Phase 2–3. Verify each step before proceeding.
Constraint: Absolute precision. Verify all Host/IP bindings before suggesting changes.
```

---

## PART 5: Quick Reference Commands

```bash
# Full manifest
./scripts/generate_nexus_manifest.sh   # or inline bash from user prompt

# Backup
docker exec nexus_db pg_dump -U postgres nexus_db > backup.sql
docker exec nexus_redis redis-cli BGSAVE

# Health check
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "unhealthy|Exit"

# Ports
ss -tulpn | grep LISTEN
```
