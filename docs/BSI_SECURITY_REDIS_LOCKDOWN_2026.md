# BSI/Hetzner Security Alert — Redis Port Lockdown

**Date:** 2026-02-25  
**Alert:** Open Redis on port 6379 (IP: 46.224.225.96)  
**Status:** RESOLVED

---

## 1. Changes Made

### docker-compose.yml

**Removed** port binding from `nexus_redis`:

```diff
  nexus_redis:
    image: redis:7-alpine
    container_name: nexus_redis
-   ports:
-     - "6379:6379"
+   # BSI/Hetzner SECURITY: No port exposure — Redis internal-only (nexus_network)
+   # ports: REMOVED — was "6379:6379" (critical vulnerability)
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
```

### Container Recreate

```bash
docker compose -f docker-compose.yml -f docker-compose.dify.yml up -d --force-recreate nexus_redis
```

---

## 2. UFW Firewall (Secondary Fallback)

Run as root:

```bash
sudo ufw deny 6379/tcp
sudo ufw status
sudo ufw reload
```

---

## 3. Verification

- `docker port nexus_redis` → (empty — no ports published)
- Redis is now **internal-only** via `nexus_network`
- All services (nexus_cortex, nexus_orchestrator, neural_spine, etc.) connect via `nexus_redis:6379` inside Docker — no change needed

---

## 4. Other Internal-Only Services (No Public Ports)

| Service | Port | Exposed | Notes |
|---------|------|---------|-------|
| nexus_db | 5432 | No | PostgreSQL — internal only |
| nexus_redis | 6379 | No | Fixed — internal only |
| Dify redis | 6379 | No | Separate stack, internal |

---

## 5. Ports Intentionally Exposed (Behind Nginx/Proxy)

These are proxied via Nginx and require HTTPS/auth:

- 5001, 3000, 9999, 8085, 8005, 8200, 8501, 5678, etc.

---

**Signed:** Principal Cybersecurity Architect
