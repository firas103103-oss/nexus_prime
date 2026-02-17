# Dual Application Deployment Guide

## Overview

This guide walks you through deploying both the **MRF103 Mobile App Backend** and **Shadow Seven Web Application** to your Ubuntu server at `root@46.224.225.96`.

## Prerequisites

- Ubuntu 20.04 or later
- SSH access to the server
- Supabase project credentials
- Google AI API key (for Shadow Seven)
- Domain names (optional, for SSL setup)

## Quick Start

### Step 1: Transfer Deployment Script to Server

```bash
# From your local machine
scp deploy.sh root@46.224.225.96:/tmp/deploy.sh

# Or download directly on server
ssh root@46.224.225.96
curl -O https://your-domain/deploy.sh
```

### Step 2: Run Deployment Script

```bash
ssh root@46.224.225.96

# Make script executable
chmod +x /tmp/deploy.sh

# Run with sudo
sudo bash /tmp/deploy.sh
```

### Step 3: Provide Configuration

When prompted, provide:

1. **Supabase URL**: `https://your-project.supabase.co`
2. **Supabase Anon Key**: Your public API key from Supabase
3. **Google AI API Key**: Your Google Gemini API key (optional)

## What the Script Does

### System Discovery
- Checks OS version, CPU, RAM, disk space
- Verifies system compatibility

### Dependency Installation
- Installs Node.js 20.x
- Installs npm, Git, Nginx, PM2
- Installs Certbot for SSL certificates

### Application Deployment

#### MRF103 Mobile App Backend
- Clones from: `https://github.com/firas103103-oss/mrf103-mobile-app.git`
- Installs dependencies
- Creates production environment file
- Starts on port **3001**
- Managed by PM2

#### Shadow Seven Web App
- Clones from your repository
- Installs dependencies
- Builds production bundle
- Starts on port **3002**
- Managed by PM2

### Nginx Configuration
- Sets up reverse proxy
- Routes `/api/*` to MRF103 (port 3001)
- Routes `/` to Shadow Seven (port 3002)
- Supports domain-based routing

### Process Management
- Configures PM2 for automatic restarts
- Sets up startup scripts
- Enables process monitoring

## Deployment Architecture

```
┌─────────────────────────────────────────────┐
│         46.224.225.96 (Ubuntu Server)       │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │        Nginx (Reverse Proxy)        │   │
│  │  Port 80 (HTTP) / 443 (HTTPS)       │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
│    ┌────────┴────────┐                     │
│    │                 │                     │
│  ┌─▼──────┐    ┌────▼──────┐              │
│  │ MRF103 │    │  Shadow    │              │
│  │Backend │    │   Seven    │              │
│  │Port 3001    │  Port 3002 │              │
│  └────────┘    └───────────┘              │
│    │                 │                     │
│    └────────┬────────┘                     │
│             │                              │
│        ┌────▼──────────┐                   │
│        │   Supabase    │                   │
│        │   (Shared DB) │                   │
│        └───────────────┘                   │
│                                             │
└─────────────────────────────────────────────┘
```

## Port Mapping

| Application | Port | Access |
|---|---|---|
| MRF103 Backend | 3001 | http://46.224.225.96/api |
| Shadow Seven | 3002 | http://46.224.225.96 |
| Nginx HTTP | 80 | http://46.224.225.96 |
| Nginx HTTPS | 443 | https://46.224.225.96 |

## Post-Deployment Configuration

### 1. Update Nginx Configuration

Edit `/etc/nginx/sites-available/dual-apps` to add your domain names:

```nginx
server {
    listen 80;
    server_name mrf103.yourdomain.com;
    # ... rest of config
}

server {
    listen 80;
    server_name shadow-seven.yourdomain.com;
    # ... rest of config
}
```

Then reload Nginx:
```bash
sudo systemctl reload nginx
```

### 2. Set Up SSL Certificates

```bash
sudo certbot --nginx -d mrf103.yourdomain.com -d shadow-seven.yourdomain.com
```

### 3. Monitor Applications

```bash
# View all processes
pm2 list

# Monitor in real-time
pm2 monit

# View logs
pm2 logs

# View specific app logs
pm2 logs mrf103
pm2 logs shadow-seven
```

### 4. Manage Applications

```bash
# Restart an application
pm2 restart mrf103
pm2 restart shadow-seven

# Stop an application
pm2 stop mrf103

# Start an application
pm2 start mrf103

# Delete an application
pm2 delete mrf103
```

## Environment Variables

### MRF103 (.env.production)
```
NODE_ENV=production
PORT=3001
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
VITE_API_BASE_URL=http://localhost:3001
VITE_API_TIMEOUT=30000
```

### Shadow Seven (.env.production)
```
NODE_ENV=production
PORT=3002
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
VITE_GOOGLE_AI_API_KEY=your_google_ai_key
VITE_API_BASE_URL=http://localhost:3002
VITE_DEFAULT_LANGUAGE=ar
VITE_ENABLE_RTL=true
```

## Troubleshooting

### Applications Not Starting

```bash
# Check PM2 logs
pm2 logs

# Check system logs
sudo journalctl -u nginx -n 50
sudo tail -f /var/log/deployment.log

# Manually test port
curl http://localhost:3001
curl http://localhost:3002
```

### Nginx Not Reloading

```bash
# Test configuration
sudo nginx -t

# Check for syntax errors
sudo nginx -T

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :3001
sudo lsof -i :3002

# Kill process if needed
sudo kill -9 <PID>
```

### Database Connection Issues

1. Verify Supabase credentials in `.env.production`
2. Check Supabase project is active
3. Verify network connectivity to Supabase
4. Check firewall rules

## Backup and Recovery

### Backup Application Data

```bash
# Backup MRF103
tar -czf mrf103-backup-$(date +%Y%m%d).tar.gz /opt/applications/mrf103

# Backup Shadow Seven
tar -czf shadow-seven-backup-$(date +%Y%m%d).tar.gz /opt/applications/shadow-seven
```

### Restore from Backup

```bash
# Stop applications
pm2 stop all

# Restore from backup
tar -xzf mrf103-backup-20260203.tar.gz -C /

# Restart applications
pm2 start all
```

## Security Recommendations

1. **Update System**: `sudo apt-get update && sudo apt-get upgrade`
2. **Configure Firewall**: 
   ```bash
   sudo ufw enable
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```
3. **Use SSH Keys**: Disable password authentication
4. **Enable SSL/TLS**: Use Certbot for automatic HTTPS
5. **Regular Updates**: Keep Node.js and dependencies updated
6. **Monitor Logs**: Set up log rotation and monitoring

## Support and Logs

All deployment activities are logged to:
```
/var/log/deployment.log
```

View deployment log:
```bash
sudo tail -f /var/log/deployment.log
```

## Additional Resources

- [PM2 Documentation](https://pm2.keymetrics.io/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Supabase Documentation](https://supabase.com/docs)
- [Node.js Best Practices](https://nodejs.org/en/docs/guides/nodejs-performance/)

## Next Steps

1. ✅ Run the deployment script
2. ✅ Verify both applications are running
3. ✅ Configure Nginx with your domain names
4. ✅ Set up SSL certificates
5. ✅ Monitor application performance
6. ✅ Set up automated backups

---

**Deployment Date**: February 3, 2026
**Server**: root@46.224.225.96
**Applications**: MRF103 Mobile App + Shadow Seven Web App
