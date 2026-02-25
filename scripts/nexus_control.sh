#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 🔱 NEXUS CONTROL - Quick Access to Sovereign Terminal
# ═══════════════════════════════════════════════════════════════════════════════
# Usage: ./nexus_control.sh [command]
#   No args     → Opens interactive terminal
#   sync        → Run hive mind sync
#   pulse       → Quick pulse check
#   status      → Quick status
# ═══════════════════════════════════════════════════════════════════════════════

NEXUS_DIR="/root/NEXUS_PRIME_UNIFIED"
MIDDLEWARE_DIR="$NEXUS_DIR/nexus_middleware"

cd "$NEXUS_DIR"
export PYTHONPATH="$NEXUS_DIR:$PYTHONPATH"

case "${1:-interactive}" in
    sync)
        echo "🧠 Running Hive Mind Sync..."
        python3 -c "
import sys
sys.path.insert(0, '$MIDDLEWARE_DIR')
from hive_mind import sync_collective_consciousness
sync_collective_consciousness()
"
        ;;
    pulse)
        echo "📡 Checking System Pulse..."
        python3 -c "
import asyncio
import sys
sys.path.insert(0, '$MIDDLEWARE_DIR')
from connector import get_connector

async def check():
    c = get_connector()
    result = await c.get_system_pulse()
    print(result)

asyncio.run(check())
"
        ;;
    status)
        echo "📊 NEXUS Status:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Check Docker containers
        echo "🐳 Docker Containers:"
        docker ps --format "   {{.Names}}: {{.Status}}" 2>/dev/null | grep nexus | head -10
        
        # Check Hive Mind
        echo ""
        echo "🧠 Hive Mind Status:"
        if [ -f "$NEXUS_DIR/GLOBAL_HIVE_MEMORY.json" ]; then
            entries=$(cat "$NEXUS_DIR/GLOBAL_HIVE_MEMORY.json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('total_wisdom_points', 0))" 2>/dev/null || echo "0")
            echo "   Wisdom Points: $entries"
        else
            echo "   Not synced yet. Run: $0 sync"
        fi
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ;;
    interactive|*)
        # Launch interactive terminal
        python3 "$MIDDLEWARE_DIR/mrf_control.py"
        ;;
esac
