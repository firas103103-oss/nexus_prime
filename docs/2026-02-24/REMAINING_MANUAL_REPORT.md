# تقرير الإجراءات اليدوية المتبقية — NEXUS PRIME

**التاريخ:** 2026-02-24  
**الغرض:** كل ما يتطلب تدخلاً يدوياً من Monsieur Feras بعد تنفيذ خطة الإصلاح الآلي.

---

## 1. Dify — موسوعة السلطان

| البند | الإجراء | المرجع |
|-------|---------|--------|
| **Knowledge Base** | رفع docs/SOVEREIGN_ENCYCLOPEDIA.md إلى Dify يدوياً، أو تشغيل: DIFY_CONSOLE_API_KEY=xxx python scripts/dify_ingest_sovereign_encyclopedia.py | scripts/DIFY_SOVEREIGN_ENCYCLOPEDIA_INGEST.md |
| **DIFY_DEFENSIVE_WORKFLOW_ID** | إنشاء workflow في Dify للـ hormonal spike، ثم تعبئة .env | RUNBOOK.md |

---

## 2. البنية التحتية

| البند | الإجراء | المرجع |
|-------|---------|--------|
| **MSL Schema** | تشغيل ./scripts/db/apply_msl_schema.sh إذا لم يُطبق | scripts/db/apply_msl_schema.sh |
| **Cloudflare DNS** | إضافة 14 سجل A للـ subdomains | docs/archive/imported_DOCS/ARCHIVE/NEXUS_CONFIGURATION_COMPLETE.md |
| **Auth Keys** | تشغيل integration/shared-auth/generate_keys.py | integration/shared-auth/README.md |

---

## 3. البريد والتسويق

| البند | الإجراء |
|-------|---------|
| **SMTP** | إعداد SMTP وتعبئة shadow-seven: SMTP_HOST, SMTP_USER, SMTP_PASSWORD |

---

## 4. الأمان

| البند | الإجراء |
|-------|---------|
| **npm audit** | تشغيل npm audit fix في shadow-seven-publisher و imperial-ui |

---

## 5. المنتجات المحلية

| البند | الإجراء |
|-------|---------|
| **AlSultan VITE_SUPABASE_URL** | عند التشغيل المحلي: ضبط على PostgREST المحلي |

---

## 6. عناصر خارج النطاق الآلي

| البند | الوصف |
|-------|-------|
| **X-BIO 9 خوارزميات** | تحتاج تطوير خوارزمي |
| **9 منتجات بدون node_modules** | تشغيل npm install لكل منتج |
| **Imperial UI** | نسخ dist إلى nginx |
| **Shadow Seven فجوات** | تعويض النص، نظام الوكلاء |
| **LiteLLM UNHEALTHY** | مراجعة litellm_config.yaml |

---

## ملخص أولويات التدخل اليدوي

| الأولوية | البند |
|----------|-------|
| P0 | MSL Schema، Auth Keys |
| P1 | Dify Knowledge Base + DIFY_DEFENSIVE_WORKFLOW_ID |
| P2 | Cloudflare DNS، SMTP |
| P3 | npm audit، AlSultan VITE_SUPABASE_URL |
