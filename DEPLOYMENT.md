# NEXUS PRIME - Deployment Guide

## Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Docker & Docker Compose installed
- Nginx installed
- Domain name with DNS configured

## Quick Deployment

### 1. Clone Repository
```bash
git clone https://github.com/your-org/nexus-prime.git
cd NEXUS_PRIME_UNIFIED
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

### 3. Start Docker Services
```bash
docker-compose up -d
```

### 4. Setup Nginx
```bash
sudo ln -s $(pwd)/nginx/products.conf /etc/nginx/sites-available/nexus
sudo ln -s /etc/nginx/sites-available/nexus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Initialize Database
```bash
docker exec nexus_db psql -U nexus -d nexus_db -f /path/to/schema.sql
```

### 6. Verify Deployment
```bash
bash scripts/monitor.sh
```

## Subdomain Setup

Configure DNS A records:
- nexusprime.io → Server IP
- *.nexusprime.io → Server IP

Or individual records:
- mobile.nexusprime.io
- hub.nexusprime.io
- ai.nexusprime.io
- imperial.nexusprime.io
- data.nexusprime.io
- sentinel.nexusprime.io
- publisher.nexusprime.io

## SSL/TLS Setup

### Using Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d nexusprime.io -d www.nexusprime.io
sudo certbot --nginx -d mobile.nexusprime.io
# Repeat for all subdomains
```

## Monitoring

Access monitoring:
```bash
bash scripts/monitor.sh
```

## Backup

Create backup:
```bash
bash scripts/backup.sh
```

## Troubleshooting

### Services not starting
```bash
docker-compose logs
```

### Database connection issues
```bash
docker exec -it nexus_db psql -U nexus -d nexus_db
```

### Nginx errors
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

## Support
- Documentation: https://docs.nexusprime.io
- Issues: https://github.com/your-org/nexus-prime/issues
- Email: support@nexusprime.io
