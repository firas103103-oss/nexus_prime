#!/bin/bash
# NEXUS PRIME - Simple Monitoring Script

echo "🔍 NEXUS PRIME System Monitor"
echo "=============================="
echo ""

# Check Docker containers
echo "📦 Docker Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep nexus

echo ""

# Check disk space
echo "💽 Disk Space:"
df -h / | tail -1 | awk '{print "Used: "$3" / "$2" ("$5")"}'

echo ""

# Check memory
echo "🧠 Memory:"
free -h | grep Mem | awk '{print "Used: "$3" / "$2}'

echo ""

# Check ports
echo "🔌 Service Ports:"
for port in 3000 5432 5678 11434 5050 8001 8002 8003 8004 8005 8006 8007; do
    if nc -z localhost $port 2>/dev/null; then
        echo "  ✅ Port $port - Active"
    else
        echo "  ⚠️  Port $port - Inactive"
    fi
done
