#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# SOVEREIGN STACK LAUNCH — Full deployment with Bridge + Gateway
# ═══════════════════════════════════════════════════════════════════════
# Usage:
#   ./scripts/sovereign_launch.sh          # Launch sovereign stack
#   ./scripts/sovereign_launch.sh --msl    # Apply MSL schema first, then launch
#   ./scripts/sovereign_launch.sh --minimal # Bridge + Gateway only (requires db, nerve)
# ═══════════════════════════════════════════════════════════════════════

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

apply_msl() {
  echo "→ Applying MSL schema..."
  "$SCRIPT_DIR/db/apply_msl_schema.sh"
}

case "${1:-}" in
  --msl)
    apply_msl
    shift
    ;;
  --minimal)
    echo "→ Launching minimal sovereign stack (db, nerve, bridge, gateway)..."
    docker compose -f docker-compose.yml -f docker-compose.dify.yml up -d \
      nexus_db nexus_redis nexus_ollama nexus_litellm \
      nexus_cortex nexus_memory_keeper nexus_oracle \
      nexus_nerve sovereign_dify_bridge sovereign_gateway
    echo "Done. Dashboard: http://localhost:8888 | Gateway: http://localhost:9999"
    exit 0
    ;;
esac

echo "→ Launching full Sovereign stack..."
docker compose -f docker-compose.yml -f docker-compose.dify.yml up -d

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  SOVEREIGN STACK DEPLOYED"
echo "═══════════════════════════════════════════════════════════════"
echo "  Dashboard (Bridge):  http://localhost:8888"
echo "  Gateway (AS-SULTAN): http://localhost:9999"
echo "  God Mode (via GW):   http://localhost:9999/api/dify/god-mode"
echo "  Nerve:               http://localhost:8200"
echo "  Oracle:              http://localhost:8100"
echo "  Memory Keeper:       http://localhost:9000"
echo "═══════════════════════════════════════════════════════════════"
echo "  MSL schema not applied? Run: ./scripts/db/apply_msl_schema.sh"
echo "═══════════════════════════════════════════════════════════════"
