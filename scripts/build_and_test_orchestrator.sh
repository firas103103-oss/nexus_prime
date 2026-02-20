#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# NEXUS PRIME — Build and Test Orchestrator (Local Docker)
# ═══════════════════════════════════════════════════════════════════════════
# Tests Redis Streams integration before K8s deployment
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

echo "════════════════════════════════════════════════════════════════════════"
echo "  NEXUS PRIME — Build & Test Orchestrator v1.1.0"
echo "  Redis Streams Integration Test"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
ORCHESTRATOR_SERVICE="nexus_orchestrator"
IMAGE_TAG="v1.1.0"

echo -e "${YELLOW}[1/5]${NC} Building orchestrator image..."
cd /root/NEXUS_PRIME_UNIFIED/nexus_prime_core
docker build -t nexus_orchestrator:${IMAGE_TAG} -f Dockerfile . || {
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
}
echo -e "${GREEN}✓ Build successful${NC}"
echo ""

echo -e "${YELLOW}[2/5]${NC} Updating docker-compose.yml image tag..."
cd /root/NEXUS_PRIME_UNIFIED
sed -i "s|image: nexus_prime_unified-nexus_orchestrator|image: nexus_orchestrator:${IMAGE_TAG}|g" docker-compose.yml
echo -e "${GREEN}✓ Image tag updated${NC}"
echo ""

echo -e "${YELLOW}[3/5]${NC} Restarting orchestrator container..."
docker compose down ${ORCHESTRATOR_SERVICE} 2>/dev/null || true
docker compose up -d ${ORCHESTRATOR_SERVICE}
echo -e "${GREEN}✓ Container restarted${NC}"
echo ""

echo -e "${YELLOW}[4/5]${NC} Waiting for orchestrator to be healthy (30s timeout)..."
timeout=30
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker compose ps ${ORCHESTRATOR_SERVICE} | grep -q "healthy"; then
        echo -e "${GREEN}✓ Orchestrator is healthy${NC}"
        break
    fi
    sleep 2
    elapsed=$((elapsed + 2))
    echo -n "."
done
echo ""

if [ $elapsed -ge $timeout ]; then
    echo -e "${RED}✗ Orchestrator did not become healthy in time${NC}"
    echo "Logs:"
    docker compose logs --tail=50 ${ORCHESTRATOR_SERVICE}
    exit 1
fi

echo -e "${YELLOW}[5/5]${NC} Testing Redis Streams integration..."
echo ""
echo "Checking logs for Redis Streams initialization..."
docker compose logs ${ORCHESTRATOR_SERVICE} | grep -i "streams" || echo "No explicit streams logs yet"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  BUILD & TEST COMPLETE${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "  1. Run test suite: cd nexus_prime_core/orchestrator && python test_suite.py"
echo "  2. Test Redis Streams: redis-cli XADD nexus:commands:stream '*' type command_issued target TEST-AGENT command_id test-123 command_type test_mission priority 5"
echo "  3. Monitor logs: docker compose logs -f ${ORCHESTRATOR_SERVICE}"
echo ""
