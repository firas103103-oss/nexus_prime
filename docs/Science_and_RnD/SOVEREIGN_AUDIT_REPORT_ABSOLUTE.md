# NEXUS PRIME — Total Sovereign Audit & Unification Report (Phase: Absolute)

**Role:** Supreme Systems Architect (Kier)  
**Date:** 2026-02-24  
**Mission:** Zero external dependency, zero redundancy, total database centralization.

---

## 1. UNIFIED DATABASE VERIFICATION (nexus_db)

### ✅ Modules Verified

| Module | DB Usage | Status |
|--------|----------|--------|
| **Shadow Seven** (products + planets) | PostgREST (3001) → nexus_db, local upload API (8002) | ✅ Unified |
| **NEXUS PRIME Core** (ecosystem_api, auth, etc.) | nexus_db via DATABASE_URL | ✅ Unified |
| **Cognitive Boardroom** | nexus_db via DATABASE_URL | ✅ Unified |
| **Sales / Subscriptions / Books** | ecosystem_api → nexus_db | ✅ Unified |
| **Marketing / Publishing Agents** | ecosystem_api, dashboard-arc | ✅ Unified |
| **nexus_postgrest** | nexus_db (PGRST_DB_URI) | ✅ Unified |
| **nexus_memory_keeper** | nexus_db | ✅ Unified |
| **nexus_auth** | nexus_db | ✅ Unified |

### ⚠️ Modules Requiring Attention

| Module | Issue | Action Taken |
|--------|-------|--------------|
| **dashboard-arc** | SUPABASE_URL pointed to cloud | ✅ Fixed: docker-compose fallback to `http://nexus_postgrest:3000` when SUPABASE_URL empty; added nexus_postgrest to depends_on |
| **AI_CONTEXT.md** | Hardcoded Supabase pooler URL | ✅ Fixed: Replaced with nexus_db reference |
| **arc-core-main** (planets/AI-ARCH) | **better-sqlite3** (SQLite) | ⚠️ Manual: Migrate to nexus_db or add DATABASE_URL support |
| **AlSultan Intelligence** (sultan-full) | Supabase client | ⚠️ Manual: Point VITE_SUPABASE_URL to local PostgREST when deploying locally |

### Inshitar / Jibnat Hawa / Eve's Cheese

- **Reactive & Genetic Fission (Inshitar)** and **Eve's Cheese (Jibnat Hawa)** — No NEXUS PRIME modules found for these terms in codebase. Likely conceptual or in external docs. No integration required for current audit.

---

## 2. ARCHITECTURAL & PORT AUDIT

### Port Map (Current Allocations)

| Port | Service | Container |
|------|---------|-----------|
| 3000 | Open WebUI (AI Chat) | nexus_ai |
| 3001 | PostgREST (Shadow Seven, dashboard) | nexus_postgrest |
| 3002 | Grafana | monitoring |
| 4000 | LiteLLM | nexus_litellm |
| 5050 | Voice (Edge TTS) | nexus_voice |
| 5678 | n8n | nexus_flow |
| 6379 | Redis | nexus_redis |
| 8002 | Shadow Seven API | shadow7_api |
| 8003 | Auth | nexus_auth |
| 8005 | Ecosystem API | ecosystem_api |
| 8080 | X-BIO Sentinel | nexus_xbio |
| 8090 | Cortex | nexus_cortex |
| 8100 | Oracle | nexus_oracle |
| 8200 | Nerve | nexus_nerve |
| 8501 | Cognitive Boardroom | nexus_boardroom |
| 9000, 9001 | Memory Keeper | nexus_memory_keeper |
| 9999 | Sovereign Gateway | sovereign_gateway |
| 11434 | Ollama | nexus_ollama |
| 5001 | Dashboard ARC | nexus_dashboard |

### Port Conflict

- **planets/AI-ARCH/arc-core-main** defaults to **8080**; **nexus_xbio** uses **8080**. If arc-core is run alongside Docker stack, change arc-core to **8081** or another free port.

### Domain → Nginx Mapping (Verified)

| Domain | Service | Nginx Location |
|--------|---------|----------------|
| mrf103.com | Landing | / |
| publisher.mrf103.com | Shadow Seven | /, /api/shadow7/, /rest/v1/ |
| sultan.mrf103.com | AlSultan | / |
| admin.mrf103.com | Admin | / |
| chat.mrf103.com, nexus.mrf103.com, ai.mrf103.com | Open WebUI | / |
| flow.mrf103.com, n8n.mrf103.com | n8n | / |
| api.mrf103.com | API Gateway | / |
| sovereign.mrf103.com, god.mrf103.com | Sovereign | / |
| gateway.mrf103.com | Gateway | / |
| dify.mrf103.com | Dify | / |
| jarvis.mrf103.com | Jarvis Control Hub | / |
| imperial.mrf103.com | Imperial | / |
| voice.mrf103.com | Voice | / |
| prime.mrf103.com | Prime | / |
| boardroom.mrf103.com | Boardroom | / |
| dashboard.mrf103.com, app.mrf103.com, dash.mrf103.com | Dashboard ARC | / |
| monitor.mrf103.com | Monitor | / |
| finance.mrf103.com | Finance | / |
| marketing.mrf103.com | Marketing | / |
| cortex.mrf103.com | Cortex | / |
| platform.mrf103.com | Platform | / |
| oracle.mrf103.com | Oracle | / |
| data.mrf103.com | Data | / |
| grafana.mrf103.com | Grafana | / |
| xbio.mrf103.com | X-BIO | / |
| memory.mrf103.com | Memory | / |
| nerve.mrf103.com | Nerve | / |

**AI-ARCH / arc-core** — Not in nginx. Orphan; see Orphan Hunt.

---

## 3. ORPHAN HUNT (Exploratory Scouting)

### Orphan / Standalone Modules

| Module | Path | Status | Recommendation |
|--------|------|--------|----------------|
| **arc-core-main** | planets/AI-ARCH/arc-core-main | Node backend, SQLite, port 8080 | Add to Master Dashboard or Operational Runbook; migrate to nexus_db; change port to 8081 |
| **jarvis-control-hub** | products/jarvis-control-hub | jarvis.mrf103.com mapped | ✅ Linked via nginx |
| **AlSultan Intelligence** | products/alsultan-intelligence/sultan-full | sultan.mrf103.com mapped | ✅ Linked; ensure VITE_SUPABASE_URL points to local when sovereign |
| **7thshadow-main** | planets/SHADOW-7/7thshadow-main | Legacy Shadow Seven | Archive or merge with shadow-seven-publisher |
| **777-main, 777777777777777777777777777777-main** | planets/AI-ARCH | Legacy AI-ARCH variants | Archive or consolidate with arc-core-main |

---

## 4. AUTO-FIX & IMPLEMENTATION (Completed)

| Fix | Location | Action |
|-----|----------|--------|
| Dashboard local PostgREST | docker-compose.yml | Added SUPABASE_URL fallback, nexus_postgrest depends_on |
| AI_CONTEXT.md credentials | dashboard-arc/AI_CONTEXT.md | Replaced Supabase pooler with nexus_db reference |
| LOCAL_DEPLOYMENT.md | docs/LOCAL_DEPLOYMENT.md | Clarified SUPABASE_URL/SUPABASE_KEY for local mode |

---

## 5. DATABASE MAP (Unified Schema Usage)

```
nexus_db (PostgreSQL @ nexus_db:5432)
├── public.manuscripts          — Shadow Seven
├── public.command_logs         — Dashboard ARC
├── public.agents               — Dashboard ARC
├── public.departments          — Dashboard ARC
├── public.memories             — Dashboard ARC (vector store)
├── public.executive_summaries  — Dashboard ARC (ensure table exists)
├── public.ceo_reminders       — Dashboard ARC (ensure table exists)
├── public.agent_events        — Dashboard ARC (ensure table exists)
├── msl.action_ledger           — Raqib & Atid
└── [ecosystem tables]          — Sales, Subscriptions, Books, etc.
```

**PostgREST** (nexus_postgrest:3000) exposes `public` schema. JWT signed with `JWT_SECRET` for `web_anon` role.

---

## 6. MANUAL CHECKLIST (Monsieur Feras)

**Items requiring physical intervention:**

1. **Full local mode:** In root `.env`, set `SUPABASE_URL=` (empty) or remove it. Set `SUPABASE_KEY` to a JWT signed with `JWT_SECRET` for PostgREST `web_anon` role (e.g. use `jsonwebtoken` or online JWT generator with payload `{"role":"web_anon"}`).
2. **arc-core-main migration:** Migrate SQLite to nexus_db PostgreSQL, or add `DATABASE_URL` support and document. Change default port from 8080 to 8081 if running alongside nexus_xbio.
3. **Dashboard tables:** Ensure `executive_summaries`, `ceo_reminders`, `agent_events` exist in nexus_db. Run migrations if provided.
4. **AlSultan local:** When deploying sultan.mrf103.com in local-only mode, set `VITE_SUPABASE_URL` to `https://publisher.mrf103.com` (or local PostgREST URL) so it uses nexus_db via PostgREST.
5. **Archive legacy docs:** Many files in `dashboard-arc/docs/archive/`, `planets/*/archive/`, `PROJECTS_ARCHIVE/` contain old Supabase URLs. Consider archiving or updating for consistency.
6. **Nginx reload:** After any nginx config changes: `sudo nginx -t && sudo systemctl reload nginx`.

---

## Summary

- **Unified DB:** Core stack uses nexus_db. Dashboard now falls back to local PostgREST.
- **Ports:** No conflicts in Docker stack. arc-core-main (8080) conflicts with nexus_xbio if both run.
- **Orphans:** arc-core-main, legacy AI-ARCH/Shadow Seven variants identified for integration or archive.
- **Auto-fixes:** docker-compose, AI_CONTEXT.md, LOCAL_DEPLOYMENT.md updated.
- **Manual:** JWT generation, arc-core migration, table creation, AlSultan local config, nginx reload.

*Kier. Purge complete.*
