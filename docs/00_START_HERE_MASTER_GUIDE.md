# 00 — START HERE: Master Guide

**Welcome, Monsieur Feras.**

This is your single entry point to the NEXUS PRIME ecosystem. Read this first.

---

## 1. Welcome — The Vision

NEXUS PRIME is a **sovereign AI ecosystem** — a bio-digital entity designed in Riyadh for absolute technical sovereignty. It is not a collection of APIs; it is a living system with:

- **46 Chromosomes, 82 Traits** — A neural-genome that drives decisions
- **12 Signal Molecules** — Hormonal state (Dopamine, Cortisol, Serotonin, etc.) injected into every LLM call
- **Raqib & Atid Ledger** — Cosmic ledger recording every action in `msl.action_ledger`
- **Soul Monitor** — Observable consciousness via `GET /api/consciousness`

**MRF** (MrF / MRF103) is the holding company. Under it:

- **14 products** (7 production-ready, 5 in development, 2 prototype)
- **12 planets** — Specialized AI agents (AI-ARCH, AS-SULTAN, X-BIO, SHADOW-7, etc.)
- **19+ services** — Docker-based microservices

**Key domains:**

| Domain | Service |
|--------|---------|
| mrf103.com | Landing |
| platform.mrf103.com | NEXUS PRIME Platform |
| publisher.mrf103.com | Shadow Seven Publisher |
| boardroom.mrf103.com | Cognitive Boardroom |
| xbio.mrf103.com | X-BIO Sentinel |
| sultan.mrf103.com | AS-SULTAN Gateway |

---

## 2. Deployment 101

### Prerequisites

- Ubuntu 22.04+ server
- 16GB+ RAM (22GB recommended)
- 50GB+ free disk space
- Docker & Docker Compose installed

### Step-by-Step Launch

```bash
# 1. Navigate to runtime directory
cd /root/NEXUS_PRIME_UNIFIED

# 2. Ensure .env is configured
# Required: POSTGRES_PASSWORD, JWT_SECRET
# Local-only: No Supabase Cloud, no external AI APIs, no Stripe required
# Optional: DIFY_API_KEY, DIFY_DEFENSIVE_WORKFLOW_ID

# 3. Start core services
docker compose up -d

# 4. (Optional) Start monitoring
docker compose -f monitoring/docker-compose.monitoring.yml up -d

# 5. (Optional) Start Dify
./scripts/dify_launch.sh

# 6. Verify health
./scripts/full_health_check.sh
# exit 0 = all services operational
```

### Port Reference

| Port | Service |
|------|---------|
| 3000 | Open WebUI |
| 3001 | PostgREST (Shadow Seven API) |
| 3002 | Grafana |
| 4000 | LiteLLM |
| 5050 | Voice (Edge TTS) |
| 5678 | n8n |
| 8002 | Shadow Seven API |
| 8080 | X-BIO Sentinel |
| 8085 | Dify |
| 8200 | Nerve Center |
| 8501 | Cognitive Boardroom |
| 8888 | Sovereign Bridge |
| 9000 | Memory Keeper |
| 9999 | AS-SULTAN Gateway |
| 11434 | Ollama |

### Stopping Services

```bash
cd /root/NEXUS_PRIME_UNIFIED
docker compose down
docker compose -f monitoring/docker-compose.monitoring.yml down

# Dify
cd dify/docker && docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify down
```

---

## 2.1 Local-Only Architecture

NEXUS PRIME runs **fully on your server**. No external dependencies:

| Component | Local Service |
|-----------|---------------|
| Database | nexus_db (PostgreSQL) |
| REST API | PostgREST (3001) |
| File Storage | Backend `/var/www/shadow7/storage` |
| AI | LiteLLM + Ollama (all models routed locally) |
| Auth | nexus_auth (8003) or PostgREST JWT |

**Manuscript upload** uses `POST /api/shadow7/manuscripts/upload` — files saved to disk, records in nexus_db. No Supabase Storage.

See [LOCAL_DEPLOYMENT.md](LOCAL_DEPLOYMENT.md) for full local deployment guide.

---

## 3. Module Walkthrough

### Shadow Seven Publisher (8002, publisher.mrf103.com)

**Purpose:** AI-powered publishing platform for manuscripts.

**Flow:**
1. **Upload** — Drag & drop TXT files (max 50MB)
2. **Analyze** — TextAnalyzerEnhanced extracts chapters, word count, content type
3. **Store** — Manuscripts saved to Supabase (manuscripts bucket + manuscripts table)
4. **Export** — PDF, EPUB, DOCX, ZIP

**Requirements (Local):**
- `VITE_API_URL` or `VITE_SUPABASE_URL` = publisher base URL (empty for same-origin)
- Backend creates `manuscripts` table automatically; files saved to `/var/www/shadow7/storage/manuscripts`

**Key files:** `planets/SHADOW-7/shadow-seven/`, `products/shadow-seven-publisher/`

---

### xBio Sentinel (8080, xbio.mrf103.com)

**Purpose:** IoT environmental sensing — VOC, BME688, ESP32 integration.

**Flow:**
1. **API** — REST endpoints for sensor data
2. **Mobile App** — Android app for BME688
3. **Firmware** — ESP32 documentation for purchasers

**Requirements:** None beyond Docker. API runs in container.

**Key files:** `planets/X-BIO/`, `products/xbio-sentinel/`

---

### AS-SULTAN (9999, sultan.mrf103.com)

**Purpose:** Sovereign AI gateway — genome-driven responses, unified bridge for NEXUS PRIME.

**Flow:**
1. **Gateway** — Receives requests, injects hormonal state and genome into context
2. **LiteLLM** — Routes to local Ollama or configured models
3. **Raqib/Atid** — Logs actions to cosmic ledger

**Requirements:** LiteLLM (4000), Ollama (11434), models pulled.

---

## 4. Troubleshooting

### Attachment Upload Error (Shadow Seven)

**Symptoms:** "فشل رفع الملف" when uploading manuscripts.

**Root causes (Local):**
1. Backend (shadow7_api 8002) not running
2. `VITE_API_URL` or `VITE_SUPABASE_URL` wrong — must point to publisher domain (e.g. `https://publisher.mrf103.com`) or empty for same-origin
3. Nginx not proxying `/api/shadow7` to backend
4. `/var/www/shadow7/storage` not writable

**Fix:**
1. Ensure `shadow7_api` container running: `docker ps | grep shadow7`
2. Set `VITE_API_URL` or `VITE_SUPABASE_URL` in `.env` (empty = same-origin)
3. Rebuild: `npm run build`
4. Verify nginx: `location /api/shadow7/` proxies to 8002

---

### Service Not Starting

```bash
# Check container status
docker ps -a

# View logs
docker compose logs <service_name>

# Common: DATABASE_URL, POSTGRES_PASSWORD, JWT_SECRET in .env
```

---

### PostgREST (3001) Down

- Ensure `nexus_db` is healthy: `docker ps | grep nexus_db`
- Verify `PGRST_DB_URI` in docker-compose points to correct DB
- Ensure `web_anon` role exists in PostgreSQL

---

### LiteLLM (4000) Not Responding

```bash
# Pull models
docker exec nexus_ollama ollama pull llama3.2:3b

# Check config
cat litellm_config.yaml

# Verify Ollama
curl http://localhost:11434/api/tags
```

---

### Nginx 502 Bad Gateway

- Backend service not running: `docker ps`
- Wrong proxy_pass in nginx config
- `nginx -t && systemctl reload nginx`

---

## 5. Next Steps

1. **Run full health check:** `./scripts/full_health_check.sh`
2. **Verify documentation:** `python3 scripts/verify_documentation_reality.py`
3. **Read RUNBOOK:** `RUNBOOK.md`
4. **Explore planets:** `planets/` directory
5. **Identity & Compliance:** `docs/IDENTITY_COMPLIANCE_PROTOCOL_KIER.md`

---

*NEXUS PRIME — Sovereign. Unified. Yours.*
