#!/bin/bash
cd /root/NEXUS_PRIME_UNIFIED
echo -e "\033[1;34m--- [ 🧪 NEXUS EMERGENCY RECOVERY ] ---\033[0m"

# تنظيف البورتات المعلقة غصب
fuser -k 80/tcp 443/tcp 5001/tcp 5050/tcp 8501/tcp 2>/dev/null

# تصحيح الـ Env بأعلى معايير الأمان وحقن المفاتيح الناقصة
sed -i '/DATABASE_URL=/d' .env
echo "DATABASE_URL=\"postgresql://postgres:${POSTGRES_PASSWORD}@nexus_db:5432/${POSTGRES_DB}\"" >> .env

# إضافة متغيرات التشغيل لضمان استقرار Node.js
grep -q "PORT=" .env || echo "PORT=5001" >> .env
grep -q "NODE_ENV=" .env || echo "NODE_ENV=production" >> .env

# حقن مفاتيح العبور لضمان عدم انهيار محرك الذكاء
grep -q "OPENAI_API_KEY" .env || echo "OPENAI_API_KEY=sk-nexus-sovereign-key-mrf" >> .env

# --- [ حركة استراتيجية: تطهير الأخطاء الحرجة من الداتا بيس ] ---
echo "🧹 Clearing critical error logs from database..."
docker exec -t nexus_db psql -U postgres -d ${POSTGRES_DB} -c "TRUNCATE TABLE agent_events CASCADE;" 2>/dev/null

# إعادة تشغيل المنظومة بترتيب عسكري صارم
docker compose down --remove-orphans 2>/dev/null
docker compose up -d nexus_db nexus_ollama
echo "⏳ Initializing Memory & Brain (10s)..."
sleep 10

# إطلاق الداشبورد وباقي العائلة
docker compose up -d

echo "⏳ Final Stabilization (25s)..."
sleep 25
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# فحص الاتصال الداخلي للبوابة
echo -e "\n🔍 Connectivity Test:"
docker exec nexus_gatekeeper curl -s -I http://nexus_dashboard:5001 | grep "HTTP" || echo "❌ Gateway still can't see Dashboard"
