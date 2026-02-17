#!/bin/bash

################################################################################
# DUAL APPLICATION DEPLOYMENT SCRIPT
# Deploys MRF103 Mobile App Backend + Shadow Seven Web App to Ubuntu Server
# Usage: sudo bash deploy.sh
################################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_USER="root"
DEPLOY_DIR="/opt/applications"
MRF103_PORT=3001
SHADOW_SEVEN_PORT=3002
NGINX_CONF="/etc/nginx/sites-available/dual-apps"
LOG_FILE="/var/log/deployment.log"

################################################################################
# LOGGING FUNCTIONS
################################################################################

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✓ $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}✗ $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}" | tee -a "$LOG_FILE"
}

################################################################################
# SYSTEM DISCOVERY
################################################################################

discover_system() {
    log "=== SYSTEM DISCOVERY ==="
    
    log "Hostname: $(hostname)"
    log "OS: $(lsb_release -ds 2>/dev/null || echo 'Unknown')"
    log "Kernel: $(uname -r)"
    log "CPU Cores: $(nproc)"
    log "Total RAM: $(free -h | grep Mem | awk '{print $2}')"
    log "Available RAM: $(free -h | grep Mem | awk '{print $7}')"
    log "Disk Space:"
    df -h / | tail -1 | tee -a "$LOG_FILE"
    
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root. Use: sudo bash deploy.sh"
    fi
    
    success "System discovery completed"
}

################################################################################
# DEPENDENCY INSTALLATION
################################################################################

install_dependencies() {
    log "=== INSTALLING DEPENDENCIES ==="
    
    # Update package manager
    log "Updating package manager..."
    apt-get update -qq || warning "apt-get update had issues"
    
    # Install Node.js if not present
    if ! command -v node &> /dev/null; then
        log "Installing Node.js..."
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash - || error "Failed to add Node.js repository"
        apt-get install -y nodejs || error "Failed to install Node.js"
        success "Node.js installed: $(node --version)"
    else
        log "Node.js already installed: $(node --version)"
    fi
    
    # Install npm if not present
    if ! command -v npm &> /dev/null; then
        log "Installing npm..."
        apt-get install -y npm || error "Failed to install npm"
    fi
    
    # Install Git if not present
    if ! command -v git &> /dev/null; then
        log "Installing Git..."
        apt-get install -y git || error "Failed to install Git"
    fi
    
    # Install Nginx if not present
    if ! command -v nginx &> /dev/null; then
        log "Installing Nginx..."
        apt-get install -y nginx || error "Failed to install Nginx"
        systemctl enable nginx || warning "Failed to enable Nginx auto-start"
    fi
    
    # Install PM2 globally for process management
    if ! command -v pm2 &> /dev/null; then
        log "Installing PM2..."
        npm install -g pm2 || error "Failed to install PM2"
        pm2 startup || warning "Failed to setup PM2 startup"
    fi
    
    # Install certbot for SSL (optional but recommended)
    if ! command -v certbot &> /dev/null; then
        log "Installing Certbot for SSL..."
        apt-get install -y certbot python3-certbot-nginx || warning "Failed to install Certbot"
    fi
    
    success "All dependencies installed"
}

################################################################################
# APPLICATION DEPLOYMENT
################################################################################

setup_deployment_directory() {
    log "=== SETTING UP DEPLOYMENT DIRECTORY ==="
    
    if [ ! -d "$DEPLOY_DIR" ]; then
        log "Creating deployment directory: $DEPLOY_DIR"
        mkdir -p "$DEPLOY_DIR"
    fi
    
    chmod 755 "$DEPLOY_DIR"
    success "Deployment directory ready: $DEPLOY_DIR"
}

deploy_mrf103() {
    log "=== DEPLOYING MRF103 MOBILE APP BACKEND ==="
    
    MRF103_DIR="$DEPLOY_DIR/mrf103"
    
    if [ -d "$MRF103_DIR" ]; then
        log "Updating existing MRF103 installation..."
        cd "$MRF103_DIR"
        git pull origin main || warning "Git pull had issues"
    else
        log "Cloning MRF103 repository..."
        git clone https://github.com/firas103103-oss/mrf103-mobile-app.git "$MRF103_DIR" || error "Failed to clone MRF103 repository"
        cd "$MRF103_DIR"
    fi
    
    # Install dependencies
    log "Installing MRF103 dependencies..."
    npm ci --only=production || npm install --only=production || error "Failed to install MRF103 dependencies"
    
    # Create environment file
    log "Creating MRF103 environment configuration..."
    cat > "$MRF103_DIR/.env.production" << EOF
# MRF103 Production Environment
NODE_ENV=production
PORT=$MRF103_PORT

# Supabase Configuration
EXPO_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
EXPO_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}

# API Configuration
VITE_API_BASE_URL=http://localhost:$MRF103_PORT
VITE_API_TIMEOUT=30000
EOF
    
    # Build if needed
    if [ -f "$MRF103_DIR/package.json" ] && grep -q '"build"' "$MRF103_DIR/package.json"; then
        log "Building MRF103..."
        npm run build || warning "Build had issues"
    fi
    
    # Start with PM2
    log "Starting MRF103 with PM2..."
    pm2 delete mrf103 2>/dev/null || true
    pm2 start "$MRF103_DIR/server/_core/index.ts" --name "mrf103" --interpreter node || \
    pm2 start "npm start" --cwd "$MRF103_DIR" --name "mrf103" || error "Failed to start MRF103"
    
    success "MRF103 deployed on port $MRF103_PORT"
}

deploy_shadow_seven() {
    log "=== DEPLOYING SHADOW SEVEN WEB APP ==="
    
    SHADOW_DIR="$DEPLOY_DIR/shadow-seven"
    
    if [ -d "$SHADOW_DIR" ]; then
        log "Updating existing Shadow Seven installation..."
        cd "$SHADOW_DIR"
        git pull origin main || warning "Git pull had issues"
    else
        log "Cloning Shadow Seven repository..."
        # Note: Replace with your actual repository URL
        git clone https://github.com/yourusername/shadow-seven.git "$SHADOW_DIR" || \
        error "Failed to clone Shadow Seven repository"
        cd "$SHADOW_DIR"
    fi
    
    # Install dependencies
    log "Installing Shadow Seven dependencies..."
    npm ci --only=production || npm install --only=production || error "Failed to install Shadow Seven dependencies"
    
    # Create environment file
    log "Creating Shadow Seven environment configuration..."
    cat > "$SHADOW_DIR/.env.production" << EOF
# Shadow Seven Production Environment
NODE_ENV=production
PORT=$SHADOW_SEVEN_PORT

# Supabase Configuration (Shared)
VITE_SUPABASE_URL=${SUPABASE_URL}
VITE_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}

# Google AI Configuration
VITE_GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY}

# API Configuration
VITE_API_BASE_URL=http://localhost:$SHADOW_SEVEN_PORT
VITE_API_VERSION=v1
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_AI_SUGGESTIONS=true
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NLP_CACHING=true
VITE_ENABLE_WEB_WORKERS=true

# Compliance
VITE_COMPLIANCE_REGIONS=SA,AE,EG,JO
VITE_DEFAULT_COMPLIANCE_LEVEL=medium

# UI Settings
VITE_DEFAULT_LANGUAGE=ar
VITE_DEFAULT_THEME=light
VITE_ENABLE_RTL=true
EOF
    
    # Build application
    log "Building Shadow Seven..."
    npm run build || error "Failed to build Shadow Seven"
    
    # Start with PM2
    log "Starting Shadow Seven with PM2..."
    pm2 delete shadow-seven 2>/dev/null || true
    pm2 start "npm start" --cwd "$SHADOW_DIR" --name "shadow-seven" || error "Failed to start Shadow Seven"
    
    success "Shadow Seven deployed on port $SHADOW_SEVEN_PORT"
}

################################################################################
# NGINX CONFIGURATION
################################################################################

configure_nginx() {
    log "=== CONFIGURING NGINX REVERSE PROXY ==="
    
    # Create Nginx configuration
    cat > "$NGINX_CONF" << 'EOF'
# Upstream servers
upstream mrf103_backend {
    server 127.0.0.1:3001;
}

upstream shadow_seven_app {
    server 127.0.0.1:3002;
}

# MRF103 Backend Server
server {
    listen 80;
    server_name mrf103.example.com;
    
    location / {
        proxy_pass http://mrf103_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Shadow Seven Web App
server {
    listen 80;
    server_name shadow-seven.example.com;
    
    location / {
        proxy_pass http://shadow_seven_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Default server (both apps accessible via IP)
server {
    listen 80 default_server;
    server_name _;
    
    # MRF103 on /api
    location /api/ {
        proxy_pass http://mrf103_backend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Shadow Seven on root
    location / {
        proxy_pass http://shadow_seven_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF
    
    # Enable the configuration
    ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/dual-apps 2>/dev/null || true
    
    # Test Nginx configuration
    log "Testing Nginx configuration..."
    nginx -t || error "Nginx configuration test failed"
    
    # Reload Nginx
    log "Reloading Nginx..."
    systemctl reload nginx || error "Failed to reload Nginx"
    
    success "Nginx configured and reloaded"
}

################################################################################
# PM2 SETUP
################################################################################

setup_pm2() {
    log "=== SETTING UP PM2 PROCESS MANAGEMENT ==="
    
    # Save PM2 configuration
    pm2 save || warning "Failed to save PM2 configuration"
    
    # Setup startup script
    pm2 startup || warning "Failed to setup PM2 startup"
    
    log "PM2 process list:"
    pm2 list | tee -a "$LOG_FILE"
    
    success "PM2 configured"
}

################################################################################
# VERIFICATION
################################################################################

verify_deployment() {
    log "=== VERIFYING DEPLOYMENT ==="
    
    sleep 3
    
    # Check MRF103
    log "Checking MRF103 on port $MRF103_PORT..."
    if curl -s http://localhost:$MRF103_PORT > /dev/null 2>&1; then
        success "MRF103 is responding"
    else
        warning "MRF103 may not be responding yet, check logs"
    fi
    
    # Check Shadow Seven
    log "Checking Shadow Seven on port $SHADOW_SEVEN_PORT..."
    if curl -s http://localhost:$SHADOW_SEVEN_PORT > /dev/null 2>&1; then
        success "Shadow Seven is responding"
    else
        warning "Shadow Seven may not be responding yet, check logs"
    fi
    
    # Check Nginx
    log "Checking Nginx..."
    if systemctl is-active --quiet nginx; then
        success "Nginx is running"
    else
        error "Nginx is not running"
    fi
    
    success "Deployment verification completed"
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    log "╔════════════════════════════════════════════════════════════════╗"
    log "║   DUAL APPLICATION DEPLOYMENT SCRIPT                          ║"
    log "║   MRF103 Mobile App Backend + Shadow Seven Web App            ║"
    log "╚════════════════════════════════════════════════════════════════╝"
    
    # Prompt for required environment variables
    log "=== ENVIRONMENT CONFIGURATION ==="
    
    if [ -z "$SUPABASE_URL" ]; then
        read -p "Enter Supabase URL: " SUPABASE_URL
    fi
    
    if [ -z "$SUPABASE_ANON_KEY" ]; then
        read -sp "Enter Supabase Anon Key: " SUPABASE_ANON_KEY
        echo ""
    fi
    
    if [ -z "$GOOGLE_AI_API_KEY" ]; then
        read -sp "Enter Google AI API Key (optional, press Enter to skip): " GOOGLE_AI_API_KEY
        echo ""
    fi
    
    # Execute deployment steps
    discover_system
    install_dependencies
    setup_deployment_directory
    deploy_mrf103
    deploy_shadow_seven
    configure_nginx
    setup_pm2
    verify_deployment
    
    log "╔════════════════════════════════════════════════════════════════╗"
    log "║   ✓ DEPLOYMENT COMPLETED SUCCESSFULLY                         ║"
    log "╚════════════════════════════════════════════════════════════════╝"
    
    log ""
    log "=== DEPLOYMENT SUMMARY ==="
    log "MRF103 Backend:     http://localhost:$MRF103_PORT (or http://46.224.225.96/api)"
    log "Shadow Seven:       http://localhost:$SHADOW_SEVEN_PORT (or http://46.224.225.96)"
    log "Nginx Config:       $NGINX_CONF"
    log "Deployment Log:     $LOG_FILE"
    log ""
    log "=== NEXT STEPS ==="
    log "1. Update Nginx configuration with your actual domain names"
    log "2. Set up SSL certificates: sudo certbot --nginx"
    log "3. Monitor applications: pm2 monit"
    log "4. View logs: pm2 logs"
    log ""
}

# Run main function
main "$@"
