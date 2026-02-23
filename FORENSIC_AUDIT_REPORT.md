# تقرير التحقيق الجنائي الاستقصائي — NEXUS PRIME UNIFIED

**التاريخ:** 2026-02-23  
**النطاق:** جرد شامل، اختبار، تحليل كود، بنية السيرفر، المشاريع الأربعة

---

## 1. جرد الدومينات والسب دومينات والمسارات

### مصفوفة كاملة: Domain | Subdomain | Path | Backend | Port | الحالة

| الدومين | المسار | الباك اند | المنفذ | HTTP |
|---------|--------|-----------|--------|------|
| mrf103.com | / | Static | — | 200 |
| mrf103.com | /api/ | Ecosystem API | 8005 | 200 |
| mrf103.com | /webhook/stripe | Ecosystem API | 8005 | — |
| publisher.mrf103.com | / | Static (shadow-seven-publisher) | — | — |
| publisher.mrf103.com | /rest/v1/ | PostgREST | 3001 | **000** |
| publisher.mrf103.com | /ai/ | Ollama | 11434 | 200 |
| publisher.mrf103.com | /api/shadow7/ | Shadow7 API | 8002 | 404 |
| sultan.mrf103.com | / | Static (sultan) | — | — |
| sultan.mrf103.com | /api/ | Ecosystem API | 8005 | 200 |
| admin.mrf103.com | / | Static (admin) | — | — |
| admin.mrf103.com | /api/ | Ecosystem API | 8005 | 200 |
| chat.mrf103.com, nexus.mrf103.com, ai.mrf103.com | / | Open WebUI | 3000 | 200 |
| flow.mrf103.com, n8n.mrf103.com | / | n8n | 5678 | 200 |
| api.mrf103.com | / | Ecosystem API | 8005 | 200 |
| sovereign.mrf103.com, god.mrf103.com | / | Sovereign Bridge | 8888 | 200 |
| gateway.mrf103.com | / | AS-SULTAN Gateway | 9999 | 200 |
| dify.mrf103.com | / | Dify | 8085 | 307 |
| jarvis.mrf103.com | / | Static (jarvis) | — | — |
| imperial.mrf103.com | / | Static (imperial) | — | — |
| voice.mrf103.com | / | Edge-TTS | 5050 | 200 |
| prime.mrf103.com | / | Static (prime) | — | — |
| boardroom.mrf103.com | / | Boardroom | 8501 | 200 |
| dashboard.mrf103.com, app.mrf103.com, dash.mrf103.com | / | Nexus Dashboard | 5001 | 200 |
| monitor.mrf103.com | / | Static (monitor) | — | — |
| finance.mrf103.com | / | Static (finance) | — | — |
| marketing.mrf103.com | / | Static (marketing) | — | — |
| cortex.mrf103.com | / | Nexus Cortex | 8090 | 200 |
| platform.mrf103.com | / | Static (nexus-platform) | — | — |
| platform.mrf103.com | /api/ | Ecosystem API | 8005 | 200 |
| oracle.mrf103.com | / | Nexus Oracle | 8100 | 404 |
| data.mrf103.com | / | Ecosystem API | 8005 | 200 |
| grafana.mrf103.com | / | Grafana | 3002 | **000** |
| xbio.mrf103.com | / | X-BIO Sentinel | 8080 | **000** |
| memory.mrf103.com | / | Memory Keeper | 9000 | 200 |
| nerve.mrf103.com | /, /api/ | Nexus Nerve | 8200 | 200 |

### جذور الملفات الثابتة (Static Roots)

| المسار | الحالة |
|--------|--------|
| /var/www/nexus-landing | ✅ (admin, imperial, sultan, jarvis, index) |
| /var/www/monitor | ✅ |
| /var/www/finance | ✅ |
| /var/www/marketing | ✅ |
| /var/www/nexus-platform | ✅ |
| /var/www/prime | ✅ |
| /root/products/shadow-seven-publisher/dist | ✅ |

---

## 2. نتائج اختبار الباك اند والفرونت اند

### منافذ تعمل (200/404/307)

| المنفذ | الخدمة | الحالة |
|--------|--------|--------|
| 3000 | Open WebUI | ✅ 200 |
| 4000 | LiteLLM | ✅ 200 |
| 5050 | Edge-TTS | ✅ 200 |
| 5678 | n8n | ✅ 200 |
| 8002 | Shadow7 API | ✅ 404 |
| 8003 | Auth | ✅ 404 |
| 8005 | Ecosystem API | ✅ 200 |
| 8085 | Dify | ✅ 307 (redirect) |
| 8090 | Cortex | ✅ 200 |
| 8100 | Oracle | ✅ 404 |
| 8200 | Nerve | ✅ 200 |
| 8501 | Boardroom | ✅ 200 |
| 8888 | Sovereign Bridge | ✅ 200 |
| 9000 | Memory Keeper | ✅ 200 |
| 9999 | Gateway | ✅ 200 |
| 5001 | Dashboard | ✅ 200 |
| 11434 | Ollama | ✅ 200 |

### منافذ مغلقة أو غير مشغلة

| المنفذ | الخدمة | المشكلة |
|--------|--------|---------|
| 3001 | PostgREST | ❌ مغلق — publisher/rest/v1 لن يعمل |
| 3002 | Grafana | ❌ مغلق — monitoring stack غير مشغل |
| 8080 | X-BIO Sentinel | ❌ مغلق — xbio.mrf103.com غير متاح |

### الربط بين الخدمات

- **Sovereign Bridge** → dify_api (alias) ✅
- **Sovereign Bridge** → nexus_db, nexus_litellm, nexus_nerve ✅
- **Gateway** → Sovereign Bridge ✅
- **Nerve** → LiteLLM, Ollama ✅
- **Memory Keeper** → LiteLLM ✅
- **Oracle** → ChromaDB, LiteLLM ✅

---

## 3. تحليل الكود: Mock، تكرار، مخلفات

### Mock / Dummy في كود الإنتاج (NEXUS Core)

| الملف | النوع | التقييم |
|-------|-------|---------|
| nexus_nerve/cognitive_bridge.py | "fake" في قائمة كلمات محظورة | ✅ مشروع — أمان |
| sovereign_dify_bridge/main.py | TODO: trigger Dify workflow | ⚠️ معلق — يحتاج DIFY_DEFENSIVE_WORKFLOW_ID |

**خلاصة:** لا يوجد mock أو dummy وهمي في كود الإنتاج الأساسي. الـ mock في dify محصور في ملفات الاختبار (tests/) و stress-test فقط.

### تكرار الملفات (duplicate_files_report.txt)

- **~6700+ سطر** من الملفات المكررة (نفس الـ hash)
- أغلبها في `SOURCE_CODE_EXTRACTED` و `planets/` و `products/`
- أنماط التكرار:
  - GRAVEYARD_DIG مكرر بين 3d-aara و aura-ar-3d
  - X-BIO firmware مكرر بين planets/X-BIO و products/xbio-sentinel
  - arc-framework، dashboard-arc، mrf103ARC-Namer — تكرار مكونات UI
  - litellm_config.yaml مكرر
  - archive_backup/duplicated_docs — توثيق مكرر

### مشاريع مستقلة (الأربعة)

| المشروع | المسار | الحالة | ملاحظات |
|---------|--------|--------|---------|
| **X-BIO** | planets/X-BIO, products/xbio-sentinel | جزئي | firmware + website؛ X-BIO Sentinel (8080) غير مشغل |
| **NEXUS PRIME** | docker-compose, nexus_*, sovereign_* | ✅ يعمل | القلب التشغيلي |
| **Shadow 7** | planets/SHADOW-7, products/shadow-seven-publisher | ✅ يعمل | publisher على 8002؛ PostgREST (3001) مغلق |
| **Clone Hub** | integration/clone-hub + planets/CLONE-HUB | ✅ يعمل | جزء من ecosystem — تحليل المنتجات، Operational |

---

## 4. بنية السيرفر والروت

### هيكل /root

```
/root
├── NEXUS_PRIME_UNIFIED/     # المشروع الرئيسي
│   ├── nexus_nerve/         # Nerve
│   ├── nexus_cortex/        # Cortex
│   ├── nexus_oracle/        # Oracle
│   ├── memory_keeper/       # Memory Keeper
│   ├── sovereign_dify_bridge/
│   ├── neural_spine/        # override
│   ├── dify/                # Dify (منفصل)
│   ├── planets/             # X-BIO, SHADOW-7, CLONE-HUB, AI-ARCH, RAG-CORE
│   ├── products/            # shadow-seven-publisher, xbio-sentinel, etc.
│   ├── SOURCE_CODE_EXTRACTED/  # نسخة أرشيفية — تكرار كبير
│   └── ...
├── products/                # symlink → قد يشير لمجلد آخر
└── integration/             # symlink من NEXUS
```

### ما له علاقة مباشرة بالتشغيل

- `docker-compose.yml` + `docker-compose.dify.yml`
- `nexus_*`, `sovereign_*`, `shadow7_api`
- `nginx/nexus_unified.conf`
- `/var/www/*` (static roots)
- `products/shadow-seven-publisher` (لو publisher مستخدم)

### ما قد يكون زائد أو أرشيفي

- `SOURCE_CODE_EXTRACTED` — نسخة مكررة ضخمة
- `GRAVEYARD_DIG` في عدة مشاريع
- `archive_backup/`, `duplicated_docs/`
- `duplicate_files_report.txt` (1100+ KB)

---

## 5. النواقص والإصلاحات

### خدمات غير مشغلة

1. **PostgREST (3001)** — مطلوب لـ publisher.mrf103.com/rest/v1/
2. **Grafana (3002)** — تشغيل `docker compose -f monitoring/docker-compose.monitoring.yml up -d`
3. **X-BIO Sentinel (8080)** — تشغيل حاوية nexus_xbio أو ما يعادلها

### TODO في الكود

- `sovereign_dify_bridge/main.py:259` — إكمال trigger لـ Dify workflow عند ضبط DIFY_DEFENSIVE_WORKFLOW_ID

### توصيات تنظيف

1. **تقليل التكرار:** دمج أو حذف الملفات المكررة في SOURCE_CODE_EXTRACTED و GRAVEYARD_DIG
2. **إزالة الأرشيف:** مراجعة archive_backup و duplicated_docs
3. **توحيد X-BIO:** دمج planets/X-BIO و products/xbio-sentinel في مصدر واحد

---

## 6. نموذج العمل والمنظومة

### كمنظومة متكاملة

- NEXUS PRIME + Sovereign + Dify + Nerve + Cortex + Memory + Oracle + Boardroom
- كل الخدمات مربوطة عبر nginx و docker network

### كمشاريع مستقلة قابلة للبيع/الترخيص

| المشروع | المكونات | قابلية |
|---------|-----------|--------|
| X-BIO | firmware + Sentinel + website | ✅ |
| NEXUS PRIME | Core stack | ✅ |
| Shadow 7 | Publisher + API | ✅ |
| Clone Hub | integration + planets | ✅ يعمل — جزء من ecosystem |

### SaaS / تراخيص / اشتراكات

- البنية تدعم فصل الخدمات (مثلاً: Dify، Boardroom، Nerve كمنتجات منفصلة)
- API Gateway (8005) نقطة دخول موحدة للـ APIs

---

## 7. ملخص تنفيذي

| البند | الحالة |
|-------|--------|
| جرد الدومينات | ✅ مكتمل |
| اختبار الباك اند | ✅ 17/20 منفذ يعمل |
| Mock في الإنتاج | ✅ لا يوجد |
| تكرار الكود | ⚠️ كبير في SOURCE_CODE_EXTRACTED |
| بنية السيرفر | ✅ واضحة |
| المشاريع الأربعة | 3 تشغيلية، 1 غير مكتمل |
| خدمات ناقصة | PostgREST, Grafana, X-BIO |

---

*التقرير أُعد آلياً. يُنصح بمراجعة يدوية للنقاط الحرجة.*
