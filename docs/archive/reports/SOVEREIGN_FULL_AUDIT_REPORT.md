# كشف شامل — 46.224.225.96 / mrf103.com

**التاريخ:** 2026-02-23  
**السيرفر:** 46.224.225.96  
**الدومين:** mrf103.com (Cloudflare)

---

## 1. مصفوفة المنافذ والخدمات

| المنفذ | الخدمة | الحاوية | الحالة | الدومين |
|--------|--------|---------|--------|----------|
| 3000 | Open WebUI (AI Chat) | nexus_ai | ✅ | chat.mrf103.com, nexus.mrf103.com, ai.mrf103.com |
| 4000 | LiteLLM | nexus_litellm | ⚠️ | — |
| 5050 | Edge-TTS | nexus_voice | ✅ | voice.mrf103.com |
| 5678 | n8n | nexus_flow | ✅ | flow.mrf103.com, n8n.mrf103.com |
| 6379 | Redis | nexus_redis | ✅ | — |
| 8002 | Shadow7 API | shadow7_api | ✅ | publisher.mrf103.com |
| 8003 | Auth | nexus_auth | ✅ | — |
| 8090 | Cortex | nexus_cortex | ✅ | cortex.mrf103.com |
| 8100 | Oracle | nexus_oracle | ✅ | oracle.mrf103.com |
| 8200 | Nerve | nexus_nerve | ✅ | nerve.mrf103.com |
| 8501 | Boardroom | nexus_boardroom | ✅ | boardroom.mrf103.com |
| 8888 | **Sovereign Bridge** | sovereign_dify_bridge | ✅ | sovereign.mrf103.com, god.mrf103.com |
| 9000 | Memory Keeper | nexus_memory_keeper | ✅ | memory.mrf103.com |
| 9001 | Memory Keeper UI | nexus_memory_keeper | ✅ | — |
| 9999 | **Gateway (AS-SULTAN)** | sovereign_gateway | ✅ | gateway.mrf103.com |
| 8085 | **Dify** | dify-nginx | ✅ | dify.mrf103.com |
| 5001 | Nexus Dashboard | nexus_dashboard | ✅ | dashboard.mrf103.com |
| 11434 | Ollama | nexus_ollama | ✅ | — |

---

## 2. الناقص وغير المربوط

### ✅ Sovereign OS Dashboard (8888) — تم الإصلاح
- **تم إضافة:** sovereign.mrf103.com و god.mrf103.com → 127.0.0.1:8888 في nginx

### ✅ Gateway (9999) — تم الإصلاح
- **تم إضافة:** gateway.mrf103.com → 127.0.0.1:9999 في nginx
- **ملاحظة:** sultan.mrf103.com يبقى للاندينج + API 8005؛ استخدم gateway.mrf103.com للـ AS-SULTAN Gateway

### ✅ Dify — تم النصب
- **الحالة:** منصب ويعمل على المنفذ 8085
- **الدومين:** dify.mrf103.com
- **التشغيل:** `./scripts/dify_launch.sh`

### ❌ خدمات خارج docker-compose الرئيسي
| الخدمة | المنفذ | الملف | الحالة |
|--------|--------|-------|--------|
| Ecosystem API | 8005 | خارج compose | يُستخدم من nginx |
| Grafana | 3002 | monitoring/docker-compose.monitoring.yml | منفصل |
| X-Bio Sentinel | 8080 | غير في compose الرئيسي | xbio.mrf103.com |

---

## 3. الداشبوردات والواجهات

| الداشبورد | الرابط المباشر | الرابط عبر الدومين |
|-----------|----------------|---------------------|
| **Sovereign OS (God Mode)** | http://46.224.225.96:8888 | https://sovereign.mrf103.com أو https://god.mrf103.com |
| **God Mode عبر Gateway** | http://46.224.225.96:9999/api/dify/god-mode | https://gateway.mrf103.com/api/dify/god-mode |
| **Boardroom** | http://46.224.225.96:8501 | https://boardroom.mrf103.com |
| **Nexus Dashboard** | http://46.224.225.96:5001 | https://dashboard.mrf103.com |
| **Open WebUI** | http://46.224.225.96:3000 | https://chat.mrf103.com |
| **n8n** | http://46.224.225.96:5678 | https://flow.mrf103.com |
| **Memory Keeper** | http://46.224.225.96:9000 | http://memory.mrf103.com (80 فقط) |
| **Nerve** | http://46.224.225.96:8200 | https://nerve.mrf103.com |
| **Oracle** | http://46.224.225.96:8100 | https://oracle.mrf103.com |
| **Cortex** | http://46.224.225.96:8090 | https://cortex.mrf103.com |
| **Dify** | http://46.224.225.96:8085 | https://dify.mrf103.com |

---

## 4. تعليمات التشغيل

### تشغيل الـ Sovereign Stack
```bash
cd /root/NEXUS_PRIME_UNIFIED
./scripts/sovereign_launch.sh
```

### تشغيل مع MSL Schema
```bash
./scripts/sovereign_launch.sh --minimal  # أو --msl
```

### تطبيق MSL + Analytics Schema
```bash
./scripts/db/apply_msl_schema.sh
```

### التحقق من الحالة
```bash
docker compose -f docker-compose.yml -f docker-compose.dify.yml ps
curl -s http://localhost:8888/health
curl -s http://localhost:9999/health
```

---

## 5. إصلاحات Nginx — تم تنفيذها ✅

تم إضافة البلوكات التالية في `nginx/nexus_unified.conf`:
- **sovereign.mrf103.com** و **god.mrf103.com** → 8888 (Sovereign OS Dashboard)
- **gateway.mrf103.com** → 9999 (AS-SULTAN Gateway)
- **dify.mrf103.com** → 8085 (Dify)

**لتطبيق التغييرات على السيرفر:**
```bash
sudo cp /root/NEXUS_PRIME_UNIFIED/nginx/nexus_unified.conf /etc/nginx/sites-available/nexus_unified
sudo nginx -t && sudo systemctl reload nginx
```
*(تم تنفيذها على السيرفر)*

---

## 6. Dify — منصب ومربوط ✅

```bash
./scripts/dify_launch.sh
```

- **الوصول:** https://dify.mrf103.com أو http://localhost:8085
- **أول تشغيل:** افتح /install لإنشاء حساب الأدمن
- **LiteLLM:** Dify يستخدم nexus_litellm (Ollama) تلقائياً
- **ربط Bridge:** بعد إنشاء workflow في Dify، ضع DIFY_API_KEY و DIFY_DEFENSIVE_WORKFLOW_ID في .env

---

## 7. ملخص الروابط (بعد التحديث)

| الخدمة | localhost | mrf103.com |
|--------|-----------|------------|
| Sovereign Dashboard | :8888 | sovereign.mrf103.com, god.mrf103.com ✅ |
| Gateway | :9999 | gateway.mrf103.com ✅ |
| Boardroom | :8501 | boardroom.mrf103.com ✅ |
| Dashboard | :5001 | dashboard.mrf103.com ✅ |
| Chat | :3000 | chat.mrf103.com ✅ |
| Nerve | :8200 | nerve.mrf103.com ✅ |
| Oracle | :8100 | oracle.mrf103.com ✅ |
| Memory | :9000 | memory.mrf103.com ✅ |
| Cortex | :8090 | cortex.mrf103.com ✅ |
| Dify | :8085 | dify.mrf103.com ✅ |

**ملاحظة DNS:** أضف في Cloudflare سجلات A أو CNAME لـ:
- sovereign.mrf103.com → 46.224.225.96
- god.mrf103.com → 46.224.225.96
- gateway.mrf103.com → 46.224.225.96
- dify.mrf103.com → 46.224.225.96

---

## 8. أوامر سريعة

```bash
# فحص كل المنافذ
for p in 3000 4000 5050 5678 8002 8003 8085 8090 8100 8200 8501 8888 9000 9999 5001; do
  echo -n "Port $p: "; curl -s -o /dev/null -w "%{http_code}" http://localhost:$p/ 2>/dev/null || echo "closed"
done

# إعادة تحميل nginx بعد التعديل
sudo nginx -t && sudo systemctl reload nginx
```
