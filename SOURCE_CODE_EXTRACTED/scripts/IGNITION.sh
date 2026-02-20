#!/bin/bash
echo "🚀 NEXUS PRIME - IGNITION"
echo "═══════════════════════════════════════════════════════════"
cd /root/nexus_prime
docker-compose up -d
echo "✅ Services started!"
docker-compose ps
