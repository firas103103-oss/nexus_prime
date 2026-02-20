#!/bin/bash
# ============================================
# NEXUS PRIME - n8n Workflow Deployment Script
# Imports all workflows into running n8n instance
# ============================================

set -e

N8N_URL="${N8N_URL:-http://localhost:5678}"
N8N_USER="${N8N_USER:-admin}"
N8N_PASS="${N8N_PASS:-nexus_mrf_flow_2026}"
WORKFLOW_DIR="/root/NEXUS_PRIME_UNIFIED/n8n-workflows"

echo "============================================"
echo "🔄 NEXUS n8n Workflow Deployment"
echo "============================================"

# Step 1: Get auth cookie
echo ""
echo "🔐 Authenticating with n8n..."

LOGIN_RESPONSE=$(curl -s -c /tmp/n8n_cookies.txt \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${N8N_USER}\",\"password\":\"${N8N_PASS}\"}" \
  "${N8N_URL}/api/v1/login" 2>/dev/null || echo "FAIL")

if echo "$LOGIN_RESPONSE" | grep -q "FAIL\|error\|Error"; then
  echo "⚠️  Cookie auth failed, trying API key..."
  
  # Try owner setup check
  SETUP=$(curl -s "${N8N_URL}/api/v1/owner/setup" 2>/dev/null || echo "")
  
  if echo "$SETUP" | grep -q "false"; then
    echo "📝 n8n needs initial setup. Setting up owner..."
    SETUP_RESP=$(curl -s -c /tmp/n8n_cookies.txt \
      -H "Content-Type: application/json" \
      -d "{\"email\":\"admin@mrf103.com\",\"password\":\"${N8N_PASS}\",\"firstName\":\"NEXUS\",\"lastName\":\"Admin\"}" \
      "${N8N_URL}/api/v1/owner/setup" 2>/dev/null || echo "FAIL")
    
    if echo "$SETUP_RESP" | grep -q "FAIL"; then
      echo "❌ Setup failed. Using direct import method..."
    else
      echo "✅ Owner setup complete"
      # Re-login
      curl -s -c /tmp/n8n_cookies.txt \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"admin@mrf103.com\",\"password\":\"${N8N_PASS}\"}" \
        "${N8N_URL}/api/v1/login" 2>/dev/null
    fi
  fi
else
  echo "✅ Authenticated"
fi

AUTH_HEADER="-b /tmp/n8n_cookies.txt"

# Step 2: Import workflows
echo ""
echo "📦 Importing workflows..."
echo "--------------------------------------------"

SUCCESS=0
FAIL=0

for wf_file in "$WORKFLOW_DIR"/*.json; do
  if [ ! -f "$wf_file" ]; then
    continue
  fi
  
  WF_NAME=$(basename "$wf_file" .json)
  echo -n "  📋 $WF_NAME... "
  
  # Import via API
  IMPORT_RESP=$(curl -s $AUTH_HEADER \
    -X POST \
    -H "Content-Type: application/json" \
    -d @"$wf_file" \
    "${N8N_URL}/api/v1/workflows" 2>/dev/null || echo "FAIL")
  
  if echo "$IMPORT_RESP" | grep -q '"id"'; then
    WF_ID=$(echo "$IMPORT_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','?'))" 2>/dev/null || echo "?")
    echo "✅ (ID: $WF_ID)"
    
    # Activate the workflow
    ACTIVATE_RESP=$(curl -s $AUTH_HEADER \
      -X PATCH \
      -H "Content-Type: application/json" \
      -d '{"active": true}' \
      "${N8N_URL}/api/v1/workflows/${WF_ID}" 2>/dev/null || echo "")
    
    if echo "$ACTIVATE_RESP" | grep -q '"active":true'; then
      echo "    🟢 Activated"
    else
      echo "    🟡 Imported (activate manually)"
    fi
    
    SUCCESS=$((SUCCESS + 1))
  else
    echo "⚠️  API import failed, saving for manual import"
    FAIL=$((FAIL + 1))
  fi
done

# Step 3: Summary
echo ""
echo "============================================"
echo "📊 Deployment Summary"
echo "============================================"
echo "  ✅ Imported: $SUCCESS"
echo "  ⚠️  Manual:   $FAIL"
echo ""

if [ $FAIL -gt 0 ]; then
  echo "📝 Manual Import Instructions:"
  echo "  1. Open https://flow.mrf103.com or http://localhost:5678"
  echo "  2. Go to Workflows → Import from File"
  echo "  3. Import each JSON file from: $WORKFLOW_DIR/"
  echo ""
fi

# Step 4: List existing workflows
echo "📋 Current n8n Workflows:"
WORKFLOWS=$(curl -s $AUTH_HEADER "${N8N_URL}/api/v1/workflows" 2>/dev/null || echo "")
if echo "$WORKFLOWS" | grep -q '"data"'; then
  echo "$WORKFLOWS" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    workflows = data.get('data', [])
    for wf in workflows:
        status = '🟢' if wf.get('active') else '⚪'
        print(f\"  {status} [{wf.get('id','?')}] {wf.get('name','Unknown')}\")
    print(f\"\n  Total: {len(workflows)} workflows\")
except:
    print('  (Could not parse response)')
" 2>/dev/null || echo "  (Could not list workflows)"
else
  echo "  (Could not fetch workflows)"
fi

echo ""
echo "🔗 n8n Dashboard: ${N8N_URL}"
echo "============================================"
