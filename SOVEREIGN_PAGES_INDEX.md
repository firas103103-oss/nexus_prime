# Sovereign Stack — Pages & Endpoints Index

## Dashboard Pages (Web UI)

| URL | Page | Service |
|-----|------|---------|
| http://localhost:8888 / https://sovereign.mrf103.com / https://god.mrf103.com | **Sovereign OS Dashboard** (God Mode) | sovereign_dify_bridge |
| http://localhost:9999/api/dify/god-mode / https://gateway.mrf103.com/api/dify/god-mode | God Mode (via Gateway) | sovereign_gateway → bridge |
| http://localhost:9999 / https://gateway.mrf103.com | AS-SULTAN Gateway | sovereign_gateway |
| http://localhost:8085 / https://dify.mrf103.com | Dify | dify-nginx |
| http://localhost:8200 | Nerve API | nexus_nerve |
| http://localhost:8501 | Boardroom | nexus_boardroom |
| http://localhost:5001 | Nexus Dashboard | nexus_dashboard |
| http://localhost:3000 | Open WebUI (AI Chat) | nexus_ai |
| http://localhost:9001 | Memory Keeper Web UI | nexus_memory_keeper |

## Sovereign Bridge APIs (8888)

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Sovereign OS Dashboard |
| GET | /health | Health check |
| GET | /api/hormonal/status | 12 signal molecules |
| GET | /api/genome/entity/{id}/llm-params | Genome → LLM params |
| GET | /api/ledger/recent | Raqib/Atid ledger |
| GET | /api/ledger/notifications | UI notifications |
| POST | /api/eve/create | Eve Protocol |
| GET | /api/systems/status | System health |
| POST | /api/xbio/voc-webhook | X-BIO webhook |
| POST | /api/analytics/collect | Traffic beacon (pageview/event) |
| GET | /api/analytics/stats | Dashboard stats (24h) |

## Gateway Proxies (9999 → Bridge)

| Method | Path |
|--------|------|
| GET | /api/dify/god-mode |
| GET | /api/dify/hormonal/status |
| GET | /api/dify/ledger/recent |
| GET | /api/dify/ledger/notifications |
| GET | /api/dify/genome/entity/{id}/llm-params |
| POST | /api/dify/eve/create |
| GET | /api/dify/systems/status |
| POST | /api/dify/analytics/collect |
| GET | /api/dify/analytics/stats |
| POST | /api/dify/xbio/voc-webhook |

## No Conflicts

All ports are unique. See `SOVEREIGN_PORTS_AND_SERVICES.md` for full matrix.
