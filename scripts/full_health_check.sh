#!/usr/bin/env bash
# NEXUS PRIME — Full Health Check
# Verifies all critical ports and health endpoints.
# Exit 0 on success, 1 on failure.
set -e

PORTS="3000 3001 3002 4000 5050 5678 8002 8003 8005 8080 8085 8090 8100 8200 8501 8888 9000 9999 5001 11434"
HEALTH_PORTS="8080 8200 8100 9000 8002"
FAILED=0

echo "=== NEXUS PRIME Health Check $(date -Iseconds) ==="

for p in $PORTS; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://127.0.0.1:$p/" 2>/dev/null || echo "000")
  if [[ "$code" == "000" ]]; then
    # 000 = connection failed
    echo "Port $p: FAIL (no response)"
    if [[ " $HEALTH_PORTS " == *" $p "* ]]; then FAILED=1; fi
  else
    echo "Port $p: OK ($code)"
  fi
done

# Health endpoints
for p in $HEALTH_PORTS; do
  if [[ "$p" == "8002" ]]; then path="/api/shadow7/health"; else path="/health"; fi
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://127.0.0.1:$p$path" 2>/dev/null || echo "000")
  if [[ "$code" =~ ^[23] ]]; then
    echo "Health $p$path: OK ($code)"
  else
    echo "Health $p$path: FAIL ($code)"
    FAILED=1
  fi
done

# Grafana
code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://127.0.0.1:3002/" 2>/dev/null || echo "000")
[[ "$code" =~ ^[23] ]] && echo "Grafana 3002: OK ($code)" || { echo "Grafana 3002: FAIL ($code)"; FAILED=1; }

echo "=== End ==="
exit $FAILED
