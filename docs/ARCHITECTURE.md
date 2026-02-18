# 🏗️ NEXUS PRIME - Technical Architecture

## Overview

NEXUS PRIME follows a microservices architecture with containerized services communicating through Docker networks and Nginx reverse proxy.

---

## System Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                   │
│  Browser → Cloudflare CDN → SSL Termination → Nginx Reverse Proxy       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          NGINX PROXY LAYER                               │
│  /etc/nginx/sites-available/nexus_unified                                │
│  ├── mrf103.com        → Landing Page (static)                          │
│  ├── ai.mrf103.com     → nexus_ai:8080 (Open-WebUI)                     │
│  ├── flow.mrf103.com   → nexus_flow:5678 (n8n)                          │
│  ├── voice.mrf103.com  → nexus_voice:8000 (Edge-TTS)                    │
│  └── *.mrf103.com      → Various services                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DOCKER SERVICE LAYER                             │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │
│  │  nexus_ai    │  │ nexus_flow   │  │ nexus_voice  │                   │
│  │  Open-WebUI  │  │    n8n       │  │  Edge-TTS    │                   │
│  │  :3000→8080  │  │    :5678     │  │  :5050→8000  │                   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘                   │
│         │                 │                                              │
│         ▼                 ▼                                              │
│  ┌──────────────┐  ┌──────────────┐                                     │
│  │nexus_ollama  │  │  nexus_db    │                                     │
│  │   Ollama     │  │ PostgreSQL   │                                     │
│  │   :11434     │  │   :5432      │                                     │
│  └──────────────┘  └──────────────┘                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA PERSISTENCE LAYER                           │
│                                                                          │
│  Docker Volumes:                                                         │
│  ├── root_postgres_data    → PostgreSQL database files                  │
│  ├── root_ollama_data      → AI model weights (11GB)                    │
│  ├── root_open_webui_data  → Chat history, settings                     │
│  └── root_n8n_data         → Workflow definitions, credentials          │
│                                                                          │
│  Bind Mounts:                                                            │
│  ├── /root/nexus_prime/db_data      → PostgreSQL                        │
│  ├── /root/nexus_prime/ollama       → Ollama models                     │
│  ├── /root/nexus_prime/open-webui   → Open-WebUI data                   │
│  └── /root/nexus_prime/n8n_data     → n8n workflows                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Service Communication

### Internal Network

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network: nexus_net                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    nexus_ai ──────────────► nexus_ollama                    │
│    (Open-WebUI)   HTTP     (Ollama API)                     │
│         │         :11434        │                           │
│         │                       │                           │
│         └──────────► nexus_db ◄─┘                           │
│                   (PostgreSQL)                              │
│                      :5432                                  │
│                                                             │
│    nexus_flow ──────────────► External APIs                 │
│    (n8n)          Webhooks    (Stripe, Cloudflare)          │
│                                                             │
│    nexus_voice ────────────► Microsoft Edge TTS             │
│    (Edge-TTS)      HTTPS      (Azure)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### External Access

| Service | Internal Port | External Access |
|---------|---------------|-----------------|
| Open-WebUI | 3000→8080 | ai.mrf103.com (HTTPS) |
| n8n | 5678 | flow.mrf103.com (HTTPS) |
| Edge-TTS | 5050→8000 | voice.mrf103.com (HTTPS) |
| Ollama | 11434 | **Internal only** (UFW DENY) |
| PostgreSQL | 5432 | **Internal only** (UFW DENY) |

---

## Directory Structure

```
/root/
├── NEXUS_PRIME_UNIFIED/           # Master repository (3.9GB)
│   ├── dashboard-arc/             # React admin dashboard
│   │   ├── server/                # Express.js backend
│   │   ├── client/                # React frontend  
│   │   └── shared/                # Shared utilities
│   ├── planets/                   # 12 AI agents
│   │   └── [PLANET_NAME]/
│   │       └── identity.json      # Agent configuration
│   ├── integration/               # 5 integration modules
│   │   ├── ecosystem-api/         # Unified REST API
│   │   ├── shared-auth/           # OAuth/JWT auth
│   │   ├── command-center/        # Command dispatch
│   │   ├── clone-hub/             # Git operations
│   │   └── admin-portal/          # Admin interface
│   ├── scripts/                   # Automation scripts
│   ├── n8n-workflows/             # n8n workflow JSONs
│   ├── landing-pages/             # Static HTML pages
│   └── nginx/                     # Nginx configuration
│
├── nexus_prime/                   # Docker runtime (12GB)
│   ├── docker-compose.yml         # Service definitions
│   ├── db_data/                   # PostgreSQL data
│   ├── ollama/                    # LLM models (11GB)
│   ├── open-webui/                # Chat interface data
│   └── n8n_data/                  # Workflow data
│
├── products/                      # 7 standalone products
│   ├── shadow-seven-publisher/
│   ├── alsultan-intelligence/
│   ├── jarvis-control-hub/
│   ├── imperial-ui/
│   ├── mrf103-mobile/
│   ├── xbio-sentinel/
│   └── nexus-data-core/
│
└── /etc/
    ├── nginx/sites-available/
    │   └── nexus_unified          # Nginx config (210 lines)
    └── letsencrypt/live/
        └── mrf103.com/            # SSL certificates
```

---

## AI Model Architecture

### Ollama Configuration

```yaml
Container: nexus_ollama
Image: ollama/ollama:latest
Port: 11434 (internal only)
Shared Memory: 16GB

Models:
  - llama3.2:latest    # 2.0 GB - General chat
  - qwen2.5:14b        # 9.0 GB - Advanced reasoning
  
Total Model Size: 11.0 GB
```

### Open-WebUI Integration

```yaml
Container: nexus_ai
Image: ghcr.io/open-webui/open-webui:main
Port: 3000→8080

Environment:
  OLLAMA_BASE_URL: http://nexus_ollama:11434
  WEBUI_SECRET_KEY: nexus_wiring_103
  
Features:
  - Multi-model chat
  - Document RAG
  - User management
  - API access
```

---

## Security Architecture

### Network Security

```
┌─────────────────────────────────────────────────────────────┐
│                        UFW Firewall                          │
├─────────────────────────────────────────────────────────────┤
│  ALLOW:                                                      │
│  ├── 22/tcp    ← SSH (all sources)                          │
│  ├── 80/tcp    ← HTTP (Cloudflare IPs only)                 │
│  ├── 443/tcp   ← HTTPS (Cloudflare IPs only)                │
│  ├── 3000/tcp  ← Open-WebUI (consider removing)             │
│  └── 81/tcp    ← NPM Admin                                  │
│                                                              │
│  DENY (External):                                            │
│  ├── 11434/tcp ← Ollama (Docker internal)                   │
│  ├── 5678/tcp  ← n8n (via Nginx only)                       │
│  ├── 5432/tcp  ← PostgreSQL (Docker internal)               │
│  ├── 5050/tcp  ← Voice (via Nginx only)                     │
│  ├── 5000/tcp  ← Gateway (via Nginx only)                   │
│  └── 8080/tcp  ← Reserved                                   │
└─────────────────────────────────────────────────────────────┘
```

### SSL/TLS

```
Certificate: Let's Encrypt Wildcard
Domain: *.mrf103.com
Expiry: April 28, 2026
Auto-renewal: certbot cron job
```

### API Security

| Service | Auth Method | Token Location |
|---------|-------------|----------------|
| Open-WebUI | JWT | Browser cookie |
| n8n | Basic Auth / API Key | Header |
| Ollama | None (internal) | - |
| PostgreSQL | Password | Connection string |

---

## Backup Architecture

### Automated Backups

```bash
# Cron: 0 3 * * * (3 AM daily)
/usr/local/bin/nexus-backup

Backup Contents:
├── nexus_db_YYYY-MM-DD.sql       # PostgreSQL dump (pg_dump)
└── nexus_configs_YYYY-MM-DD.tar.gz
    ├── docker-compose.yml
    ├── db_data/
    ├── n8n_data/
    ├── open-webui/
    ├── MASTER_DOCUMENTATION.md
    ├── scripts/
    └── nginx config

Note: Ollama models (11GB) are EXCLUDED
      (can be re-downloaded from Ollama Registry)
```

### Retention Policy

- Keep last 7 days of backups
- Auto-cleanup older files

---

## Deployment Architecture

### Production Stack

```yaml
Server: Hetzner Ubuntu
RAM: 22GB
Disk: 451GB (45% used)
IPv4: 46.224.225.96
IPv6: 2a01:4f8:1c19:c6de::1

DNS: Cloudflare
  - Proxied A records
  - SSL: Full (Strict)
  - Firewall: IP whitelist

Services:
  - Docker Engine
  - Nginx (host-level)
  - Certbot auto-renewal
  - UFW firewall
```

### CI/CD Pipeline

```
Local Development
      │
      ▼
GitHub (firas103103-oss)
      │
      ▼
SSH → Server (/root/NEXUS_PRIME_UNIFIED)
      │
      ▼
git pull → docker compose restart
```

---

## Performance Considerations

### Resource Allocation

| Service | CPU | Memory | Storage |
|---------|-----|--------|---------|
| nexus_ollama | High (inference) | 8-16GB | 11GB models |
| nexus_ai | Medium | 512MB-1GB | 889MB data |
| nexus_db | Low | 128MB | 48MB |
| nexus_flow | Medium | 256MB | 4.6MB |
| nexus_voice | Low | 32MB | Minimal |

### Optimization Tips

1. **Ollama**: Use `shm_size: 16gb` for better performance
2. **PostgreSQL**: Consider connection pooling for scale
3. **Nginx**: Enable gzip compression and caching
4. **n8n**: Archive old executions regularly

---

## Monitoring

### Health Checks

```bash
# Docker built-in healthchecks
docker ps --format "table {{.Names}}\t{{.Status}}"

# Service-specific
curl -s localhost:11434/api/tags     # Ollama
curl -s localhost:3000               # Open-WebUI
curl -s localhost:5678               # n8n
```

### Logs

```bash
# All containers
docker compose logs -f

# Specific service
docker logs -f nexus_ai
docker logs -f nexus_ollama

# Nginx
tail -f /var/log/nginx/access.log
```

---

## Future Architecture Considerations

1. **Kubernetes**: For horizontal scaling
2. **Redis**: Session caching for Open-WebUI
3. **Prometheus/Grafana**: Metrics and monitoring
4. **Vector Database**: Enhanced RAG capabilities
5. **Load Balancer**: For high availability

---

*Last updated: February 18, 2026*
