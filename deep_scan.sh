#!/bin/bash

# تنسيق الألوان
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}║          🔎 NEXUS PRIME: DEEP SYSTEM DIAGNOSTIC             ║${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo "Date: $(date)"
echo ""

# 1. فحص الموارد (Infrastructure Layer)
echo -e "${YELLOW}1. [INFRASTRUCTURE] Checking Server Resources...${NC}"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
RAM_USAGE=$(free -m | awk 'NR==2 {printf "%.2f%%", $3*100/$2 }')
echo -e "   • Disk Usage: $DISK_USAGE"
echo -e "   • RAM Usage:  $RAM_USAGE"
echo -e "   • Uptime:     $(uptime -p)"
echo ""

# 2. فحص الحاويات (Docker Layer)
echo -e "${YELLOW}2. [DOCKER] Checking Container Health...${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | while read line; do
  if [[ "$line" == *"Up"* ]]; then
    echo -e "${GREEN}   ✅ $line${NC}"
  elif [[ "$line" == *"Exited"* ]]; then
    echo -e "${RED}   ❌ $line${NC}"
  else
    echo -e "   $line"
  fi
done
echo ""

# 3. فحص الشبكة والدومينات (Network & SSL Layer)
echo -e "${YELLOW}3. [NETWORK] Checking Domains & SSL Handshake...${NC}"
check_url() {
  URL=$1
  NAME=$2
  # -sk: skip SSL verify (self-signed), --resolve avoids Cloudflare loop from server itself
  CODE=$(curl -sk --max-time 10 -o /dev/null -w "%{http_code}" "$URL")
  if [ "$CODE" == "200" ] || [ "$CODE" == "301" ] || [ "$CODE" == "302" ]; then
    echo -e "   ✅ $NAME ($URL) -> HTTP $CODE (Online)"
  else
    echo -e "   ❌ $NAME ($URL) -> HTTP $CODE (Check Logs!)"
  fi
}

check_url "https://ai.mrf103.com" "AI Interface"
check_url "https://flow.mrf103.com" "Workflow Engine"
check_url "https://voice.mrf103.com" "Voice Service"
check_url "https://admin.mrf103.com" "Imperial Dashboard"
echo ""

# 4. فحص المنطق الداخلي (Application Logic Layer)
echo -e "${YELLOW}4. [LOGIC] Testing Internal APIs...${NC}"

# فحص الدماغ (Ollama) - curl غير موجود داخل container، نستخدم host
echo -n "   • Testing Brain (Ollama Models)... "
if curl -s --max-time 5 http://localhost:11434/api/tags | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'PASSED ({len(d[\"models\"])} models: ' + ', '.join(m[\"name\"] for m in d[\"models\"]) + ')')" 2>/dev/null; then
    echo -e "${GREEN}(Brain is responding)${NC}"
else
    echo -e "${RED}FAILED (Brain not responding)${NC}"
fi

# فحص الحنجرة (Voice)
echo -n "   • Testing Voice (Edge-TTS)... "
if curl -s http://localhost:5050/health > /dev/null 2>&1 || curl -s http://localhost:5050/v1/models > /dev/null 2>&1; then
    echo -e "${GREEN}PASSED (Voice is ready)${NC}"
else
    echo -e "${RED}FAILED (Voice silent)${NC}"
fi

# 5. فحص البيانات (Data Layer)
echo -e "${YELLOW}5. [DATA] Checking Database Connection...${NC}"
echo -n "   • Connecting to PostgreSQL... "
if docker exec nexus_db psql -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}PASSED (Database active)${NC}"
else
    echo -e "${RED}FAILED (Connection refused)${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE} DIAGNOSTIC COMPLETE ${NC}"
