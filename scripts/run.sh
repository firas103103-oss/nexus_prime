#!/bin/bash
# NEXUS PRIME — Unified Entry Point
# Usage: ./run.sh {start|stop|status|restart}
# Manages the full docker-compose stack per 2026-02-24 Organizational Map

set -e
NEXUS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$NEXUS_DIR"

COMPOSE_OPTS="-f docker-compose.yml"
[ -f docker-compose.dify.yml ] && COMPOSE_OPTS="$COMPOSE_OPTS -f docker-compose.dify.yml"

case "${1:-status}" in
    start)
        echo "Starting NEXUS PRIME stack..."
        docker compose $COMPOSE_OPTS up -d
        echo "Run: ./scripts/run.sh status to verify"
        ;;
    stop)
        echo "Stopping NEXUS PRIME stack..."
        docker compose $COMPOSE_OPTS down
        ;;
    restart)
        echo "Restarting NEXUS PRIME stack..."
        docker compose $COMPOSE_OPTS restart
        ;;
    status)
        echo "NEXUS PRIME — Service Status"
        echo "============================"
        docker compose $COMPOSE_OPTS ps 2>/dev/null || true
        echo ""
        echo "Port checks:"
        for port_name in "3000:AI" "5001:Dashboard" "5678:n8n" "8200:Nerve" "8100:Oracle" "9999:Gateway" "11434:Ollama"; do
            port="${port_name%%:*}"
            name="${port_name##*:}"
            if curl -s -o /dev/null --connect-timeout 1 "http://localhost:$port" 2>/dev/null; then
                echo "  OK $port ($name)"
            else
                echo "  -- $port ($name)"
            fi
        done
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
