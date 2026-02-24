# NEXUS PRIME — Local Deployment Guide

**Full local execution.** No Supabase Cloud, no external AI APIs, no Stripe required.

---

## Prerequisites

- Ubuntu 22.04+ server
- 16GB+ RAM (22GB recommended)
- 50GB+ free disk space
- Docker & Docker Compose installed

---

## Required Environment Variables

**Root `.env` (NEXUS_PRIME_UNIFIED):**

```env
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=nexus_db
JWT_SECRET=your_jwt_secret_for_postgrest
DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@nexus_db:5432/${POSTGRES_DB}
```

**Optional (for local-only, leave empty or omit):**
- `SUPABASE_URL` — Not used; PostgREST is local
- `SUPABASE_KEY` — Only for JWT generation (PostgREST anon role)
- `STRIPE_SECRET_KEY` — Optional; payment endpoints return "not configured" if empty

---

## Service Dependency Graph

```
nexus_db (PostgreSQL)
    ├── nexus_postgrest (3001) — REST API
    ├── shadow7_api (8002) — Manuscript upload, submit
    ├── nexus_auth (8003)
    └── nexus_memory_keeper (9000)

nexus_ollama (11434)
    └── nexus_litellm (4000) — Routes all AI to Ollama

shadow7_api
    └── /var/www/shadow7/storage — Local file storage
```

---

## Launch Sequence

```bash
cd /root/NEXUS_PRIME_UNIFIED

# 1. Core services
docker compose up -d

# 2. Ensure storage directory exists
sudo mkdir -p /var/www/shadow7/storage/manuscripts
sudo chown -R www-data:www-data /var/www/shadow7  # or your app user

# 3. Pull Ollama models (if not already)
docker exec nexus_ollama ollama pull llama3.2:3b

# 4. Verify
./scripts/full_health_check.sh
```

---

## Shadow Seven — Local Upload Flow

1. **Frontend** (UploadPage) → `POST /api/shadow7/manuscripts/upload`
2. **Backend** (shadow7_api) → Saves file to `/var/www/shadow7/storage/manuscripts/`
3. **Backend** → Inserts into `public.manuscripts` (auto-created if missing)
4. **PostgREST** → Serves manuscripts via `/rest/v1/manuscripts`

**Frontend .env:**
```env
VITE_API_URL=
VITE_SUPABASE_URL=https://publisher.mrf103.com
```
Empty `VITE_API_URL` = same-origin. `VITE_SUPABASE_URL` = base for PostgREST auth.

---

## Verification Checklist

| Check | Command |
|-------|---------|
| All containers up | `docker ps` |
| PostgREST | `curl -s http://localhost:3001/` |
| Shadow7 API | `curl -s http://localhost:8002/api/shadow7/health` |
| LiteLLM | `curl -s http://localhost:4000/health/liveliness` |
| Manuscripts upload | Upload TXT via publisher UI |

---

## Nginx Configuration

Ensure `publisher.mrf103.com` has:

- `location /api/shadow7/` → proxy to `http://127.0.0.1:8002`
- `location /rest/v1/` → proxy to `http://127.0.0.1:3001`
- `client_max_body_size 50M` for manuscript uploads

---

## Stripe (Optional)

When `STRIPE_SECRET_KEY` is empty:
- Payment endpoints return 503 or "not configured"
- No code changes required if already guarded

---

*Local. Sovereign. Yours.*
