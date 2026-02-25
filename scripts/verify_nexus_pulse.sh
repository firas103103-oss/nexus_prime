
#!/bin/bash
# NEXUS PRIME — Pulse Verification
set -e
ok() { echo "✓ $1"; }
fail() { echo "✗ $1"; exit 1; }
echo "=== NEXUS PRIME Pulse ==="
systemctl is-enabled nginx >/dev/null 2>&1 && ok "Nginx" || fail "Nginx"
curl -sf https://api.mrf103.com/api/v1/health >/dev/null && ok "api" || fail "api"
curl -sf https://dashboard.mrf103.com/ -o /dev/null && ok "dashboard" || fail "dashboard"
curl -sf https://cortex.mrf103.com/health >/dev/null && ok "cortex" || fail "cortex"
curl -sf https://dify.mrf103.com/ -o /dev/null && ok "dify" || fail "dify"
echo "=== OK ==="

