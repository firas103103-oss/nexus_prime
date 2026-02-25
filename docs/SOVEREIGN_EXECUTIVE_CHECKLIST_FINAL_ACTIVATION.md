# SOVEREIGN EXECUTIVE CHECKLIST: FINAL ACTIVATION

**Authority:** Monsieur Feras  
**Date:** 2026-02-25  
**Purpose:** Manual activation steps for Sovereign AI ecosystem — execute in order.

---

## 1. CLOUDFLARE CONFIRMATION (The Shield)

- [ ] Go to Cloudflare Dashboard → `mrf103.com`.
- [ ] Navigate to **SSL/TLS** → **Overview**.
- [ ] Ensure the mode is strictly set to: **Full (strict)**.  
  *(This guarantees end-to-end encryption between Cloudflare and your Nginx Let's Encrypt certificates.)*
- [ ] Navigate to **DNS** → **Records**.
- [ ] Visually confirm every single subdomain (api, dify, dashboard, etc.) has the Orange Cloud icon (Proxied).

---

## 2. DIFY GOD MODE INITIALIZATION (The Brain)

- [ ] Open your browser and navigate to: `https://dify.mrf103.com`
- [ ] The page should load securely (Padlock icon) without redirect loops.
- [ ] Set up your primary Admin Account.
- [ ] Navigate to **Knowledge** → **Create Knowledge**.
- [ ] Upload `/root/NEXUS_PRIME_UNIFIED/docs/SOVEREIGN_ENCYCLOPEDIA.md`.  
  *(This officially injects the "Sovereign Mindset" into your local AI models.)*

**If 502 Bad Gateway:** Restart dify nginx and web:
```bash
cd /root/NEXUS_PRIME_UNIFIED/dify/docker
docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify restart nginx web
# Wait ~15 seconds, then retry https://dify.mrf103.com
```

**If you forgot the Dify admin password:**
```bash
docker exec -it dify-api-1 flask reset-password
```

---

## 3. THE ECOSYSTEM PULSE TEST (The Verification)

- [ ] Visit `https://dashboard.mrf103.com` → Confirm Dashboard ARC UI loads.
- [ ] Visit `https://cortex.mrf103.com` → Confirm Cortex API / agent dashboard loads.  
  *(Note: cortex serves nexus_cortex, not PocketBase.)*
- [ ] Visit `https://api.mrf103.com/api/v1/health` → Confirm it returns a healthy JSON response.

---

## 4. PRE-CHECK (Optional — Run from Server)

```bash
# Quick health probe from server
curl -sf https://api.mrf103.com/api/v1/health | jq .
curl -sf https://api.mrf103.com/health | jq .
curl -sf https://dashboard.mrf103.com/ -o /dev/null -w "%{http_code}\n"
curl -sf https://cortex.mrf103.com/health | jq .
```

Expected: `200` for HTTP probes; JSON with `status: healthy` for `/health` endpoints.

---

## 5. REFERENCE

| URL | Backend | Port |
|-----|---------|------|
| dashboard.mrf103.com | nexus_dashboard | 5001 |
| cortex.mrf103.com | nexus_cortex | 8090 |
| api.mrf103.com | ecosystem_api | 8005 |
| dify.mrf103.com | Dify | 8085 |

---

**Signed:** Principal Systems Architect
