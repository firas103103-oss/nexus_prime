#!/usr/bin/env bash
# NEXUS PRIME — اختبارات التوافقية البرمجية والتقنية
# Compatibility Tests — Programmatic & Technical
set -e

PROJ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJ"

FAILED=0

echo "=== NEXUS PRIME Compatibility Tests $(date -Iseconds) ==="

# 1. Ethical Gate VOC
echo ""
echo "1. Ethical Gate VOC..."
python3 scripts/ethical_gate_voc_test.py || FAILED=1

# 2. Documentation Reality Verification
echo ""
echo "2. Documentation Reality..."
python3 scripts/verify_documentation_reality.py || FAILED=1

# 3. Clone Hub (integration)
echo ""
echo "3. Clone Hub (integration/clone-hub)..."
python3 integration/clone-hub/main.py >/dev/null 2>&1 || FAILED=1

# 4. Sovereign APIs compatibility
echo ""
echo "4. Sovereign APIs..."
for path in "/api/hormonal/status" "/api/systems/status" "/api/genome/entity/AS-SULTAN/llm-params"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://127.0.0.1:8888$path" 2>/dev/null || echo "000")
  if [[ "$code" =~ ^[23] ]]; then
    echo "   $path: OK ($code)"
  else
    echo "   $path: FAIL ($code)"
    FAILED=1
  fi
done

# 5. Gateway → Bridge proxy (when DIFY_BOARDROOM_ENABLED)
echo ""
echo "5. Gateway health..."
code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://127.0.0.1:9999/health" 2>/dev/null || echo "000")
[[ "$code" =~ ^[23] ]] && echo "   Gateway: OK ($code)" || { echo "   Gateway: FAIL ($code)"; FAILED=1; }

# 6. Nerve health
echo ""
echo "6. Nerve health..."
code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://127.0.0.1:8200/health" 2>/dev/null || echo "000")
[[ "$code" =~ ^[23] ]] && echo "   Nerve: OK ($code)" || { echo "   Nerve: FAIL ($code)"; FAILED=1; }

echo ""
echo "=== End ==="
exit $FAILED
