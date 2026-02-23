# Sovereign Command Center — Ports & Services Matrix

## Port Allocation (No Conflicts)

| Port | Service | Container | Role |
|------|---------|-----------|------|
| 3000 | Open WebUI | nexus_ai | AI Chat (8080→3000) |
| 4000 | LiteLLM | nexus_litellm | LLM Proxy |
| 5050 | Edge-TTS | nexus_voice | Voice (8000→5050) |
| 5678 | n8n | nexus_flow | Workflow automation |
| 6379 | Redis | nexus_redis | Event bus |
| 7777 | Apex | nexus_apex | Command layer (override only, localhost) |
| 8002 | Shadow7 | shadow7_api | Publisher API |
| 8003 | Auth | nexus_auth | RS256 Auth |
| 8090 | Cortex | nexus_cortex | Central neural |
| 8100 | Oracle | nexus_oracle | RAG documentation |
| 8200 | Nerve | nexus_nerve | Central nervous system |
| 8300 | Neural Spine | neural_spine | Cognitive backbone (override) |
| 8501 | Boardroom | nexus_boardroom | Cognitive boardroom |
| 8888 | **Dify Bridge** | **sovereign_dify_bridge** | **Sovereign OS Dashboard** (sovereign/god.mrf103.com) |
| 9000 | Memory Keeper | nexus_memory_keeper | حارس الذاكرة |
| 9001 | Memory Keeper UI | nexus_memory_keeper | Web UI |
| 9999 | **Gateway** | **sovereign_gateway** | **AS-SULTAN unified bridge** (gateway.mrf103.com) |
| 8085 | **Dify** | dify-nginx | Dify platform (dify.mrf103.com) |
| 50051 | Orchestrator | nexus_orchestrator | gRPC meta-orchestrator |
| 11434 | Ollama | nexus_ollama | Local LLM |
| 5001 | Dashboard | nexus_dashboard | Nexus dashboard |

## Sovereign Stack Startup Order

1. **nexus_db** (healthcheck: pg_isready)
2. **nexus_redis**, **nexus_ollama**
3. **nexus_litellm**, **nexus_cortex**, **nexus_memory_keeper**, **nexus_oracle**
4. **nexus_nerve**
5. **sovereign_dify_bridge** (depends_on: nexus_db healthy)
6. **sovereign_gateway** (depends_on: nexus_nerve, sovereign_dify_bridge)

## MSL Schema Prerequisite

Before full operation (Bridge hormonal/ledger/Eve), apply MSL schema once:

```bash
./scripts/db/apply_msl_schema.sh
```

Requires `nexus_db` running. Re-run safe (shows "already exists" if applied).

## Deployment Commands

```bash
# Full Sovereign stack (recommended)
./scripts/sovereign_launch.sh

# With MSL schema first
./scripts/sovereign_launch.sh --msl

# Minimal (bridge + gateway + deps only)
./scripts/sovereign_launch.sh --minimal
```

## Optional Services (docker-compose.override.yml)

Add `-f docker-compose.override.yml` for:
- **nexus_apex** (7777) — Apex command layer
- **neural_spine** (8300) — Cognitive backbone
- **reflex_agents** — Agent runtime
