# Final Deployment Steps

## Status: Files Being Transferred to Server

Your deployment files are currently being transferred to `root@46.224.225.96`. Once complete, follow these steps to deploy your applications.

## Step 1: SSH into Your Server

```bash
ssh root@46.224.225.96
# Password: mrfiras1Q@@@
```

## Step 2: Verify Files Transferred

```bash
# Check if files are in home directory
ls -la ~/

# You should see:
# - deploy.sh
# - mrf103-website/
# - DEPLOYMENT_GUIDE.md
```

## Step 3: Deploy Applications (MRF103 + Shadow Seven)

```bash
# Make script executable
chmod +x ~/deploy.sh

# Run deployment (will take 5-15 minutes)
sudo bash ~/deploy.sh

# When prompted, provide:
# 1. Supabase URL: https://your-project.supabase.co
# 2. Supabase Anon Key: your_key_here
# 3. Google AI API Key: (optional)
```

## Step 4: Deploy Website

```bash
# Navigate to website directory
cd ~/mrf103-website

# Make script executable
chmod +x deploy-website.sh

# Run website deployment
sudo bash deploy-website.sh
```

## Step 5: Verify Deployment

```bash
# Check all services
pm2 list

# View logs
pm2 logs

# Test endpoints
curl http://localhost:3001    # MRF103
curl http://localhost:3002    # Shadow Seven
curl http://localhost:8000    # Website
```

## Step 6: Configure Domain (Optional)

```bash
# Edit Nginx configuration
sudo nano /etc/nginx/sites-available/dual-apps

# Update server_name entries with your domain
# Then reload Nginx
sudo systemctl reload nginx

# Set up SSL
sudo certbot --nginx
```

## Step 7: Monitor Applications

```bash
# View all processes
pm2 list

# Monitor in real-time
pm2 monit

# View application logs
pm2 logs mrf103
pm2 logs shadow-seven

# View website logs
tail -f /var/log/website-deployment.log
```

## Accessing Your Applications

Once deployed, access your applications at:

| Application | URL |
|---|---|
| MRF103 API | http://46.224.225.96/api |
| Shadow Seven | http://46.224.225.96 |
| Website | http://46.224.225.96:8000 |

## Troubleshooting

### Applications Not Starting

```bash
# Check PM2 logs
pm2 logs

# Check system resources
free -h
df -h

# Restart all services
pm2 restart all
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :3001
sudo lsof -i :3002

# Kill if necessary
sudo kill -9 <PID>
```

### Nginx Errors

```bash
# Test configuration
sudo nginx -t

# View error log
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx
```

## Environment Variables

The deployment script will create `.env.production` files with:

**MRF103**: `/opt/applications/mrf103/.env.production`
**Shadow Seven**: `/opt/applications/shadow-seven/.env.production`
**Website**: `/opt/websites/mrf103/.env`

## Useful Commands

```bash
# Restart services
pm2 restart all
pm2 restart mrf103
pm2 restart shadow-seven

# Stop services
pm2 stop all

# View service status
systemctl status mrf103-website

# View deployment logs
sudo tail -f /var/log/deployment.log

# Update applications
cd /opt/applications/mrf103
git pull origin main
npm install
pm2 restart mrf103
```

## Support

For issues:
1. Check logs: `pm2 logs`
2. Review deployment guide: `cat ~/DEPLOYMENT_GUIDE.md`
3. Check Nginx: `sudo nginx -t`
4. Monitor resources: `htop`

## Next Steps After Deployment

1. ✅ Configure your domain name
2. ✅ Set up SSL certificates
3. ✅ Monitor application performance
4. ✅ Set up automated backups
5. ✅ Configure monitoring alerts

---

**Deployment Guide v1.0**
MRF103 - AI-Powered Mobile Platform
