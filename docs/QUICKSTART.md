# ⚡ NEXUS PRIME - Quick Start Guide

Get NEXUS PRIME up and running in under 5 minutes.

---

## Prerequisites

- Ubuntu 22.04+ server
- 16GB+ RAM (22GB recommended)
- 50GB+ free disk space
- Docker & Docker Compose installed
- Domain pointing to server (optional but recommended)

---

## Step 1: Clone Repository

```bash
# SSH into your server
ssh root@your-server-ip

# Clone the repository
git clone git@github.com:firas103103-oss/nexus_prime.git
cd nexus_prime
```

---

## Step 2: Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**Required Variables:**
```env
POSTGRES_PASSWORD=your_secure_password
WEBUI_SECRET_KEY=your_secret_key
TZ=Asia/Riyadh
```

---

## Step 3: Launch Services

```bash
# Navigate to runtime directory
cd /root/nexus_prime

# Start all services
docker compose up -d

# Verify services are running
docker ps
```

Expected output:
```
NAMES          STATUS          PORTS
nexus_ai       Up (healthy)    0.0.0.0:3000->8080/tcp
nexus_db       Up (healthy)    5432/tcp
nexus_ollama   Up              0.0.0.0:11434->11434/tcp
nexus_flow     Up              0.0.0.0:5678->5678/tcp
nexus_voice    Up              0.0.0.0:5050->8000/tcp
```

---

## Step 4: Pull AI Models

```bash
# Pull the default models (this takes a few minutes)
docker exec nexus_ollama ollama pull llama3.2:latest
docker exec nexus_ollama ollama pull qwen2.5:14b

# Verify models
curl -s http://localhost:11434/api/tags | python3 -m json.tool
```

---

## Step 5: Access Services

| Service | URL | Default Credentials |
|---------|-----|---------------------|
| AI Chat | http://localhost:3000 | Create on first visit |
| n8n Automation | http://localhost:5678 | admin / nexus_mrf_flow_2026 |
| Ollama API | http://localhost:11434 | No auth (internal) |

---

## Step 6: Run Tests

```bash
# Navigate to unified directory
cd /root/NEXUS_PRIME_UNIFIED

# Run comprehensive tests
bash scripts/final_test.sh
```

Expected: `41/41 (100%) - All tests passing`

---

## Optional: Configure Domain & SSL

### DNS Setup (Cloudflare)

```bash
# Set your Cloudflare credentials
export CF_TOKEN="your_cloudflare_token"
export CF_ZONE_ID="your_zone_id"

# Run DNS setup script
bash scripts/setup_dns.sh
```

### SSL Certificate

```bash
# Install certbot
apt install certbot python3-certbot-nginx

# Get wildcard certificate
certbot certonly --manual --preferred-challenges dns \
  -d "*.mrf103.com" -d "mrf103.com"
```

### Nginx Configuration

```bash
# Copy nginx config
cp nginx/nexus_unified.conf /etc/nginx/sites-available/nexus_unified

# Enable site
ln -s /etc/nginx/sites-available/nexus_unified /etc/nginx/sites-enabled/

# Test and reload
nginx -t && systemctl reload nginx
```

---

## Common Commands

### Service Management

```bash
# Restart all services
cd /root/nexus_prime && docker compose restart

# Stop all services
docker compose down

# View logs
docker compose logs -f

# View specific service logs
docker logs -f nexus_ai
```

### System Status

```bash
# Quick status check
bash scripts/STATUS.sh

# Full system status
bash scripts/final_test.sh

# Docker resource usage
docker stats --no-stream
```

### Git Sync

```bash
# Sync all products to GitHub
bash scripts/git_sync_all.sh

# Pull latest changes
git pull origin main
```

### Backup

```bash
# Manual backup
/usr/local/bin/nexus-backup

# View backups
ls -la /root/nexus_prime_backups/
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check container status
docker ps -a

# View logs for failed container
docker logs nexus_SERVICE_NAME

# Remove and recreate
docker compose down
docker compose up -d
```

### Ollama Out of Memory

```bash
# Check memory usage
free -h

# Restart Ollama
docker restart nexus_ollama

# Use smaller model
docker exec nexus_ollama ollama rm qwen2.5:14b
docker exec nexus_ollama ollama pull llama3.2:3b
```

### Database Connection Issues

```bash
# Check database container
docker logs nexus_db

# Connect to database
docker exec -it nexus_db psql -U postgres

# Reset database (CAUTION: destroys data)
docker compose down
rm -rf db_data/*
docker compose up -d
```

### Nginx 502 Bad Gateway

```bash
# Check backend service is running
docker ps | grep nexus_ai

# Check nginx config
nginx -t

# Restart nginx
systemctl restart nginx
```

---

## Next Steps

1. **Explore AI Chat**: Visit http://localhost:3000 and start chatting
2. **Create Workflows**: Open n8n at http://localhost:5678
3. **Read Full Docs**: See [MASTER_DOCUMENTATION.md](../MASTER_DOCUMENTATION.md)
4. **Configure Planets**: Explore the `/planets/` directory
5. **Set Up Products**: Review the `/products/` directory

---

## Getting Help

- **Documentation**: [MASTER_DOCUMENTATION.md](../MASTER_DOCUMENTATION.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **GitHub Issues**: https://github.com/firas103103-oss/nexus_prime/issues
- **Email**: admin@mrf103.com

---

*Happy building with NEXUS PRIME! 🌌*
