#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS HIVE MIND AUTO-SYNC - Runs every hour
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/var/log/nexus_hive_sync.log"

echo "═══════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "🧠 HIVE SYNC STARTED: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

cd "$SCRIPT_DIR"

# Run the sync
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hive_mind import sync_collective_consciousness
count = sync_collective_consciousness()
print(f'Synced {count} wisdom points')
" >> "$LOG_FILE" 2>&1

echo "✅ HIVE SYNC COMPLETED: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "═══════════════════════════════════════════════════════════════" >> "$LOG_FILE"
