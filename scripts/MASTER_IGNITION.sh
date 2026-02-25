#!/bin/bash
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}║    🚀 NEXUS PRIME: MASTER IGNITION PROTOCOL (DEPLOYMENT)    ║${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

# إعداد المسارات
BASE_DIR="/root/NEXUS_PRIME_UNIFIED"
PRODUCTS_DIR="/root/products"
NGINX_CONF="/root/nexus_prime/npm_data/nginx/proxy_host/nexus_prime_unified.conf"

mkdir -p "$PRODUCTS_DIR"

# =========================================================
# المرحلة 1: الحصاد والتجهيز (Harvest & Prep)
# =========================================================
echo -e "${YELLOW}[1] Harvesting Sovereign Systems...${NC}"

# 1. استخراج وتجهيز X-BIO Boardroom
BOARDROOM_DEST="$PRODUCTS_DIR/cognitive-boardroom"
mkdir -p "$BOARDROOM_DEST"
# البحث عن الكود الأصلي ونسخه
SOURCE_BOARDROOM=$(find /root -name "main.py" | grep "xbio-sovereign" | head -n 1)
if [ -f "$SOURCE_BOARDROOM" ]; then
    cp "$SOURCE_BOARDROOM" "$BOARDROOM_DEST/main.py"
    echo "   ✅ Boardroom Logic Extracted."
    
    # إنشاء Dockerfile للـ Boardroom
    cat << 'DOCKER' > "$BOARDROOM_DEST/Dockerfile"
FROM python:3.11-slim
WORKDIR /app
RUN pip install streamlit openai psycopg2-binary python-dotenv pandas
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
DOCKER
else
    echo "   ⚠️ Boardroom source not found (Check Archives)."
fi

# =========================================================
# المرحلة 2: دمج الخدمات في الدستور (Docker Compose Merge)
# =========================================================
echo -e "${YELLOW}[2] Merging Services into Infrastructure...${NC}"

# سنقوم بإضافة خدمة Boardroom إلى ملف الكومبوز الحالي
# (نقوم بذلك عبر Append ذكي لضمان عدم تخريب الموجود)

COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

# التحقق مما إذا كانت الخدمة مضافة مسبقاً لتجنب التكرار
if ! grep -q "nexus_boardroom:" "$COMPOSE_FILE"; then
cat << 'SERVICE' >> "$COMPOSE_FILE"

  # --- كوكب الاجتماعات: X-BIO Boardroom ---
  nexus_boardroom:
    build: /root/products/cognitive-boardroom
    container_name: nexus_boardroom
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@nexus_db:5432/${POSTGRES_DB}
      - TZ=${TZ}
    networks:
      - nexus_network
    restart: always
SERVICE
    echo "   ✅ Nexus Boardroom Service Added to Compose."
else
    echo "   ℹ️ Nexus Boardroom already in Compose."
fi

# =========================================================
# المرحلة 3: تحديث الحارس (Gatekeeper Re-Wiring)
# =========================================================
echo -e "${YELLOW}[3] Updating Gatekeeper (Nginx) Configuration...${NC}"

# إضافة إعدادات Boardroom إلى الملف الموحد
if ! grep -q "boardroom.mrf103.com" "$NGINX_CONF"; then
cat << 'NGINX' >> "$NGINX_CONF"

# كوكب الاجتماعات Boardroom
server {
    listen 80;
    server_name boardroom.mrf103.com;
    location / { return 301 https://$host$request_uri; }
}
server {
    listen 443 ssl;
    http2 on;
    server_name boardroom.mrf103.com;
    # نستخدم نفس شهادة الـ Wildcard الموجودة
    ssl_certificate /etc/letsencrypt/live/ai.mrf103.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ai.mrf103.com/privkey.pem;
    
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://nexus_boardroom:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX
    echo "   ✅ Boardroom Domain Routing Added."
else
    echo "   ℹ️ Boardroom Routing already exists."
fi

# =========================================================
# المرحلة 4: الإقلاع والتفعيل (Ignition)
# =========================================================
echo -e "${YELLOW}[4] IGNITING SYSTEMS...${NC}"

# إعادة بناء وتشغيل الحاويات المحدثة فقط
cd "$BASE_DIR"
docker compose up -d --build

# إعادة تحميل Nginx
docker exec nexus_gatekeeper nginx -t && \
docker exec nexus_gatekeeper nginx -s reload

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ MISSION ACCOMPLISHED: SYSTEM EXPANDED${NC}"
echo -e "   🌐 New Planet Active: https://boardroom.mrf103.com"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
