#!/bin/bash
# ============================================
# NEXUS PRIME - Cloudflare DNS Setup Script
# Creates A records for all subdomains
# ============================================

CF_TOKEN="NTf2k_LX2NykdvAI78ClVO1NTojmYQoQZJEgpNDX"
ZONE_ID="156bc9bdda82a4c6d357dbf5578d4845"
SERVER_IP="46.224.225.96"

# Subdomains to create
SUBDOMAINS="publisher sultan admin chat flow api jarvis imperial voice nexus n8n dash data"

echo "============================================"
echo "🌐 NEXUS DNS Setup - Cloudflare"
echo "============================================"
echo "Zone: mrf103.com ($ZONE_ID)"
echo "Server IP: $SERVER_IP"
echo ""

# First, list existing DNS records
echo "📋 Current DNS Records:"
echo "--------------------------------------------"
EXISTING=$(curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=A&per_page=100" 2>/dev/null)

echo "$EXISTING" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('result', []):
    proxy = '🟠 Proxied' if r.get('proxied') else '⚪ DNS only'
    print(f'  {r[\"name\"]:30s} → {r[\"content\"]:16s} {proxy}  (ID: {r[\"id\"]})')
" 2>/dev/null

echo ""
echo "🔧 Adding missing subdomains..."
echo "--------------------------------------------"

SUCCESS=0
SKIP=0
FAIL=0

for SUB in $SUBDOMAINS; do
  FULL="${SUB}.mrf103.com"
  
  # Check if record already exists
  EXISTS=$(echo "$EXISTING" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('result', []):
    if r['name'] == '$FULL':
        print(r['id'])
        break
" 2>/dev/null)

  if [ -n "$EXISTS" ]; then
    echo "  ⏭️  $FULL already exists (ID: $EXISTS)"
    SKIP=$((SKIP + 1))
    continue
  fi

  # Create A record (DNS-only for SSL cert - not proxied since we have our own SSL)
  RESULT=$(curl -s -X POST \
    -H "Authorization: Bearer $CF_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"type\":\"A\",\"name\":\"$SUB\",\"content\":\"$SERVER_IP\",\"ttl\":1,\"proxied\":false}" \
    "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" 2>/dev/null)

  if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('success') else 1)" 2>/dev/null; then
    echo "  ✅ $FULL → $SERVER_IP (DNS-only)"
    SUCCESS=$((SUCCESS + 1))
  else
    ERROR=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('errors',[{}])[0].get('message','unknown'))" 2>/dev/null)
    echo "  ❌ $FULL - Error: $ERROR"
    FAIL=$((FAIL + 1))
  fi
  
  sleep 0.5
done

echo ""
echo "============================================"
echo "📊 DNS Setup Summary"
echo "============================================"
echo "  ✅ Created: $SUCCESS"
echo "  ⏭️  Existed: $SKIP"
echo "  ❌ Failed:  $FAIL"
echo ""
echo "🔍 Verification (may take 1-2 minutes to propagate):"
for SUB in "" $SUBDOMAINS; do
  FULL="${SUB:+$SUB.}mrf103.com"
  IP=$(dig +short "$FULL" A 2>/dev/null | head -1)
  echo "  $FULL → ${IP:-pending...}"
done
echo "============================================"
