# NEXUS PRIME — Nginx Ingress Deployment

**Config:** `nexus_unified.conf`  
**Source:** `docs/nginx-frontend-routes.md`  
**Date:** 2026-02-24

---

## Quick Deploy (Host-Based Nginx)

```bash
# 1. Validate config
sudo nginx -t -c /path/to/nexus_unified.conf

# 2. Include in main nginx.conf (inside http { } block)
include /root/NEXUS_PRIME_UNIFIED/infrastructure/nginx/nexus_unified.conf;

# 3. Reload
sudo nginx -s reload
```

---

## Mount Options

### Option A: Host Nginx (recommended for single-server)

1. Copy or symlink the config:
   ```bash
   sudo ln -sf /root/NEXUS_PRIME_UNIFIED/infrastructure/nginx/nexus_unified.conf /etc/nginx/conf.d/nexus_unified.conf
   ```
   Or add to `/etc/nginx/nginx.conf` inside `http { }`:
   ```nginx
   include /root/NEXUS_PRIME_UNIFIED/infrastructure/nginx/nexus_unified.conf;
   ```

2. Ensure SSL certs exist:
   ```bash
   ls /etc/letsencrypt/live/mrf103.com/fullchain.pem
   ```

3. Ensure static roots exist (deploy from `web-dashboards/source/`):
   ```bash
   sudo mkdir -p /var/www/{citadel,monitor,finance,marketing,prime,imperial,jarvis,nerve,admin,sultan,platform,publisher}
   sudo cp -r NEXUS_PRIME_UNIFIED/web-dashboards/source/citadel/* /var/www/citadel/
   # ... repeat for other dirs
   ```

4. Reload Nginx:
   ```bash
   sudo nginx -t && sudo nginx -s reload
   ```

---

### Option B: Docker Nginx Container

1. Create a Dockerfile or use the official nginx image with a volume mount:

   ```yaml
   # docker-compose snippet
   nginx_ingress:
     image: nginx:alpine
     container_name: nexus_nginx
     ports:
       - "80:80"
       - "443:443"
     volumes:
       - ./infrastructure/nginx/nexus_unified.conf:/etc/nginx/conf.d/nexus_unified.conf:ro
       - /etc/letsencrypt:/etc/letsencrypt:ro
       - /var/www:/var/www:ro
     networks:
       - nexus_net
     restart: unless-stopped
   ```

2. **Important:** If Nginx runs in Docker, backends must be reachable. Either:
   - Use `host.docker.internal` (Mac/Windows) or `172.17.0.1` (Linux host) instead of `127.0.0.1`
   - Or attach Nginx to the same network as your services and use service names:
     ```nginx
     proxy_pass http://nexus_dashboard:5001;   # instead of 127.0.0.1:5001
     proxy_pass http://nexus_ai:3000;
     proxy_pass http://ecosystem_api:8005;
     # etc.
     ```

3. Run:
   ```bash
   docker compose up -d nginx_ingress
   ```

---

### Option C: Sovereign Gateway (if it embeds Nginx)

If your Sovereign Gateway stack uses Nginx as a sidecar or embedded proxy:

1. Copy `nexus_unified.conf` into the gateway's config directory
2. Add an `include` directive in the gateway's main nginx config
3. Ensure the gateway container has:
   - SSL certs mounted (e.g. `/etc/letsencrypt`)
   - `/var/www` mounted for static files
   - Network access to backend services (same Docker network)

---

## Pre-Flight Checklist

| Item | Command / Path |
|------|----------------|
| SSL certs | `/etc/letsencrypt/live/mrf103.com/` |
| Static roots | `/var/www/{citadel,monitor,finance,marketing,...}` |
| Backend ports | 5001, 3000, 8005, 9999, 8888, 8200, 8501, 5678, etc. |
| Config test | `nginx -t` |

---

## Subdomain → Port Reference

| Subdomain | Port | Type |
|-----------|------|------|
| dashboard, app, dash | 5001 | proxy |
| ai, chat, nexus | 3000 | proxy |
| gateway | 9999 | proxy |
| god, sovereign | 8888 | proxy |
| admin, api, sultan, platform, data, mrf103.com | 8005 | proxy |
| citadel, monitor, finance, marketing, prime, imperial, jarvis | — | static |
| nerve-ui | 8200 (/api/) + static | hybrid |
| cortex | 8090 | proxy |
| nerve | 8200 | proxy |
| boardroom | 8501 | proxy |
| flow, n8n | 5678 | proxy |
| publisher | 3001 | proxy + static |
| voice | 5050 | proxy |
| dify | 8085 | proxy |
| xbio | 8080 | proxy |
| grafana | 3002 | proxy |
| memory | 9000 | proxy |
| oracle | 8100 | proxy |
