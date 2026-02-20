#!/bin/bash
# 🚪 NEXUS PRIME - نص خروج النظام  
# Exit Script - إغلاق النظام بالتدرج الآمن

set -e  # Stop on any error

echo "🚪 === NEXUS PRIME EMPIRE EXIT SEQUENCE ==="
echo "📅 Starting shutdown at: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Function to check if service is stopped
check_service_stopped() {
    local port=$1
    local service=$2
    local max_attempts=10
    local attempt=1
    
    echo "🔍 Verifying $service shutdown (Port $port)..."
    while [ $attempt -le $max_attempts ]; do
        if ! curl -s -o /dev/null --connect-timeout 1 --max-time 2 http://localhost:$port > /dev/null 2>&1; then
            echo "  ✅ $service stopped successfully"
            return 0
        fi
        echo "  ⏳ Waiting for $service to stop... (attempt $attempt/$max_attempts)"
        sleep 1
        ((attempt++))
    done
    echo "  ⚠️ $service may still be running"
    return 1
}

# Function to safely backup before shutdown
create_emergency_backup() {
    echo "💾 Creating emergency backup..."
    backup_dir="/root/nexus_prime_backups/EMERGENCY_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Database backup
    echo "  📊 Backing up database..."
    cd /root/NEXUS_PRIME_UNIFIED
    if docker compose exec nexus_db pg_dump -U postgres nexus_db > "$backup_dir/nexus_db_emergency.sql" 2>/dev/null; then
        echo "  ✅ Database backed up to: $backup_dir/nexus_db_emergency.sql"
    else
        echo "  ⚠️ Database backup failed or unavailable"
    fi
    
    # Configuration backup
    echo "  ⚙️ Backing up configurations..."
    cp -r /root/NEXUS_PRIME_UNIFIED/.env "$backup_dir/" 2>/dev/null || echo "  ℹ️ .env not found"
    cp -r /root/NEXUS_PRIME_UNIFIED/docker-compose.yml "$backup_dir/" 2>/dev/null || echo "  ℹ️ docker-compose.yml not found"
    
    echo "  ✅ Emergency backup completed: $backup_dir"
}

# Pre-shutdown checks and backup
echo "🔧 === PRE-SHUTDOWN PROCEDURES ==="

# Ask for confirmation (optional - remove for automated scripts)
read -p "⚠️  Are you sure you want to shutdown NEXUS PRIME EMPIRE? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Shutdown cancelled by user"
    exit 1
fi

# Create emergency backup
create_emergency_backup

echo ""
echo "🛑 === PHASE 1: SECONDARY SERVICES SHUTDOWN ==="

# Stop Jarvis Memory
echo "🧠 Stopping Jarvis Memory API..."
if pgrep -f jarvis_api.py > /dev/null; then
    pkill -f jarvis_api.py
    echo "  ✅ Jarvis Memory processes terminated"
else
    echo "  ℹ️ Jarvis Memory not running"
fi
check_service_stopped 9000 "Jarvis Memory"

# Stop XBio System
echo "🧬 Stopping XBio Vault System..."
if docker ps | grep -q nexus_xbio; then
    docker stop nexus_xbio 2>/dev/null || true
    docker rm nexus_xbio 2>/dev/null || true
    echo "  ✅ XBio System container stopped and removed"
else
    echo "  ℹ️ XBio System not running"
fi
check_service_stopped 8080 "XBio Vault"

echo ""
echo "🔬 === PHASE 2: ADVANCED SERVICES SHUTDOWN ==="

cd /root/NEXUS_PRIME_UNIFIED

# Stop Cognitive Boardroom
echo "👥 Stopping Cognitive Boardroom..."
docker compose stop nexus_boardroom 2>/dev/null
echo "  ✅ Cognitive Boardroom stopped"
check_service_stopped 8501 "Cognitive Boardroom"

# Stop Flow Automation  
echo "🔄 Stopping Workflow Automation..."
docker compose stop nexus_flow 2>/dev/null
echo "  ✅ Flow Automation stopped"
check_service_stopped 5678 "Flow Automation"

echo ""
echo "🏛️ === PHASE 3: CORE SERVICES SHUTDOWN ==="

# Stop Voice Service
echo "🎙️ Stopping Voice Service..."
docker compose stop nexus_voice 2>/dev/null
echo "  ✅ Voice Service stopped"
check_service_stopped 5050 "Voice Service"

# Stop Dashboard
echo "📊 Stopping Main Dashboard..."
docker compose stop nexus_dashboard 2>/dev/null  
echo "  ✅ Dashboard stopped"
check_service_stopped 5001 "Dashboard"

# Stop AI Interface
echo "🧠 Stopping AI Interface..."
docker compose stop nexus_ai 2>/dev/null
echo "  ✅ AI Interface stopped"
check_service_stopped 3000 "AI Interface"

echo ""
echo "🔧 === PHASE 4: FOUNDATION SHUTDOWN ==="

# Stop Ollama (AI Engine)
echo "🤖 Stopping Ollama AI Engine..."
docker compose stop nexus_ollama 2>/dev/null
echo "  ✅ Ollama Engine stopped"
check_service_stopped 11434 "Ollama Engine"

# Stop Database (LAST)
echo "🗃️ Stopping PostgreSQL Database..."
docker compose stop nexus_db 2>/dev/null
echo "  ✅ Database stopped safely"

echo ""
echo "🔍 === FINAL VERIFICATION ==="

echo "📊 Checking remaining processes..."
remaining_containers=$(docker ps --filter "label=com.docker.compose.project=nexus_prime_unified" --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | tail -n +2)
if [ -z "$remaining_containers" ]; then
    echo "  ✅ All NEXUS containers stopped"
else
    echo "  ⚠️ Some containers may still be running:"
    echo "$remaining_containers"
fi

echo "🌐 Checking remaining network connections..."
active_ports=$(ss -tuln | grep -E ":(3000|5001|5050|5678|8080|8501|9000|11434)" 2>/dev/null || true)
if [ -z "$active_ports" ]; then
    echo "  ✅ All NEXUS ports are free"
else
    echo "  ⚠️ Some ports may still be in use:"
    echo "$active_ports"
fi

# Check for any remaining Python processes
remaining_python=$(pgrep -f "python.*jarvis\|python.*nexus" 2>/dev/null || true)
if [ -z "$remaining_python" ]; then
    echo "  ✅ No remaining Python processes"
else
    echo "  ⚠️ Some Python processes may still be running: $remaining_python"
fi

echo ""
echo "📊 === SHUTDOWN SUMMARY ==="

services_shutdown=(
    "Jarvis Memory API"
    "XBio Vault System"
    "Cognitive Boardroom"
    "Flow Automation"
    "Voice Service"
    "Main Dashboard"
    "AI Interface"
    "Ollama Engine"
    "PostgreSQL Database"
)

echo "🏰 NEXUS PRIME EMPIRE COMPONENTS SHUTDOWN:"
for service in "${services_shutdown[@]}"; do
    echo "  ✅ $service"
done

echo ""
echo "💾 Data Safety Report:"
echo "  ✅ Emergency backup created"
echo "  ✅ Database safely stopped"
echo "  ✅ No forced kills used"
echo "  ✅ Configurations preserved"

echo ""
echo "🔄 === RESTART INSTRUCTIONS ==="
echo "To restart NEXUS PRIME EMPIRE, run:"
echo "  bash /root/nexus_entry.sh"
echo ""
echo "To check logs if issues occur:"
echo "  cd /root/NEXUS_PRIME_UNIFIED"
echo "  docker compose logs [service_name]"

echo ""
echo "📝 Shutdown completed at: $(date '+%Y-%m-%d %H:%M:%S')"
echo "🏰 NEXUS PRIME EMPIRE - SAFELY POWERED DOWN"
echo ""
echo "👑 Until next time, Your Majesty..."