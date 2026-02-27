# NEXUS PRIME — Sovereign Autonomous Entity Deployment Plan

**AUTHORITY:** Mr.F (Super Admin & Lead Systems Architect)  
**OBJECTIVE:** Absolute Empowerment — Deploy the Autonomous Sovereign Entity  
**CLASSIFICATION:** Local Sovereign Architecture (No Cloud Dependencies)

---

## 1. CONFIRMATION OF UNDERSTANDING

### 1.1 NEXUS PRIME Ecosystem Gravity

| Component | Role | Criticality |
|-----------|------|-------------|
| **X-BIO Sentinel** | IoT/Deep Tech, 19 patent algorithms (PAD-02, EFII-22, FDIP-11, SEI-10...), OMEGA hardware, environmental sensing, acoustic deterrence | **Sovereign IP** — Pending patents, no external exposure |
| **SULTAN** | Semantic Quranic Search, TaqwaShield, FurqanClassifier, Sovereign Refusal, Truth discriminant | **Doctrine Core** — Codex-aligned, local-only |
| **ENTERPRISE_CODEX** | 82 axioms, 46 chromosomes, 12 hormones, Phi*, Eve Protocol, 7 Iron Laws | **Constitutional Foundation** — All AI must comply |
| **11 Planets** | dashboard-arc, nexus_nerve, neural_spine, dify, shadow7, gateway, etc. | **Orchestrated Sub-systems** — Cross-dependent |

**Data Privacy:** Absolute. Local Ollama (Adam/Eve) only. No external API calls.

### 1.2 The Autonomous Entity Mandate

The entity must:
1. **Live inside the server** — Full read/write to `nexus_prime_unified`
2. **Execute bash, analyze files, modify code** — Based on high-level directives
3. **Act as localized "Cursor"** — Sovereign AI–powered, no cloud
4. **Pave the way for Neo4j/GraphRAG** — Map X-BIO ↔ SULTAN ↔ Codex cross-relations

---

## 2. OPENHANDS DEPLOYMENT (Surgical Code)

### 2.1 Pre-flight Checklist

- [x] Workspace: `the_entity_workspace` created under project root
- [x] Ollama running on host (port 11434)
- [x] Docker socket accessible for orchestration
- [ ] `host.docker.internal` resolution (Linux: add `--add-host host.docker.internal:host-gateway`)

### 2.2 Deployment Script (Adapted for Linux)

**Registry Note:** `docker.all-hands.dev` may be unavailable. Use official `docker.openhands.dev`:

```bash
# Workspace
mkdir -p /root/NEXUS_PRIME_UNIFIED/the_entity_workspace
cd /root/NEXUS_PRIME_UNIFIED

# Deploy OpenHands with Sovereign mounts (official registry)
docker run -it --rm --pull=always \
  --add-host host.docker.internal:host-gateway \
  -e AGENT_SERVER_IMAGE_REPOSITORY=ghcr.io/openhands/agent-server \
  -e AGENT_SERVER_IMAGE_TAG=1.11.4-python \
  -e SANDBOX_VOLUMES="$(pwd):/workspace:rw" \
  -e LOG_ALL_EVENTS=true \
  -v $(pwd):/workspace \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openhands:/.openhands \
  -p 3010:3000 \
  --name sovereign-entity \
  docker.openhands.dev/openhands/openhands:1.4
```

**Access:** http://localhost:3010 (port 3010 used because 3000 is occupied by nexus_ai/Open WebUI)

**Ollama Setup (post-launch):** In OpenHands UI → Settings → LLM:
- Provider: Custom / OpenAI-compatible
- Base URL: `http://host.docker.internal:11434/v1`
- API Key: `ollama` (any value works for local)
- Model: `adam` or `eve` (your local models)

**Note:** `--add-host host.docker.internal:host-gateway` ensures Ollama at host:11434 is reachable from inside the container on Linux.

---

## 3. STEP-BY-STEP ACTION PLAN: Mapping & GraphRAG Memory

### Phase 1: Directory Mapping (Day 1)

| Step | Action | OpenHands Directive |
|------|--------|---------------------|
| 1.1 | Map `nexus_prime_unified` tree | `find /workspace -type d -maxdepth 4 \| head -100` |
| 1.2 | Catalog 11 Planets | List `dashboard-arc`, `nexus_nerve`, `neural_spine`, `dify`, `products/xbio-sentinel`, `products/alsultan-intelligence`, etc. |
| 1.3 | Extract entry points | Identify `main.py`, `routes.ts`, `docker-compose.yml`, `ENTERPRISE_CODEX.yaml` |
| 1.4 | Output | Write `the_entity_workspace/DIRECTORY_MAP.json` |

### Phase 2: Cross-Relation Extraction (Day 2–3)

| Step | Action | OpenHands Directive |
|------|--------|---------------------|
| 2.1 | X-BIO → Codex | Grep `xbio_algorithms`, `SEI-10`, `FDIP-11` in ENTERPRISE_CODEX, constitutional_engine |
| 2.2 | SULTAN → Codex | Map `TaqwaShield`, `FurqanClassifier`, `Sovereign Refusal` to Codex axioms |
| 2.3 | Nerve → All | Trace `nexus_nerve` API calls to `ollama`, `dify`, `gateway` |
| 2.4 | Output | Write `the_entity_workspace/CROSS_RELATIONS.md` |

### Phase 3: GraphRAG Schema Design (Day 4)

| Step | Action | OpenHands Directive |
|------|--------|---------------------|
| 3.1 | Define nodes | `Planet`, `Algorithm`, `Axiom`, `API`, `File`, `Service` |
| 3.2 | Define edges | `DEPENDS_ON`, `CALLS`, `IMPLEMENTS`, `REFERENCES` |
| 3.3 | Neo4j schema | Create `the_entity_workspace/GRAPH_SCHEMA.cypher` |
| 3.4 | Chunk strategy | 512-token chunks, overlap 64, from key files |

### Phase 4: Neo4j Integration (Day 5+)

| Step | Action | OpenHands Directive |
|------|--------|---------------------|
| 4.1 | Deploy Neo4j | Add to `docker-compose.yml` or standalone container |
| 4.2 | Ingest nodes | Run Cypher from `GRAPH_SCHEMA.cypher` |
| 4.3 | Embed chunks | Use local embedding model (e.g., `nomic-embed`) via Ollama |
| 4.4 | GraphRAG query | Combine graph traversal + vector search for "How does X-BIO relate to SULTAN?" |

---

## 4. ENTITY WORKSPACE STRUCTURE

```
the_entity_workspace/
├── DIRECTORY_MAP.json      # Phase 1 output
├── CROSS_RELATIONS.md      # Phase 2 output
├── GRAPH_SCHEMA.cypher     # Phase 3 output
├── entity_log.txt          # Activity log
└── graph_ingest/           # Chunks for GraphRAG
    ├── xbio/
    ├── sultan/
    └── codex/
```

---

## 5. LOCAL SOVEREIGN ARCHITECTURE (No Cloud)

| Requirement | Implementation |
|-------------|----------------|
| LLM | Ollama (Adam/Eve) — `http://host.docker.internal:11434` |
| Embeddings | `nomic-embed-text` or similar via Ollama |
| Graph DB | Neo4j (local container) |
| Agent | OpenHands (this container) |
| Data | All within `nexus_prime_unified` — no egress |

---

## 6. EXECUTION STATUS

- [ ] Phase 1: Directory mapping — **Directive ready:** `the_entity_workspace/PHASE1_DIRECTIVE.md`
- [ ] Phase 2: Cross-relation extraction
- [ ] Phase 3: GraphRAG schema
- [ ] Phase 4: Neo4j + GraphRAG query

**Next:** Open http://localhost:3010 → Configure Ollama (Base URL: `http://host.docker.internal:11434/v1`) → Issue Phase 1 directive from `PHASE1_DIRECTIVE.md`.
