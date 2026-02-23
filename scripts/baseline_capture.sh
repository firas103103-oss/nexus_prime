#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# NEXUS PRIME — Baseline Capture (المرحلة 0)
# يسجل الحالة الحالية قبل أي تعديل
# ═══════════════════════════════════════════════════════════════

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="${PROJECT_ROOT}/baselines"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/baseline_${TIMESTAMP}.txt"

mkdir -p "$OUTPUT_DIR"

{
  echo "═══════════════════════════════════════════════════════════"
  echo "NEXUS PRIME — Baseline Capture — $TIMESTAMP"
  echo "═══════════════════════════════════════════════════════════"
  echo ""

  echo "=== 1. Port Status ==="
  for p in 3000 3001 3002 4000 5050 5678 8002 8003 8005 8080 8085 8090 8100 8200 8501 8888 9000 9999 5001 11434; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://127.0.0.1:$p/" 2>/dev/null || echo "000")
    echo "  Port $p: $code"
  done
  echo ""

  echo "=== 2. Docker Containers ==="
  docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null | head -40
  echo ""

  echo "=== 3. Disk Usage (top dirs) ==="
  du -sh "$PROJECT_ROOT"/*/ 2>/dev/null | sort -hr | head -20
  echo ""

  echo "=== 4. Static Roots ==="
  for d in /var/www/nexus-landing /var/www/monitor /var/www/finance /var/www/marketing /var/www/nexus-platform /var/www/prime /root/products/shadow-seven-publisher/dist; do
    if [ -d "$d" ]; then
      echo "  $d: $(ls "$d" 2>/dev/null | wc -l) items"
    else
      echo "  $d: MISSING"
    fi
  done
  echo ""

  echo "=== 5. Health Endpoints ==="
  for url in "http://127.0.0.1:8888/health" "http://127.0.0.1:9999/health" "http://127.0.0.1:8200/health" "http://127.0.0.1:8090/health"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "$url" 2>/dev/null || echo "000")
    echo "  $url: $code"
  done

} | tee "$OUTPUT_FILE"

echo ""
echo "Baseline saved to: $OUTPUT_FILE"
