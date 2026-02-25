# NEXUS PRIME — دليل الاستخدام والفهرس والمحتوى وشجرة وخريطة الأنظمة

**التاريخ:** 2026-02-25  
**اللغة:** العربية

---

# الجزء الأول: دليل الاستخدام المختصر

## من أنت؟

| الدور | ابدأ من | الروابط الأساسية |
|-------|---------|-------------------|
| **مستخدم** | الروابط أدناه | dify، chat، dashboard، publisher، boardroom |
| **مطور** | الواجهات البرمجية | api، llm، cortex، nerve |
| **أدمن** | أوامر التشغيل | docker compose، verify_nexus_pulse |

## الروابط حسب الاستخدام

| الرابط | ماذا يفعل |
|--------|-----------|
| dify.mrf103.com | محادثة AI — Chatflow و Workflows |
| chat.mrf103.com / ai.mrf103.com | واجهة محادثة مباشرة (Open WebUI) |
| dashboard.mrf103.com | لوحة التحكم الرئيسية |
| publisher.mrf103.com | نشر المحتوى (Shadow Seven) |
| boardroom.mrf103.com | غرفة القرار المعرفية |
| api.mrf103.com | واجهة برمجية عامة |
| llm.mrf103.com | LiteLLM — للمطورين |
| cortex.mrf103.com | Cortex API |
| nerve.mrf103.com | Nerve API |
| gateway.mrf103.com | AS-SULTAN Gateway |

---

# الجزء الثاني: الفهرس الكامل

## 1. ابدأ من هنا

| الملف | الوصف |
|-------|-------|
| GUIDE_USER_DEVELOPER_ADMIN_AR.md | دليل المستخدم والمطور والأدمن (عربي) |
| 00_START_HERE_MASTER_GUIDE.md | نقطة الدخول الوحيدة: الرؤية، النشر، المشغّل |
| READY_TO_FILL_AND_OVERVIEW.md | متغيرات البيئة، خريطة DNS، دليل الإجراءات |
| USER_CHECKLIST_MINIMAL.md | الخطوات اليدوية فقط (3 خطوات) |
| OVERVIEW_AND_SUMMARY_2026-02-25.md | نظرة وحوصة |

## 2. البنية والهندسة

| الملف | الوصف |
|-------|-------|
| ARCHITECTURE.md | البنية المعمارية الكاملة |
| FRONTEND_ARCHITECTURE.md | بنية الواجهات، المستويان |
| FRONTEND_INDEX.md | جرد الصفحات والمسارات |
| nginx-frontend-routes.md | DNS و ingress |

## 3. النشر والتشغيل

| الملف | الوصف |
|-------|-------|
| LOCAL_DEPLOYMENT.md | تشغيل محلي كامل |
| DEPLOYMENT.md | دليل النشر العام |
| SOVEREIGN_PORTS_AND_SERVICES.md | المنافذ والخدمات |

## 4. Dify والتحقق

| الملف | الوصف |
|-------|-------|
| DIFY_VERIFICATION_AND_DNS_MAP.md | DNS + Dify |
| DIFY_MODELS_DATA_KNOWLEDGE_TEST_REPORT.md | تقرير اختبار Dify والمودلز والمعرفة |
| SOVEREIGN_EXECUTIVE_CHECKLIST_FINAL_ACTIVATION.md | قائمة التفعيل اليدوية |

## 5. الامتثال والعلوم

| الملف | الوصف |
|-------|-------|
| Compliance/ | SoF, PoR, SoW, AML |
| Science_and_RnD/ | براءات الاختراع، الاستثمار، التدقيق |

## 6. التقارير المؤرخة

| المجلد | الوصف |
|--------|-------|
| 2026-02-24/ | لقطات وتقارير |
| archive/ | أرشيف التقارير |

---

# الجزء الثالث: شجرة الطبقات والأنظمة

```
NEXUS PRIME — الشجرة الكاملة
═══════════════════════════════════════════════════════════════

1. طبقة الوصول (Access Layer)
   ├── Cloudflare (DNS + SSL)
   ├── Nginx (Reverse Proxy)
   └── النطاقات: *.mrf103.com

2. طبقة الواجهة (Frontend Layer)
   ├── Dashboard ARC (dashboard.mrf103.com)
   ├── Shadow Seven Publisher (publisher.mrf103.com)
   ├── X-BIO Sentinel (xbio.mrf103.com)
   ├── Boardroom (boardroom.mrf103.com)
   ├── Web Dashboards (ثابت)
   └── Imperial UI (مشترك)

3. طبقة API (API Gateway Layer)
   ├── ecosystem_api (api.mrf103.com)
   ├── nexus_auth (المصادقة)
   ├── nexus_litellm (llm.mrf103.com)
   └── shadow7_api

4. طبقة الذكاء الاصطناعي (AI Layer)
   ├── Dify (dify.mrf103.com)
   ├── nexus_ai / Open WebUI (chat, ai)
   ├── nexus_ollama (النماذج المحلية)
   ├── nexus_litellm (بوابة LLM)
   └── nexus_oracle (RAG)

5. طبقة Cortex (العصبية)
   ├── nexus_cortex (8090)
   ├── nexus_nerve (8200)
   ├── neural_spine (8300)
   └── reflex_agents

6. طبقة Gateway (البوابة)
   ├── sovereign_gateway (9999)
   └── sovereign_dify_bridge (8888)

7. طبقة البيانات (Data Layer)
   ├── nexus_db (PostgreSQL)
   ├── nexus_redis
   ├── dify-db_postgres
   ├── dify-redis
   └── dify-weaviate (Vector DB)

8. طبقة المراقبة (Monitoring)
   ├── nexus_prometheus
   ├── nexus_grafana
   └── nexus_alertmanager

9. خدمات إضافية
   ├── nexus_flow (n8n)
   ├── nexus_voice (Edge TTS)
   ├── nexus_memory_keeper
   └── nexus_postgrest
```

---

# الجزء الرابع: خريطة الطبقات

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        المستخدمون / العملاء                               │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────────┐
│  طبقة الوصول: Cloudflare → Nginx (SSL) → *.mrf103.com                  │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────▼───────┐     ┌────────▼────────┐     ┌────────▼────────┐
│  واجهات الويب  │     │   واجهات API   │     │   Dify / Chat   │
│  dashboard    │     │  api, cortex   │     │  dify, chat, ai  │
│  publisher    │     │  nerve, llm   │     │                 │
│  boardroom    │     │               │     │                 │
└───────┬───────┘     └────────┬────────┘     └────────┬────────┘
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────────┐
│  طبقة الخدمات: Auth, LiteLLM, Ecosystem API, Shadow7                    │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐    ┌────────▼────────┐    ┌──────▼──────┐
│  Cortex      │    │  AI / LLM       │    │  Gateway    │
│  Nerve       │    │  Dify, Ollama   │    │  Sovereign  │
│  Neural Spine│    │  Oracle, Memory │    │  Bridge     │
└───────┬──────┘    └────────┬────────┘    └──────┬──────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│  طبقة البيانات: PostgreSQL, Redis, Weaviate                              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# الجزء الخامس: جدول الخدمات والمنافذ

| المنفذ | الخدمة | النطاق | الدور |
|--------|--------|--------|-------|
| 3000 | Open WebUI | chat, ai | محادثة AI |
| 4000 | LiteLLM | llm | بوابة LLM |
| 5001 | Dashboard | dashboard | لوحة التحكم |
| 5678 | n8n | — | أتمتة |
| 8002 | Shadow7 API | — | نشر المحتوى |
| 8003 | Auth | — | المصادقة |
| 8085 | Dify | dify | منصة AI |
| 8090 | Cortex | cortex | التوجيه |
| 8100 | Oracle | — | RAG |
| 8200 | Nerve | nerve | الجهاز العصبي |
| 8300 | Neural Spine | — | العمود المعرفي |
| 8501 | Boardroom | boardroom | غرفة القرار |
| 8888 | Dify Bridge | sovereign | جسر Dify |
| 9000 | Memory Keeper | memory | حارس الذاكرة |
| 9999 | Gateway | gateway | AS-SULTAN |
| 11434 | Ollama | — | نماذج محلية |

---

# الجزء السادس: مسار الـ LLM

```
المتصفح → dify.mrf103.com → Dify API
                ↓
         llm.mrf103.com (Nginx) → nexus_litellm:4000
                ↓
         nexus_ollama:11434 → llama3.2:3b
```

---

# الخلاصة

- **دليل الاستخدام:** الجزء الأول
- **الفهرس:** الجزء الثاني
- **الشجرة:** الجزء الثالث
- **الخريطة:** الجزء الرابع
- **جدول الخدمات:** الجزء الخامس

**للمزيد:** docs/INDEX.md و docs/GUIDE_USER_DEVELOPER_ADMIN_AR.md
