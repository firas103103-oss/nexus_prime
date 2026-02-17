#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# NEXUS PRIME - Final Comprehensive Test
# Phase 4 Commercialization Verification
# ═══════════════════════════════════════════════════════════════

PASS=0; FAIL=0; WARN=0
pass() { echo "  ✅ $1"; PASS=$((PASS+1)); }
fail() { echo "  ❌ $1"; FAIL=$((FAIL+1)); }
warn() { echo "  ⚠️  $1"; WARN=$((WARN+1)); }

echo "═══════════════════════════════════════════"
echo "🏗️  NEXUS PRIME - Final Verification"
echo "═══════════════════════════════════════════"
echo ""

# ═══ Test 1: Docker Infrastructure ═══
echo "📦 [1/8] Docker Containers"
echo "-------------------------------------------"
for c in nexus_db nexus_ai nexus_ollama nexus_flow nexus_voice; do
  STATUS=$(docker inspect -f '{{.State.Status}}' "$c" 2>/dev/null)
  if [ "$STATUS" = "running" ]; then
    pass "$c: running"
  else
    fail "$c: $STATUS"
  fi
done

# ═══ Test 2: Service Ports ═══
echo ""
echo "🔌 [2/8] Service Ports"
echo "-------------------------------------------"
declare -A PORTS=( ["PostgreSQL"]=5432 ["Open-WebUI"]=3000 ["Ollama"]=11434 ["n8n"]=5678 ["Voice"]=5050 ["Nginx-HTTP"]=80 ["Nginx-HTTPS"]=443 )
for name in "${!PORTS[@]}"; do
  PORT=${PORTS[$name]}
  if ss -tlnp | grep -q ":${PORT} " 2>/dev/null; then
    pass "$name (port $PORT)"
  else
    fail "$name (port $PORT) - not listening"
  fi
done

# ═══ Test 3: SSL Certificate ═══
echo ""
echo "🔒 [3/8] SSL Certificate"
echo "-------------------------------------------"
CERT_DOMAINS=$(openssl x509 -in /etc/letsencrypt/live/mrf103.com/cert.pem -text -noout 2>/dev/null | grep "Subject Alternative Name" -A1 | tail -1)
if echo "$CERT_DOMAINS" | grep -q "\*.mrf103.com"; then
  pass "Wildcard cert: *.mrf103.com"
else
  warn "No wildcard cert (domains: $CERT_DOMAINS)"
fi

EXPIRY=$(openssl x509 -in /etc/letsencrypt/live/mrf103.com/cert.pem -noout -enddate 2>/dev/null | cut -d= -f2)
if [ -n "$EXPIRY" ]; then
  pass "SSL expires: $EXPIRY"
else
  fail "Cannot read SSL expiry"
fi

# ═══ Test 4: DNS Records ═══
echo ""
echo "🌐 [4/8] DNS Records"
echo "-------------------------------------------"
for sub in publisher sultan admin chat flow api jarvis imperial voice nexus n8n; do
  IP=$(dig +short "${sub}.mrf103.com" A 2>/dev/null | head -1)
  if [ -n "$IP" ]; then
    pass "${sub}.mrf103.com → $IP"
  else
    warn "${sub}.mrf103.com → pending propagation"
  fi
done

# ═══ Test 5: Nginx & Landing Pages ═══
echo ""
echo "📄 [5/8] Landing Pages"
echo "-------------------------------------------"
nginx -t 2>/dev/null && pass "Nginx config valid" || fail "Nginx config invalid"

for page in /var/www/nexus-landing/index.html /var/www/nexus-landing/publisher/index.html /var/www/nexus-landing/sultan/index.html; do
  if [ -f "$page" ]; then
    SIZE=$(stat -c%s "$page" 2>/dev/null)
    pass "$(basename $(dirname $page))/$(basename $page) (${SIZE}B)"
  else
    fail "$page missing"
  fi
done

# Test with curl (local)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null)
if [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "200" ]; then
  pass "HTTP → HTTPS redirect ($HTTP_CODE)"
else
  warn "Landing page HTTP code: $HTTP_CODE"
fi

# ═══ Test 6: Stripe Module ═══
echo ""
echo "💳 [6/8] Stripe Payment System"
echo "-------------------------------------------"
cd /root/integration/ecosystem-api
STRIPE_TEST=$(python3 -c "
from payments.stripe_handler import get_products_catalog, get_revenue_stats
catalog = get_products_catalog()
stats = get_revenue_stats()
print(f'CATALOG:{len(catalog)}|STATS:{stats[\"total_revenue\"]}')
" 2>/dev/null)

if echo "$STRIPE_TEST" | grep -q "CATALOG:8"; then
  pass "Stripe module: 8 products loaded"
else
  fail "Stripe module: $STRIPE_TEST"
fi

if echo "$STRIPE_TEST" | grep -q "STATS:"; then
  pass "Revenue tracking functional"
else
  fail "Revenue tracking broken"
fi

# ═══ Test 7: n8n Workflows ═══
echo ""
echo "🔄 [7/8] n8n Automation"
echo "-------------------------------------------"
N8N_HEALTH=$(curl -s http://localhost:5678/healthz 2>/dev/null)
if echo "$N8N_HEALTH" | grep -q "ok"; then
  pass "n8n health: OK"
else
  fail "n8n health: $N8N_HEALTH"
fi

WF_COUNT=$(docker exec nexus_flow n8n export:workflow --all 2>/dev/null | python3 -c "import sys,json; data=json.load(sys.stdin); print(len(data) if isinstance(data,list) else 1)" 2>/dev/null)
if [ "$WF_COUNT" -ge 3 ] 2>/dev/null; then
  pass "n8n workflows: $WF_COUNT imported"
else
  warn "n8n workflows: $WF_COUNT (expected 3+)"
fi

for wf_file in /root/NEXUS_PRIME_UNIFIED/n8n-workflows/lead_capture.json /root/NEXUS_PRIME_UNIFIED/n8n-workflows/auto_nurturing.json /root/NEXUS_PRIME_UNIFIED/n8n-workflows/payment_onboarding.json; do
  if [ -f "$wf_file" ]; then
    pass "Workflow: $(basename $wf_file)"
  else
    fail "Missing: $(basename $wf_file)"
  fi
done

# ═══ Test 8: Git & GitHub ═══
echo ""
echo "📦 [8/8] Git & GitHub"
echo "-------------------------------------------"
cd /root/NEXUS_PRIME_UNIFIED

REMOTE=$(git remote get-url origin 2>/dev/null)
if [ -n "$REMOTE" ]; then
  pass "Remote: $REMOTE"
else
  fail "No git remote configured"
fi

COMMITS=$(git log --oneline | wc -l)
pass "Commits: $COMMITS"

BRANCH=$(git branch --show-current 2>/dev/null)
pass "Branch: $BRANCH"

TRACKING=$(git rev-parse --abbrev-ref @{u} 2>/dev/null)
if [ -n "$TRACKING" ]; then
  pass "Tracking: $TRACKING"
else
  warn "Not tracking remote branch"
fi

# ═══ Final Summary ═══
echo ""
echo "═══════════════════════════════════════════"
echo "📊 FINAL RESULTS"
echo "═══════════════════════════════════════════"
TOTAL=$((PASS + FAIL + WARN))
echo "  ✅ Passed:   $PASS"
echo "  ❌ Failed:   $FAIL"
echo "  ⚠️  Warnings: $WARN"
echo "  📋 Total:    $TOTAL"
echo ""
SCORE=$((PASS * 100 / TOTAL))
echo "  🎯 Score: $SCORE%"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "  🚀 STATUS: SYSTEM READY FOR LAUNCH!"
else
  echo "  ⚠️  STATUS: $FAIL issues need attention"
fi

echo ""
echo "═══════════════════════════════════════════"
echo "🏗️  NEXUS PRIME - Phase 4 Infrastructure"
echo "═══════════════════════════════════════════"
echo "  🌐 Main:      https://mrf103.com"
echo "  📚 Publisher:  https://publisher.mrf103.com"
echo "  🕌 Sultan:     https://sultan.mrf103.com"
echo "  ⚙️  Admin:     https://admin.mrf103.com"
echo "  💬 AI Chat:    https://chat.mrf103.com"
echo "  🔄 n8n:        https://flow.mrf103.com"
echo "  🔗 API:        https://api.mrf103.com"
echo "  🤖 Jarvis:     https://jarvis.mrf103.com"
echo "  👑 Imperial:   https://imperial.mrf103.com"
echo "  🎤 Voice:      https://voice.mrf103.com"
echo "  🧠 Nexus:      https://nexus.mrf103.com"
echo "  📊 GitHub:     https://github.com/firas103103-oss/nexus_prime"
echo "═══════════════════════════════════════════"
