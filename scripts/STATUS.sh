#!/bin/bash
echo "📊 NEXUS PRIME - System Status"
echo "═══════════════════════════════════════════════════════════"
cd /root/nexus_prime
docker-compose ps
echo ""
echo "Disk Usage:"
df -h / | tail -1
