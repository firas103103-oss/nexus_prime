# NEXUS PRIME — Ready-to-Fill Variables & Overall Action Guide

**Date:** 2026-02-25

---

## 1. Ready-to-Fill Variables (Mr. F)

Copy [.env.example](.env.example) to `.env` and paste values when ready:

| Variable | Where | Purpose |
|----------|-------|---------|
| `POSTGRES_PASSWORD` | .env | DB password |
| `JWT_SECRET` | .env | Auth signing |
| `SMTP_USER` | .env | Email auth (Nerve, Shadow Seven) |
| `SMTP_PASS` | .env | Email auth |
| `SMTP_FROM_EMAIL` | .env | Sender address |
| `DIFY_API_KEY` | .env | Dify app API key (from Dify Settings → API Keys) |
| `DIFY_DEFENSIVE_WORKFLOW_ID` | .env | Workflow ID for hormonal/X-BIO triggers |
| `STRIPE_PUBLIC_KEY` | .env | Dashboard ARC payments (UK company pending) |
| `STRIPE_SECRET_KEY` | .env | Dashboard ARC payments |
| `VITE_API_URL` | shadow-seven/.env | Publisher API base (empty = same-origin) |
| `SMTP_*` | shadow-seven/.env | Backend email (if separate from root) |

---

## 2. Cloudflare DNS — Your Current Setup

All subdomains point to `46.224.225.96`. Nginx on the server terminates SSL and routes by `Host` header.

**DNS only** (direct to server): admin, ai, api, app, boardroom, chat, citadel, cortex, dashboard, dash, data, dify, flow, gateway, god, imperial, jarvis, n8n, nerve-ui, nexus, oracle, platform, prime, publisher, sovereign, sultan, voice

**Proxied** (via Cloudflare): finance, grafana, marketing, memory, monitor, mrf103.com, nerve, xbio, www (CNAME)

**Recommendation:** For SSL and caching, "DNS only" is fine when Nginx has Let's Encrypt. "Proxied" adds Cloudflare CDN/DDoS protection. Both work; your mix is valid.

---

## 3. What You Should Do Overall

### Immediate (Already Done)
- Dify 502 fixed (full restart applied)
- docs/INDEX.md updated
- Obsolete plans purged (only FINAL_SOVEREIGN_STATE.plan.md kept)
- .env.example pre-wired with SMTP and Dify placeholders

### Your Manual Steps

1. **Fill .env** — Copy `.env.example` to `.env` and add:
   - `POSTGRES_PASSWORD`, `JWT_SECRET` (required)
   - `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM_EMAIL` (for Nerve/Shadow Seven email)
   - `DIFY_API_KEY`, `DIFY_DEFENSIVE_WORKFLOW_ID` (after creating a workflow in Dify)
   - `STRIPE_*` (when UK company is ready)

2. **Dify Admin** — If you forgot the admin password:
   ```bash
   docker exec -it dify-api-1 flask reset-password
   ```

3. **Dify Knowledge Base** — Upload [SOVEREIGN_ENCYCLOPEDIA.md](SOVEREIGN_ENCYCLOPEDIA.md) to Dify as a Knowledge Base for God Mode RAG (manual via Dify UI).

4. **Cloudflare** — No changes needed. All records resolve correctly. Optional: switch more subdomains to Proxied for CDN/DDoS if desired.

5. **Health** — `nexus_nerve` and `sovereign_dify_bridge` show "unhealthy" in Docker but serve traffic (200 OK). You can adjust their healthchecks later if needed.

---

## 4. Service-to-Route Map (Quick Reference)

| Subdomain | Backend | Port | Status |
|-----------|---------|------|--------|
| dify.mrf103.com | Dify | 8085 | OK |
| dashboard.mrf103.com | nexus_dashboard | 5001 | OK |
| gateway.mrf103.com | sovereign_gateway | 9999 | OK |
| chat.mrf103.com, ai.mrf103.com | nexus_ai | 3000 | OK |
| nerve.mrf103.com | nexus_nerve | 8200 | OK |
| api.mrf103.com, platform.mrf103.com | ecosystem_api | 8005 | OK |
| god.mrf103.com, sovereign.mrf103.com | sovereign_dify_bridge | 8888 | OK |
| publisher.mrf103.com | shadow-seven + shadow7_api | 3001, 8002 | OK |
| boardroom.mrf103.com | nexus_boardroom | 8501 | OK |
| oracle.mrf103.com | nexus_oracle | 8100 | OK |
| memory.mrf103.com | nexus_memory_keeper | 9000 | OK |
| flow.mrf103.com, n8n.mrf103.com | nexus_flow | 5678 | OK |
| xbio.mrf103.com | nexus_xbio | 8080 | OK |
| citadel, monitor, finance, etc. | Static /var/www/ | — | OK |

---

## 5. Master Docs Entry Point

Start here: [docs/INDEX.md](INDEX.md)
