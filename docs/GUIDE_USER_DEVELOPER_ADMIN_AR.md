# NEXUS PRIME — دليل المستخدم والمطور والأدمن

**اللغة:** العربية  
**التاريخ:** 2026-02-25

---

# الجزء الأول: دليل المستخدم

## من أنت كمستخدم؟

أنت شخص يستخدم المنصة من المتصفح — محادثة مع الذكاء الاصطناعي، لوحة تحكم، نشر محتوى، أو أي خدمة أخرى.

---

## الروابط التي تحتاجها

| الرابط | ماذا يفعل |
|--------|-----------|
| **dify.mrf103.com** | محادثة مع الذكاء الاصطناعي — أنشئ تطبيقاً أو استخدم Chatflow |
| **chat.mrf103.com** أو **ai.mrf103.com** | واجهة محادثة مباشرة (Open WebUI) |
| **dashboard.mrf103.com** | لوحة التحكم الرئيسية |
| **publisher.mrf103.com** | نشر المحتوى (Shadow Seven) |
| **boardroom.mrf103.com** | غرفة القرار المعرفية |
| **api.mrf103.com** | واجهة برمجية عامة |

---

## كيف تبدأ؟

1. افتح الرابط المناسب من الجدول أعلاه.
2. سجّل الدخول إذا طُلب منك ذلك.
3. استخدم الواجهة — اكتب، انقر، ارفع ملفات حسب الخدمة.

---

## إذا واجهت مشكلة

- **الصفحة لا تفتح:** تأكد من الاتصال بالإنترنت، وجرّب متصفحاً آخر.
- **خطأ 502 أو 504:** الخدمة قد تكون متوقفة — تواصل مع الأدمن.
- **نسيت كلمة المرور:** تواصل مع الأدمن لإعادة التعيين.

---

# الجزء الثاني: دليل المطور

## من أنت كمطور؟

أنت مبرمج يريد ربط تطبيق أو سكربت بالمنصة عبر واجهاتها البرمجية (API).

---

## الواجهات البرمجية الرئيسية

| الرابط | الاستخدام |
|--------|-----------|
| **api.mrf103.com/api/v1/health** | فحص صحة النظام |
| **api.mrf103.com/api/v1/products** | قائمة المنتجات |
| **llm.mrf103.com/v1** | واجهة OpenAI-compatible (LiteLLM) — تحتاج `Authorization: Bearer sk-nexus-sovereign-mrf103` |
| **cortex.mrf103.com** | Cortex API — تسجيل الوكلاء والأوامر |
| **nerve.mrf103.com** | Nerve API — الإشارات والهرمونات |

---

## مثال: استدعاء الذكاء الاصطناعي

```bash
curl -X POST "https://llm.mrf103.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-nexus-sovereign-mrf103" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"مرحبا"}]}'
```

---

## متغيرات البيئة (للتطوير المحلي)

انسخ `.env.example` إلى `.env` واملأ:

- `POSTGRES_PASSWORD` — كلمة مرور قاعدة البيانات
- `JWT_SECRET` — للتوقيع
- `DIFY_API_KEY` — (اختياري) لاستدعاء Dify من التطبيق

---

## هيكل المشروع (مختصر)

```
NEXUS_PRIME_UNIFIED/
├── docker-compose.yml      # الخدمات الرئيسية
├── docker-compose.dify.yml # Dify والجسر
├── infrastructure/nginx/   # إعدادات Nginx
├── integration/           # واجهات التكامل
├── nexus_cortex/          # Cortex API
├── nexus_nerve/            # Nerve API
└── docs/                  # التوثيق
```

---

# الجزء الثالث: دليل الأدمن

## من أنت كأدمن؟

أنت مسؤول عن تشغيل السيرفر، الحاويات، قواعد البيانات، والشبكات.

---

## أوامر التشغيل الأساسية

```bash
# الانتقال للمجلد الرئيسي
cd /root/NEXUS_PRIME_UNIFIED

# تشغيل كل الخدمات
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.dify.yml up -d

# تشغيل Dify (منفصل)
cd dify/docker
docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify up -d

# التحقق من الصحة
./scripts/verify_nexus_pulse.sh
```

---

## أوامر الصيانة

| المهمة | الأمر |
|--------|-------|
| عرض حالة الحاويات | `docker ps -a` |
| إعادة تشغيل خدمة | `docker restart <اسم_الحاوية>` |
| عرض سجلات خدمة | `docker logs <اسم_الحاوية>` |
| إعادة تشغيل Nginx | `systemctl restart nginx` |
| إعادة تعيين كلمة مرور Dify | `docker exec -it dify-api-1 flask reset-password` |
| تسجيل الدخول عبر API | كلمة المرور يجب أن تكون **Base64** — انظر docs/DIFY_MODELS_DATA_KNOWLEDGE_TEST_REPORT |

---

## الملفات المهمة

| الملف | الغرض |
|-------|-------|
| `.env` | المتغيرات السرية — كلمات المرور، المفاتيح |
| `infrastructure/nginx/nexus_unified.conf` | إعدادات Nginx — النطاقات والمسارات |
| `dify/docker/.env` | إعدادات Dify |
| `litellm_config.yaml` | نماذج LiteLLM والتوجيه |

---

## Cloudflare (مرة واحدة)

1. SSL/TLS → **Full (strict)**
2. DNS → كل السجلات **Proxied** (السحابة البرتقالية)
3. أضف سجل `llm` → IP السيرفر (لـ llm.mrf103.com)

---

## إضافة نموذج في Dify

1. Settings → Model Provider → OpenAI
2. API Base: `https://llm.mrf103.com`
3. API Key: `sk-nexus-sovereign-mrf103`
4. Model Name: `gpt-4o`

---

## التحقق من الربط

| الفحص | الأمر أو الرابط |
|-------|-----------------|
| صحة API | `curl -s https://api.mrf103.com/api/v1/health` |
| صحة Dify | افتح https://dify.mrf103.com |
| صحة قاعدة البيانات | `docker exec nexus_db pg_isready -U postgres` |
| صحة Redis | `docker exec nexus_redis redis-cli ping` |

---

## إذا توقفت خدمة

1. تحقق: `docker ps -a`
2. أعد التشغيل: `docker restart <الاسم>`
3. راجع السجلات: `docker logs <الاسم>`
4. إذا استمر الخطأ: راجع `docs/` للتوثيق التفصيلي

---

# ملخص سريع

| الدور | ابدأ من |
|-------|---------|
| **مستخدم** | الروابط في الجزء الأول |
| **مطور** | الواجهات البرمجية في الجزء الثاني |
| **أدمن** | أوامر التشغيل والصيانة في الجزء الثالث |

---

**للمزيد:** راجع `docs/INDEX.md` و `docs/00_START_HERE_MASTER_GUIDE.md`
