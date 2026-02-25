# NEXUS PRIME Nginx Frontend Routes

**Date:** 2026-02-24  
**Source:** `nginx/nexus_unified.conf`  
**Purpose:** Map subdomains to frontend services and static file roots.

---

## 1. Control Plane (Super Admin)

| Subdomain | Backend | Port | Root / Notes |
|-----------|---------|------|--------------|
| dashboard.mrf103.com | nexus_dashboard | 5001 | Dashboard ARC (React) |
| app.mrf103.com | nexus_dashboard | 5001 | Alias |
| dash.mrf103.com | nexus_dashboard | 5001 | Alias |
| gateway.mrf103.com | sovereign_gateway | 9999 | AS-SULTAN Gateway |
| sovereign.mrf103.com | sovereign_dify_bridge | 8888 | God Mode |
| god.mrf103.com | sovereign_dify_bridge | 8888 | God Mode |
| admin.mrf103.com | ecosystem_api | 8005 | Admin API |
| citadel.mrf103.com | Static | — | root: /var/www/citadel |
| monitor.mrf103.com | Static | — | root: /var/www/monitor |
| jarvis.mrf103.com | Static | — | Jarvis Control Hub |
| imperial.mrf103.com | Static | — | Imperial UI |
| nerve-ui.mrf103.com | Static + API proxy | 8200 | root: /var/www/nerve, /api/ → nexus_nerve |
| cortex.mrf103.com | nexus_cortex | 8090 | Cortex API |
| nerve.mrf103.com | nexus_nerve | 8200 | Nerve API |
| boardroom.mrf103.com | nexus_boardroom | 8501 | Cognitive Boardroom (Streamlit) |

---

## 2. Data Plane (End User)

| Subdomain | Backend | Port | Root / Notes |
|-----------|---------|------|--------------|
| publisher.mrf103.com | shadow-seven | 3001 | Shadow Seven Publisher |
| chat.mrf103.com | nexus_ai | 3000 | Open WebUI (AI Chat) |
| ai.mrf103.com | nexus_ai | 3000 | Alias |
| nexus.mrf103.com | nexus_ai | 3000 | Alias |
| mrf103.com | ecosystem_api | 8005 | Main domain, /api/ |
| www.mrf103.com | ecosystem_api | 8005 | Alias |
| sultan.mrf103.com | ecosystem_api | 8005 | Sultan |
| api.mrf103.com | ecosystem_api | 8005 | API Gateway |
| platform.mrf103.com | ecosystem_api | 8005 | Platform |
| data.mrf103.com | ecosystem_api | 8005 | Data Core |
| prime.mrf103.com | Static | — | NEXUS PRIME Frontend |
| finance.mrf103.com | Static | — | root: /var/www/finance |
| marketing.mrf103.com | Static | — | root: /var/www/marketing |
| flow.mrf103.com | nexus_flow | 5678 | n8n Automation |
| n8n.mrf103.com | nexus_flow | 5678 | Alias |

---

## 3. Supporting Services

| Subdomain | Backend | Port |
|-----------|---------|------|
| voice.mrf103.com | nexus_voice | 5050 |
| dify.mrf103.com | Dify | 8085 |
| oracle.mrf103.com | nexus_oracle | 8100 |
| memory.mrf103.com | nexus_memory_keeper | 9000 |
| xbio.mrf103.com | xbio-sentinel | 8080 |
| grafana.mrf103.com | Grafana | 3002 |

---

## 4. Static File Deployment

Web dashboards source files live in `NEXUS_PRIME_UNIFIED/web-dashboards/source/`. To serve via nginx, deploy to `/var/www/`:

| Source | Deploy To |
|--------|-----------|
| web-dashboards/source/citadel/ | /var/www/citadel/ |
| web-dashboards/source/monitor/ | /var/www/monitor/ |
| web-dashboards/source/finance/ | /var/www/finance/ |
| web-dashboards/source/marketing/ | /var/www/marketing/ |
| web-dashboards/source/admin/ | /var/www/admin/ (if configured) |

---

## 5. WebSocket / SSE Routes

| Path | Service |
|------|---------|
| /realtime | nexus_dashboard (Dashboard ARC) |
| /_stcore/stream | nexus_boardroom (Streamlit) |

---

## 6. Cloudflare DNS & Ingress Mapping (Appendix)

**Server IP:** 46.224.225.96 — All subdomains resolve via Cloudflare A records.

| Subdomain | Internal Service / Root | Port | Plane |
|-----------|-------------------------|------|-------|
| admin | ecosystem_api / admin static | 8005 | Control |
| citadel | /var/www/citadel | — | Control |
| dashboard, dash | nexus_dashboard | 5001 | Control |
| monitor | /var/www/monitor | — | Control |
| grafana | Grafana | 3002 | Control |
| nerve-ui | /var/www/nerve + nexus_nerve | 8200 | Control |
| god | sovereign_dify_bridge | 8888 | Control |
| ai, chat, nexus | nexus_ai | 3000 | Data |
| xbio | xbio-sentinel | 8080 | Data |
| sultan | ecosystem_api | 8005 | Data |
| publisher | shadow-seven | 3001 | Data |
| finance, marketing | /var/www/* | — | Data |
| app | nexus_dashboard | 5001 | Data |
| boardroom | nexus_boardroom | 8501 | Data |
| platform, sovereign | ecosystem_api / dify_bridge | 8005/8888 | Data |
| voice | nexus_voice | 5050 | Data |
| api | ecosystem_api | 8005 | Infra |
| gateway | sovereign_gateway | 9999 | Infra |
| dify | Dify | 8085 | Infra |
| flow, n8n | nexus_flow | 5678 | Infra |
| memory | nexus_memory_keeper | 9000 | Infra |
| oracle | nexus_oracle | 8100 | Infra |
| nerve | nexus_nerve | 8200 | Infra |
| cortex | nexus_cortex | 8090 | Infra |
| prime | Static | — | Infra |
| imperial | /var/www/imperial | — | Infra |
| jarvis | /var/www/jarvis | — | Infra |

---

## 7. References

- [FRONTEND_INDEX.md](FRONTEND_INDEX.md) — Page inventory
- [FRONTEND_ARCHITECTURE.md](FRONTEND_ARCHITECTURE.md) — Network flow
- [nginx/nexus_unified.conf](../nginx/nexus_unified.conf) — Full config
