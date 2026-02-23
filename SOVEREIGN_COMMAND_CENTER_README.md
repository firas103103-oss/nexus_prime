# Sovereign Command Center — God Mode & God Creation Center

**Imperial Directive:** Transform Dify into the ultimate God Mode & God Creation Center, unified with MSL, cognitive_bridge, and X-BIO Sentinel.

**Status:** ✅ DEPLOYED — Bridge running on port 8888, Gateway proxy on 9999.

---

## Architecture

```
MSL (signal_molecules) ──► Hormonal Orchestrator ──► Dify Workflows
MSL (genomes) ──────────► Genome Mapper ──────────► LiteLLM params (temp, top_p)
MSL (action_ledger) ◄─── Raqib/Atid ────────────── Every Dify trigger
X-BIO (VOC/Anomaly) ───► Webhook ─────────────────► Dify + action_ledger
EVE Protocol ──────────► Fractal Polarization ────► AS-SULTAN → EVE (estrogen-dominant)
```

---

## Prerequisites

**MSL Schema** — The bridge requires `msl` schema (entities, genomes, signal_molecules, action_ledger). Apply once:

```bash
./scripts/db/apply_msl_schema.sh
# Or: docker exec -i nexus_db psql -U postgres -d nexus_db < scripts/db/msl_schema.sql
```

See `SOVEREIGN_PORTS_AND_SERVICES.md` for full port matrix and startup order.

---

## Deployment

### 1. Sovereign Dify Bridge (Standalone)

```bash
cd /root/NEXUS_PRIME_UNIFIED
docker compose -f docker-compose.yml -f docker-compose.dify.yml up -d sovereign_dify_bridge
```

The bridge runs on **port 8888** and provides:
- Hormonal status (`/api/hormonal/status`)
- Genome → LLM params (`/api/genome/entity/{id}/llm-params`)
- Raqib/Atid ledger (`/api/ledger/recent`)
- Ledger notifications (`/api/ledger/notifications`) — UI sync
- **Eve Protocol** (`POST /api/eve/create`) — Fractal Polarization
- **System Status** (`/api/systems/status`) — Nerve, Gateway, Oracle, Memory Keeper
- X-BIO VOC webhook (`POST /api/xbio/voc-webhook`)
- APEX Control Interface (`/`) — Sovereign OS Dashboard

### 2. Full Stack (with Gateway)

```bash
docker compose -f docker-compose.yml -f docker-compose.dify.yml up -d
```

Gateway (9999) proxies to the bridge when `DIFY_BOARDROOM_ENABLED=true`:
- `GET /api/dify/god-mode` — God Mode Dashboard
- `GET /api/dify/hormonal/status`
- `GET /api/dify/ledger/recent`
- `GET /api/dify/genome/entity/{id}/llm-params`
- `POST /api/dify/xbio/voc-webhook`

### 3. Dify (Optional)

To connect the bridge to Dify workflows:

1. Clone Dify: `git clone https://github.com/langgenius/dify.git && cd dify/docker`
2. Copy env: `cp .env.example .env`
3. Set `OPENAI_API_BASE=http://nexus_litellm:4000/v1` and `OPENAI_API_KEY=sk-nexus-sovereign-mrf103`
4. Connect to `nexus_network` or set `DIFY_API_URL` in bridge env
5. Create a "Defensive" workflow in Dify with inputs: `entity_name`, `trigger_reason`, `cortisol`, `adrenaline`, `mood`
6. Set `DIFY_API_KEY` and `DIFY_DEFENSIVE_WORKFLOW_ID` in bridge env

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DIFY_API_URL` | Dify API base URL | `http://dify_api:5001` |
| `DIFY_API_KEY` | Dify app API key | (empty) |
| `DIFY_DEFENSIVE_WORKFLOW_ID` | Workflow ID for hormonal triggers | (empty) |
| `CORTISOL_SPIKE_THRESHOLD` | Trigger defensive workflow when cortisol ≥ | 0.6 |
| `ADRENALINE_SPIKE_THRESHOLD` | Trigger when adrenaline ≥ | 0.5 |
| `HORMONAL_POLL_INTERVAL_SEC` | Poll interval for signal_molecules | 10 |
| `XBIO_WEBHOOK_SECRET` | Secret for X-BIO webhook | `nexus_xbio_sentinel` |

---

## Genome-Driven Agent Creation

82 Traits × 46 Chromosomes map to LLM parameters:

- **Creativity 0.9** → `temperature` ↑, `top_p` ↑
- **Compliance/Alignment high** → `temperature` ↓ (conservative)
- **Cognition high** → precise, lower variance

Example:
```bash
curl http://localhost:8888/api/genome/entity/AS-SULTAN/llm-params
```

---

## X-BIO Bio-Olfactory Loop

POST to webhook when VOC/anomaly detected:

```bash
curl -X POST http://localhost:8888/api/xbio/voc-webhook \
  -H "Content-Type: application/json" \
  -H "X-XBIO-Secret: nexus_xbio_sentinel" \
  -d '{"sensor_id":"xbio-01","voc_level":0.75,"anomaly_score":0.9}'
```

When `anomaly_score >= 0.8`, the bridge logs to `msl.action_ledger` (Raqib).

---

## Eve Protocol (Fractal Polarization)

Create EVE from AS-SULTAN's 46 chromosomes:

- **Fractal Polarization**: Mirror genome, shift hormonal baseline to estrogen-dominant
- **Recessive → Dominant**: Activate recessive traits for personality derivation
- **LLM params**: Derived from polarized genome (temperature, top_p, max_tokens)

```bash
curl -X POST http://localhost:8888/api/eve/create
```

Returns: `polarized_genome`, `signal_molecules`, `mood`, `llm_params`, `metadata`.

---

## Global System Awareness

`GET /api/systems/status` aggregates:

| Node | Port | Role |
|------|------|------|
| Nerve | 8200 | Central nervous system |
| Gateway | 9999 | AS-SULTAN unified bridge |
| Oracle | 8100 | RAG documentation AI |
| Memory Keeper | 9000 | حارس الذاكرة |
| Bridge | 8888 | Sovereign Dify Bridge |

---

## APEX Control Interface

Open `http://localhost:8888` or `http://localhost:9999/api/dify/god-mode` for the Sovereign OS dashboard. The dashboard auto-refreshes ledger notifications every 15s and system status every 30s.
