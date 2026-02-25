#!/bin/bash
# 🎮 NEXUS PRIME - المرجع السريع
# Quick Reference & Control Panel

echo "🏰 NEXUS PRIME EMPIRE - QUICK CONTROL PANEL"
echo "=========================================="
echo ""
echo "📊 Current System Status:"

# Quick status check
services=(
    "3000:AI Interface"
    "5001:Dashboard"
    "5050:Voice Service" 
    "5678:Flow Automation"
    "8080:XBio Vault"
    "8501:Cognitive Boardroom"
    "9000:Jarvis Memory"
    "11434:Ollama Engine"
)

echo "🌐 Port Status Check:"
for service in "${services[@]}"; do
    port=${service%%:*}
    name=${service##*:}
    if curl -s -o /dev/null --connect-timeout 1 --max-time 2 http://localhost:$port 2>/dev/null; then
        echo "  ✅ $name (Port $port)"
    else
        echo "  ❌ $name (Port $port)"
    fi
done

echo ""
echo "🐳 Docker Containers:"
cd "$(dirname "$0")/.." 2>/dev/null && docker compose ps --format "table {{.Name}}\t{{.State}}" 2>/dev/null || echo "  ℹ️ NEXUS_PRIME_UNIFIED not accessible"

echo ""
echo "⚡ System Resources:"
echo "  💾 Disk: $(df -h / | awk 'NR==2 {print $5 " used of " $2}')"
echo "  🧠 Memory: $(free -h | awk 'NR==2{printf "%s used of %s (%.1f%%)\n", $3, $2, $3/$2*100}')"
echo "  📊 Load: $(uptime | awk -F'load average:' '{print $2}')"

echo ""
echo "🎮 CONTROL OPTIONS:"
echo "=========================================="
echo ""
echo "🚀 STARTUP COMMANDS:"
echo "  1. Full System Start:     bash /root/nexus_entry.sh"
echo "  2. Quick Start (Docker):  cd /root/NEXUS_PRIME_UNIFIED && docker compose up -d"
echo "  3. Database Only:         cd /root/NEXUS_PRIME_UNIFIED && docker compose up nexus_db -d"
echo "  4. AI Core Only:          cd /root/NEXUS_PRIME_UNIFIED && docker compose up nexus_ai nexus_ollama -d"
echo ""
echo "🛑 SHUTDOWN COMMANDS:"
echo "  1. Safe Full Shutdown:    bash /root/nexus_exit.sh"
echo "  2. Quick Stop (Docker):   cd /root/NEXUS_PRIME_UNIFIED && docker compose down"
echo "  3. Emergency Stop:        docker stop \$(docker ps -q)"
echo ""
echo "🔧 MAINTENANCE COMMANDS:"
echo "  1. Restart Service:       cd /root/NEXUS_PRIME_UNIFIED && docker compose restart [service_name]"
echo "  2. View Logs:            cd /root/NEXUS_PRIME_UNIFIED && docker compose logs [service_name]"
echo "  3. Update System:        cd /root/NEXUS_PRIME_UNIFIED && docker compose pull && docker compose up -d"
echo "  4. Backup Database:      cd /root/NEXUS_PRIME_UNIFIED && docker compose exec nexus_db pg_dump -U postgres nexus_db > backup.sql"
echo ""
echo "📊 MONITORING COMMANDS:"
echo "  1. Port Status:          bash /root/nexus_status.sh"
echo "  2. Docker Status:        cd /root/NEXUS_PRIME_UNIFIED && docker compose ps"
echo "  3. System Resources:     htop"
echo "  4. Network Connections:  ss -tuln | grep LISTEN"
echo ""
echo "🌐 QUICK ACCESS URLS:"
echo "  • AI Interface:          http://localhost:3000"
echo "  • Main Dashboard:        http://localhost:5001"
echo "  • Flow Automation:       http://localhost:5678"
echo "  • XBio Vault:           http://localhost:8080"
echo "  • Cognitive Boardroom:   http://localhost:8501"
echo "  • Ollama API:           http://localhost:11434"
echo ""
echo "📈 BUSINESS COMMANDS:"
echo "  1. Revenue Calculator:   echo 'NEXUS AI: \$15K + XBio: \$25K + Boardroom: \$25K + Others: \$45K = \$110K/month'"
echo "  2. Customer Report:      find /root -name '*customer*' -o -name '*client*' -type f 2>/dev/null"
echo "  3. Performance Report:   bash /root/nexus_performance.sh 2>/dev/null || echo 'Performance script not found'"
echo ""
echo "🆘 EMERGENCY COMMANDS:"
echo "  1. Kill All Processes:   pkill -f nexus; pkill -f jarvis; docker stop \$(docker ps -q)"
echo "  2. Emergency Backup:     tar -czf /root/emergency_backup_\$(date +%Y%m%d_%H%M).tar.gz /root/NEXUS_PRIME_UNIFIED"
echo "  3. System Restore:       bash /root/emergency_restore.sh 2>/dev/null || echo 'Restore script not found'"
echo ""
echo "💡 TIPS:"
echo "  • Always use nexus_entry.sh for startup (safer than docker compose up)"
echo "  • Use nexus_exit.sh for shutdown (includes backup)"
echo "  • Monitor logs regularly: docker compose logs -f [service_name]"
echo "  • Keep backups: Database is backed up to /root/nexus_prime_backups/"
echo ""
echo "🎯 For detailed documentation, see:"
echo "  • Entry/Exit Plan: /root/ENTRY_EXIT_STRATEGY.md"
echo "  • System Report: /root/SYSTEM_SYNCHRONIZATION_REPORT.md"
echo "  • Test Results: /root/SYSTEM_TEST_RESULTS.md"
echo ""
echo "👑 NEXUS PRIME EMPIRE - READY FOR YOUR COMMAND!"