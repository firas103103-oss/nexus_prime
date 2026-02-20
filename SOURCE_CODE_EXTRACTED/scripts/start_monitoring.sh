#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 📊 NEXUS PRIME - Start Monitoring Stack
# ═══════════════════════════════════════════════════════════════════════════

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${BLUE}📊 NEXUS PRIME - Starting Monitoring Stack${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

cd /root/NEXUS_PRIME_UNIFIED/monitoring

echo -e "${BLUE}1️⃣ Creating necessary directories...${NC}"
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p grafana/dashboards

echo -e "${BLUE}2️⃣ Starting monitoring services...${NC}"
docker compose -f docker-compose.monitoring.yml up -d

echo ""
echo -e "${BLUE}3️⃣ Waiting for services to be ready...${NC}"
sleep 10

echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Monitoring Stack Started!${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📊 Access Points:"
echo -e "   • Grafana:     ${YELLOW}http://localhost:3001${NC}"
echo -e "                  Username: ${GREEN}admin${NC}"
echo -e "                  Password: ${GREEN}nexussovereign${NC}"
echo ""
echo -e "   • Prometheus:  ${YELLOW}http://localhost:9090${NC}"
echo -e "   • AlertManager:${YELLOW}http://localhost:9093${NC}"
echo -e "   • Node Exporter: ${YELLOW}http://localhost:9100/metrics${NC}"
echo -e "   • cAdvisor:    ${YELLOW}http://localhost:8080${NC}"
echo ""
echo "🔍 Check status:"
echo "   docker compose -f monitoring/docker-compose.monitoring.yml ps"
echo ""
echo "📋 View logs:"
echo "   docker logs nexus_grafana -f"
echo "   docker logs nexus_prometheus -f"
echo ""
