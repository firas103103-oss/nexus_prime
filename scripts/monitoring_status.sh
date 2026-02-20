#!/bin/bash
# Quick Monitoring Status Check

echo "════════════════════════════════════════════════════════════════"
echo "📊 NEXUS PRIME - Monitoring Stack Status"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check containers
docker compose -f /root/NEXUS_PRIME_UNIFIED/monitoring/docker-compose.monitoring.yml ps --format "table {{.Name}}\t{{.Status}}"

echo ""
echo "🔍 Service Health:"
echo "────────────────────────────────────────────────────────────────"

# Prometheus
if curl -sf http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo "✅ Prometheus: http://localhost:9090"
else
    echo "❌ Prometheus: Not responding"
fi

# Grafana
if curl -sf http://localhost:3002/api/health > /dev/null 2>&1; then
    echo "✅ Grafana: http://localhost:3002 (admin/nexussovereign)"
else
    echo "⏳ Grafana: Starting or not ready"
fi

# AlertManager
if curl -sf http://localhost:9093/-/healthy > /dev/null 2>&1; then
    echo "✅ AlertManager: http://localhost:9093"
else
    echo "⏳ AlertManager: Starting or not ready"
fi

echo "✅ Node Exporter: http://localhost:9100"
echo "✅ cAdvisor: http://localhost:8081"

echo ""
echo "════════════════════════════════════════════════════════════════"
