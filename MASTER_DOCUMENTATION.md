# 📋 NEXUS PRIME - التوثيق الشامل
### المرجع الرسمي الكامل لنظام NEXUS PRIME
**التاريخ:** 18 فبراير 2026  
**الإصدار:** v2.2.0  
**المالك:** MrF (firas103103-oss)  
**الدومين:** mrf103.com  
**السيرفر:** 46.224.225.96 (Hetzner - Ubuntu)  
**IPv6:** 2a01:4f8:1c19:c6de::1

---

## 📑 فهرس المحتويات

1. [نظرة عامة](#-نظرة-عامة)
2. [المراحل الخمس](#-المراحل-الخمس)
3. [المنتجات السبعة](#-المنتجات-السبعة)
4. [البنية التحتية](#-البنية-التحتية)
5. [الدومينات و DNS](#-الدومينات-و-dns)
6. [Docker Stack](#-docker-stack)
7. [نظام الكواكب (Planets)](#-نظام-الكواكب-planets)
8. [التكاملات (Integration)](#-التكاملات-integration)
9. [GitHub Repos](#-github-repos)
10. [الأمان و SSL](#-الأمان-و-ssl)
11. [خزنة الموديلات (Model Vault)](#-خزنة-الموديلات-model-vault)
12. [خريطة الـ API Endpoints](#-خريطة-الـ-api-endpoints)
13. [السكريبتات](#-السكريبتات)
14. [بيانات الوصول](#-بيانات-الوصول)
15. [خريطة الملفات](#-خريطة-الملفات)

---

## 🌍 نظرة عامة

**NEXUS PRIME** هو نظام موحد يجمع كل مشاريع MrF في بنية واحدة منظمة.
- **قبل:** 105GB ملفات مبعثرة، 11 نسخة مكررة، بدون تنظيم
- **بعد:** 3.9GB نظام موحد، 7 منتجات، 12 كوكب، 5 تكاملات

```
NEXUS_PRIME_UNIFIED/
├── dashboard-arc/        # لوحة التحكم الرئيسية (480 ملف)
├── data/                 # بيانات Docker (symlinks)
├── docker-compose.yml    # البنية التحتية
├── docs/                 # الوثائق
├── integration/          # 5 تكاملات
├── landing-pages/        # صفحات الهبوط
├── marketing/            # مواد التسويق
├── n8n-workflows/        # 3 أتمتة
├── nginx/                # إعدادات Nginx
├── planets/              # 12 كوكب (وكلاء ذكاء)
├── products/             # 7 منتجات
└── scripts/              # سكريبتات الإدارة
```

---

## 🚀 المراحل الخمس

### المرحلة 0: الاكتشاف (Discovery)
- **الهدف:** فحص كامل النظام
- **النتيجة:** 105GB بيانات مبعثرة، 11 نسخة مكررة مكتشفة
- **الأدوات:** فحص يدوي + سكريبتات مسح

### المرحلة 1: التوحيد (Consolidation)
- **الهدف:** دمج كل شيء في مجلد واحد
- **النتيجة:**
  - إنشاء `NEXUS_PRIME_UNIFIED` (3.1GB أولياً → 3.9GB حالياً)
  - تحرير 13GB من المساحة
  - حذف التكرارات
  - هيكلة المجلدات

### المرحلة 2: التحويل لمنتجات (Productization)
- **الهدف:** تحويل المشاريع الخام إلى 7 منتجات جاهزة
- **النتيجة:** 7 منتجات، 524MB، 54,821 ملف
- **المسار:** `/root/products/` و `/root/NEXUS_PRIME_UNIFIED/products/`

### المرحلة 3: التكامل (Integration)
- **الهدف:** ربط المنتجات ببعضها
- **النتيجة:** 5 مكونات تكامل:
  1. CLONE HUB - مركز الاستنساخ
  2. Ecosystem API - واجهة النظام البيئي
  3. Command Center - مركز القيادة
  4. Shared Auth - مصادقة موحدة
  5. Admin Portal - بوابة الإدارة

### المرحلة 4: التتجير (Commercialization)
- **الهدف:** تجهيز النظام للإنتاج والبيع
- **النتائج:**
  - ✅ استعادة Dashboard-ARC (480 ملف، 5.7MB)
  - ✅ استعادة بيانات Docker المهددة بالفقدان (48MB DB + 889MB Open-WebUI + 11GB Ollama + 4.6MB n8n)
  - ✅ إعداد Nginx موحد (10 server blocks مع SSL)
  - ✅ 3 صفحات هبوط احترافية (الرئيسية، الناشر، السلطان)
  - ✅ تكامل Stripe للدفع (8 منتجات، webhooks، تتبع الإيرادات)
  - ✅ 3 أتمتة n8n (التقاط العملاء، الرعاية، الإعداد)
  - ✅ إعداد DNS (15 سجل عبر Cloudflare API)
  - ✅ شهادة SSL Wildcard (*.mrf103.com)
  - ✅ رفع Git إلى GitHub (798MB → nexus_prime)
  - ✅ اختبار نهائي: 41/41 نجاح (100%) ✨

### المرحلة 5: مزامنة GitHub (Git Sync)
- **الهدف:** رفع كل المنتجات لمستودعات GitHub مستقلة
- **النتيجة:** 9/9 مستودعات تحتوي على commits ✅

---

## 📦 المنتجات السبعة

| # | المنتج | الوصف | الملفات | الحجم | GitHub Repo |
|---|--------|--------|---------|-------|-------------|
| 1 | **Shadow Seven Publisher** | منصة نشر بالذكاء الاصطناعي | 168 | 1.9MB | shadow-seven-publisher |
| 2 | **AlSultan Intelligence** | تحليل قرآني بالذكاء (Chronos, Decoder, Identity) | 5 | 452K | alsultan-intelligence |
| 3 | **Jarvis Control Hub** | مراقبة وتنسيق مركزي (Python + FastAPI) | 9 | 80K | jarvis-control-hub |
| 4 | **Imperial UI** | واجهة لوحة تحكم (React + Vite + Tailwind) | 14 | 204K | imperial-ui |
| 5 | **MRF103 Mobile** | تطبيق موبايل (React Native + Expo) | 89 | 1.5MB | mrf103-mobile-app |
| 6 | **X-BIO Sentinel** | نظام رصد حيوي (Python + ESP32) | 13 | 56K | xbio-sentinel |
| 7 | **NEXUS Data Core** | محرك معالجة بيانات موحد | 2 | 12K | nexus-data-core |

---

## 🏗️ البنية التحتية

### السيرفر
```
المزود:    Hetzner
النظام:    Ubuntu
الرام:     22GB
القرص:     451GB (191GB مستخدم - 45%)
IPv4:      46.224.225.96
IPv6:      2a01:4f8:1c19:c6de::1
```

### الخدمات النشطة
| الخدمة | المنفذ | الحالة |
|--------|--------|--------|
| Nginx (SSL) | 443 | ✅ Active |
| Nginx (HTTP) | 80 | ✅ Active |
| Open-WebUI (AI Chat) | 3000 → 8080 | ✅ Healthy |
| PostgreSQL | 5432 | ✅ Healthy |
| Ollama (LLM) | 11434 | ✅ Running |
| n8n (Automation) | 5678 | ✅ Running |
| Edge-TTS (Voice) | 5050 → 8000 | ✅ Running |
| SSH | 22 | ✅ Active |

---

## 🌐 الدومينات و DNS

**المزود:** Cloudflare  
**Zone ID:** `156bc9bdda82a4c6d357dbf5578d4845`

| السجل | الدومين | الوجهة | الخدمة |
|--------|---------|--------|--------|
| A | mrf103.com | 46.224.225.96 | الموقع الرئيسي |
| A | admin.mrf103.com | 46.224.225.96 | لوحة الإدارة |
| A | ai.mrf103.com | 46.224.225.96 | AI Services |
| A | api.mrf103.com | 46.224.225.96 | API Gateway |
| A | chat.mrf103.com | 46.224.225.96 | واجهة الدردشة |
| A | dash.mrf103.com | 46.224.225.96 | Dashboard |
| A | data.mrf103.com | 46.224.225.96 | Data Services |
| A | flow.mrf103.com | 46.224.225.96 | n8n Automation |
| A | imperial.mrf103.com | 46.224.225.96 | Imperial UI |
| A | jarvis.mrf103.com | 46.224.225.96 | Jarvis Hub |
| A | n8n.mrf103.com | 46.224.225.96 | n8n (alias) |
| A | nexus.mrf103.com | 46.224.225.96 | Nexus Portal |
| A | publisher.mrf103.com | 46.224.225.96 | Shadow Seven |
| A | sultan.mrf103.com | 46.224.225.96 | AlSultan |
| A | voice.mrf103.com | 46.224.225.96 | Voice TTS |
| MX | mrf103.com | smtp.google.com | البريد |
| TXT | mrf103.com | google-site-verification | تحقق Google |
| TXT | google._domainkey.mrf103.com | DKIM | توقيع البريد |

---

## 🐳 Docker Stack

**ملف التكوين:** `NEXUS_PRIME_UNIFIED/docker-compose.yml`

```yaml
الحاويات:
  nexus_db:       PostgreSQL 15.1.0.147 (Supabase)
  nexus_ollama:   Ollama LLM Engine
  nexus_ai:       Open-WebUI (AI Chat Interface)
  nexus_flow:     n8n v2.7.5 (Automation)
  nexus_voice:    Edge-TTS (Text-to-Speech)
  nexus_gatekeeper: Nginx Proxy Manager (معرّف لكن غير مشغّل)
```

---

## 🪐 نظام الكواكب (Planets)

12 كوكب - كل واحد وكيل ذكاء اصطناعي متخصص:

| الكوكب | الدور | الملفات الرئيسية |
|--------|-------|------------------|
| **AI-ARCH** | هندسة الذكاء الاصطناعي | arc-core, ARC-Namer, identity.json |
| **AS-SULTAN** | تحليل وتفسير قرآني | identity.json |
| **CLONE-HUB** | مركز الاستنساخ والنسخ | App.tsx, vault, repos |
| **LEGAL-EAGLE** | الشؤون القانونية | identity.json, عروض استثمارية PDF |
| **NAV-ORACLE** | التنقل والتوجيه | identity.json |
| **NEXUS-ANALYST** | تحليل البيانات | identity.json |
| **N-TARGET** | الاستهداف والأعمال | عروض تقديمية, MrF_Enterprise |
| **OPS-CTRL** | التحكم بالعمليات | identity.json |
| **RAG-CORE** | محرك RAG للمعرفة | package.json, metadata, تقارير |
| **SEC-GUARD** | الأمن السيبراني | identity.json |
| **SHADOW-7** | النشر والتوزيع | shadow-seven packages, portfolio |
| **X-BIO** | الأجهزة الحيوية IoT | Arduino CLI, BME688, xbio projects |

---

## 🔗 التكاملات (Integration)

**المسار:** `NEXUS_PRIME_UNIFIED/integration/`

| المكون | الملفات | الوظيفة |
|--------|---------|---------|
| **admin-portal** | 3 | بوابة إدارة موحدة |
| **clone-hub** | 8 | إدارة النسخ والاستنساخ |
| **command-center** | 5 | مركز القيادة وإصدار الأوامر |
| **ecosystem-api** | 8 | واجهة برمجة النظام البيئي |
| **shared-auth** | 4 | نظام مصادقة مشترك |

---

## 🔑 GitHub Repos

**الحساب:** [github.com/firas103103-oss](https://github.com/firas103103-oss)  
**المصادقة:** SSH Key (`/root/.ssh/id_ed25519`) + GH_TOKEN

### المستودعات النشطة (9 repos)

| Repo | الرؤية | الحجم | آخر Push | الحالة |
|------|--------|-------|----------|--------|
| **nexus_prime** | PUBLIC | 817 MB | 2026-02-17 | ✅ 5 commits |
| **shadow-seven-publisher** | PUBLIC | 379 KB | 2026-02-17 | ✅ Synced |
| **alsultan-intelligence** | PUBLIC | 413 KB | 2026-02-17 | ✅ Synced |
| **jarvis-control-hub** | PUBLIC | 7 KB | 2026-02-17 | ✅ Synced |
| **imperial-ui** | PUBLIC | 27 KB | 2026-02-17 | ✅ Synced |
| **mrf103-mobile-app** | PUBLIC | 740 KB | 2026-02-17 | ✅ Synced |
| **xbio-sentinel** | PUBLIC | 7 KB | 2026-02-17 | ✅ Synced |
| **nexus-data-core** | PUBLIC | ~8 KB | 2026-02-17 | ✅ Synced |
| **mrf103-website** | PUBLIC | 25 KB | 2026-02-17 | ✅ Synced |

### مستودعات قديمة (أرشيف)

| Repo | الرؤية | الحجم | الملاحظات |
|------|--------|-------|-----------|
| 777 | PRIVATE | 60 MB | مشروع قديم |
| mrf103ARC-Namer | PRIVATE | 43 MB | ARC Namer الأصلي |
| audio-intera | PRIVATE | 1.6 MB | تفاعل صوتي |
| MrF_ | PRIVATE | 1.4 MB | مشروع MrF |
| x-book | PRIVATE | 1.2 MB | X-Book |
| 7thshadow | PRIVATE | 540 KB | Shadow Seven القديم |
| hhome-canv | PRIVATE | 337 KB | Home Canvas |
| author | PRIVATE | 296 KB | Author |
| mrf103-arc-ecosystem | PRIVATE | 218 KB | النظام البيئي القديم |
| arc-namer-core | PRIVATE | 214 KB | ARC Core |
| arc-namer-vscode | PUBLIC | 212 KB | VS Code Extension |
| arc-namer-cli | PUBLIC | 212 KB | CLI Tool |
| xbook-engine | PRIVATE | 212 KB | محرك X-Book |
| mrf103 | PRIVATE | 100 KB | موقع قديم |
| data-nerve-system | PRIVATE | 56 KB | نظام أعصاب البيانات |
| nati-f-call | PRIVATE | 47 KB | Native Function Call |
| history | PRIVATE | 13 KB | التاريخ |
| mrf103-landing | PRIVATE | 6 KB | صفحة هبوط قديمة |
| mrf103-secrets | PRIVATE | 0 KB | فارغ |

---

## 🔒 الأمان و SSL

### شهادات SSL
```
Wildcard:  *.mrf103.com (Let's Encrypt)
المسار:    /etc/letsencrypt/live/mrf103.com/
الحالة:    ✅ نشطة
```

### Nginx
```
الملف:     /etc/nginx/sites-available/nexus_unified
الحالة:    ✅ Active
Blocks:    10 server blocks
```

### Nginx Server Blocks
| Block | الدومين | Proxy Pass |
|-------|---------|------------|
| 1 | mrf103.com, www.mrf103.com, *.mrf103.com | Default |
| 2 | mrf103.com, www.mrf103.com | الصفحة الرئيسية |
| 3 | publisher.mrf103.com | Shadow Seven |
| 4 | sultan.mrf103.com | AlSultan |
| 5 | admin.mrf103.com | Dashboard-ARC |
| 6 | chat.mrf103.com, nexus.mrf103.com | Open-WebUI (:3000) |
| 7 | flow.mrf103.com, n8n.mrf103.com | n8n (:5678) |
| 8 | api.mrf103.com | API Gateway |
| 9 | jarvis.mrf103.com | Jarvis Hub |
| 10 | imperial.mrf103.com | Imperial UI |
| 11 | voice.mrf103.com | Edge-TTS (:5050) |

### إصلاحات أمنية (2026-02-17 — 2026-02-18)

#### 1. إزالة مفاتيح API المكشوفة
- **المشكلة:** مفتاح OpenAI (`sk-proj-...`) كان مكشوفاً في `jarvis-control-hub/ai/orchestrator.py`
- **المشكلة:** مفتاح Gemini كان مكشوفاً في `alsultan-intelligence/app.py` و `test_api.py`
- **الحل:** استبدال بـ `os.getenv('OPENAI_API_KEY', '')` و `os.getenv('GEMINI_API_KEY', '')`
- **الحالة:** ✅ تم الإصلاح - GitHub Push Protection كانت تمنع الرفع

#### 2. إصلاح ثغرة Shell Injection في nexus_voice
- **المشكلة:** خدمة الصوت `nexus_voice` (Edge-TTS) كانت تقبل مدخلات المستخدم بدون تعقيم
- **الخطر:** أمر shell injection عبر معاملات TTS (نص → أمر نظام)
- **الحل:** تم تأمين الخدمة باستخدام `subprocess` مع قائمة أوامر آمنة (secure list) بدلاً من shell=True
- **التحقق:** Docker container يعمل بدون صلاحيات root مع `--security-opt=no-new-privileges`
- **الحالة:** ✅ تم التأمين

#### 3. إصلاح سكريبت النسخ الاحتياطي
- **المشكلة:** `nexus-backup` كان يستخدم `mysqldump` بينما قاعدة البيانات PostgreSQL
- **النتيجة:** النسخ الاحتياطية كانت فارغة (0 bytes) أو خطأ
- **الحل:** تم التصحيح لـ `pg_dump` + استثناء بيانات Ollama (11GB) من ضغط الإعدادات
- **الحالة:** ✅ تم الإصلاح (2026-02-18)

### جدار الحماية (UFW)
```
الحالة: ✅ نشط
SSH (22):     ALLOW من الجميع
HTTP (80):    ALLOW من Cloudflare IPs فقط + عام
HTTPS (443):  ALLOW من Cloudflare IPs فقط + عام
Port 3000:    ALLOW (Open-WebUI)
Port 81:      ALLOW (NPM Admin)
Port 11434:   DENY (Ollama - داخلي فقط)
Port 5678:    DENY (n8n - داخلي فقط)
Port 5432:    DENY (PostgreSQL - داخلي فقط)
Port 5050:    DENY (Voice - داخلي فقط)
Port 8080:    DENY (محجوز)
Port 8000:    DENY (محجوز)
Port 5000:    DENY (Gateway - داخلي فقط عبر Nginx)
```

---

## 🏦 خزنة الموديلات (Model Vault)

### بروتوكول حماية بيانات الذكاء الاصطناعي

**موقع الموديلات:** `/root/.ollama/models` (Docker volume: `root_ollama_data`)  
**نسخة ثانية:** `/root/nexus_prime/ollama/` (11GB)

### الموديلات المُثبتة
| الموديل | الحجم | النوع | الاستخدام |
|---------|-------|-------|-----------|
| `llama3.2:latest` | 2.0 GB | LLM عام | محادثات، تحليل نصي |
| `qwen2.5:14b` | 9.0 GB | LLM متقدم | تحليل معمق، كود |
| **المجموع** | **11.0 GB** | | |

### قواعد الحماية
1. **النسخ الاحتياطي:** الموديلات **مستثناة** من النسخ اليومي (لتجنب 11GB يومياً)
2. **الاسترجاع:** في حالة الفقدان، يتم إعادة التحميل من Ollama Registry:
   ```bash
   docker exec nexus_ollama ollama pull llama3.2:latest
   docker exec nexus_ollama ollama pull qwen2.5:14b
   ```
3. **التخزين المزدوج:** البيانات محفوظة في Docker volume + bind mount
4. **الحماية الشبكية:** Port 11434 محظور من الخارج (UFW DENY) - وصول داخلي فقط عبر Docker network
5. **إضافة موديل جديد:**
   ```bash
   docker exec nexus_ollama ollama pull <model_name>
   # التحقق
   curl -s http://localhost:11434/api/tags | python3 -m json.tool
   ```
6. **حذف موديل:**
   ```bash
   docker exec nexus_ollama ollama rm <model_name>
   ```

### مراقبة المساحة
```bash
# حجم الموديلات الحالي
du -sh /root/.ollama/models
# أو عبر API
curl -s http://localhost:11434/api/tags | python3 -c "
import json,sys; d=json.load(sys.stdin)
total=sum(m['size'] for m in d.get('models',[]))
print(f'Total: {total/1e9:.1f} GB ({len(d.get(\"models\",[]))} models)')
"
```

---

## 🔌 خريطة الـ API Endpoints

### Ecosystem API - نقاط النهاية الأساسية

| الـ Endpoint | الطريقة | الدومين | المنفذ الداخلي | الوصف |
|-------------|---------|---------|----------------|-------|
| `/` | GET | mrf103.com | nginx static | صفحة الهبوط الرئيسية |
| `/` | GET | ai.mrf103.com | 3000→8080 | واجهة Open-WebUI |
| `/api/v1/` | GET | ai.mrf103.com | 3000→8080 | Open-WebUI API |
| `/api/tags` | GET | localhost:11434 | 11434 | قائمة الموديلات (Ollama) |
| `/api/generate` | POST | localhost:11434 | 11434 | توليد نص (Ollama) |
| `/api/chat` | POST | localhost:11434 | 11434 | محادثة (Ollama) |
| `/` | GET | flow.mrf103.com | 5678 | لوحة n8n |
| `/api/v1/workflows` | GET | flow.mrf103.com | 5678 | أتمتة n8n API |
| `/api/v1/executions` | GET | flow.mrf103.com | 5678 | سجل التنفيذ |
| `/` | GET | voice.mrf103.com | 5050→8000 | خدمة الصوت |
| `/tts` | POST | voice.mrf103.com | 5050→8000 | تحويل نص لصوت |
| `/voices` | GET | voice.mrf103.com | 5050→8000 | قائمة الأصوات المتاحة |
| `/` | GET | publisher.mrf103.com | nginx static | صفحة Shadow Seven |
| `/` | GET | sultan.mrf103.com | nginx static | صفحة AlSultan |
| `/` | GET | admin.mrf103.com | nginx static | Dashboard-ARC |

### ملاحظات API
- **Ollama API** متاح داخلياً فقط (محظور من الخارج عبر UFW)
- **n8n API** يتطلب مصادقة (Bearer Token أو Basic Auth)
- **Open-WebUI API** يتطلب تسجيل دخول (Token-based)
- **Voice API** متاح عبر Nginx reverse proxy فقط (HTTPS)

---

## 📜 السكريبتات

**المسار:** `NEXUS_PRIME_UNIFIED/scripts/`

| السكريبت | الوظيفة |
|----------|---------|
| `IGNITION.sh` | تشغيل النظام الكامل |
| `git_sync_all.sh` | مزامنة جميع المنتجات مع GitHub |
| `PHASE4_LAUNCH.sh` | تنفيذ المرحلة 4 |
| `setup_dns.sh` | إعداد سجلات DNS عبر Cloudflare API |
| `deploy-unified.sh` | نشر موحد |
| `setup_nginx_proxy.sh` | إعداد Nginx Proxy |
| `system_status.sh` | حالة النظام |
| `monitor.sh` | مراقبة الخدمات |
| `STATUS.sh` | تقرير حالة سريع |
| `final_test.sh` | اختبار شامل (41/41 = 100%) ✅ |
| `shadow7_publish.py` | نشر Shadow Seven |
| `push_to_github.sh` | رفع لـ GitHub |

### أتمتة n8n
**المسار:** `NEXUS_PRIME_UNIFIED/n8n-workflows/`

| Workflow | الوظيفة |
|----------|---------|
| `lead_capture.json` | التقاط العملاء المحتملين |
| `auto_nurturing.json` | رعاية العملاء تلقائياً |
| `payment_onboarding.json` | إعداد عملاء الدفع الجدد |
| `deploy_workflows.sh` | نشر الأتمتة |

---

## 🔐 بيانات الوصول

### SSH
```
المفتاح:    /root/.ssh/id_ed25519
المستخدم:   firas103103-oss (على GitHub)
```

### PostgreSQL
```
المنفذ:     5432
قاعدة:     postgres
المستخدم:   postgres
كلمة السر: nexus_mrf_password_2026
```

### n8n
```
الرابط:     https://flow.mrf103.com
المنفذ:     5678
المستخدم:   admin
كلمة السر: nexus_mrf_flow_2026
```

### Open-WebUI
```
الرابط:     https://chat.mrf103.com
المنفذ:     3000
```

### Cloudflare
```
Token:      NTf2k_LX2NykdvAI78ClVO1NTojmYQoQZJEgpNDX
Zone ID:    156bc9bdda82a4c6d357dbf5578d4845
```

### Git
```
user.name:  MrF
user.email: admin@mrf103.com
```

---

## 🗺️ خريطة الملفات

```
/root/
├── NEXUS_PRIME_UNIFIED/           # ← النظام الرئيسي (3.9GB)
│   ├── dashboard-arc/             # لوحة التحكم (480 ملف)
│   │   ├── server/                # Backend (routes, services, modules)
│   │   ├── client/                # Frontend (React)
│   │   ├── shared/                # الكود المشترك
│   │   └── *.sql                  # ملفات قاعدة البيانات
│   ├── data/                      # بيانات Docker
│   ├── docker-compose.yml         # تكوين Docker (6 حاويات)
│   ├── docs/                      # الوثائق
│   │   └── PLANET_GUIDE.md
│   ├── integration/               # 5 تكاملات
│   │   ├── admin-portal/          # بوابة الإدارة
│   │   ├── clone-hub/             # مركز الاستنساخ
│   │   ├── command-center/        # مركز القيادة
│   │   ├── ecosystem-api/         # API الموحد
│   │   └── shared-auth/           # المصادقة
│   ├── landing-pages/             # صفحات الهبوط
│   │   └── index.html             # الصفحة الرئيسية
│   ├── marketing/                 # التسويق
│   │   └── PITCH.md               # العرض التقديمي
│   ├── n8n-workflows/             # أتمتة n8n
│   │   ├── lead_capture.json
│   │   ├── auto_nurturing.json
│   │   └── payment_onboarding.json
│   ├── nginx/                     # إعدادات Nginx
│   │   └── nexus_unified.conf
│   ├── planets/                   # 12 كوكب ذكاء
│   │   ├── AI-ARCH/
│   │   ├── AS-SULTAN/
│   │   ├── CLONE-HUB/
│   │   ├── LEGAL-EAGLE/
│   │   ├── NAV-ORACLE/
│   │   ├── NEXUS-ANALYST/
│   │   ├── N-TARGET/
│   │   ├── OPS-CTRL/
│   │   ├── RAG-CORE/
│   │   ├── SEC-GUARD/
│   │   ├── SHADOW-7/
│   │   └── X-BIO/
│   ├── products/                  # 7 منتجات (symlinks)
│   ├── scripts/                   # سكريبتات النظام
│   │   ├── IGNITION.sh
│   │   ├── git_sync_all.sh
│   │   ├── PHASE4_LAUNCH.sh
│   │   ├── setup_dns.sh
│   │   ├── final_test.sh
│   │   └── ...
│   ├── MASTER_DOCUMENTATION.md    # ← هذا الملف
│   ├── README.md
│   └── DEPLOYMENT.md
│
├── products/                      # المنتجات المحلية
│   ├── shadow-seven-publisher/    # Shadow Seven (168 files)
│   ├── alsultan-intelligence/     # AlSultan (5 files)
│   ├── jarvis-control-hub/        # Jarvis (9 files)
│   ├── imperial-ui/               # Imperial UI (14 files)
│   ├── mrf103-mobile/             # MRF103 Mobile (89 files)
│   ├── xbio-sentinel/             # X-BIO (13 files)
│   └── nexus-data-core/           # Data Core (2 files)
│
├── nexus_prime/
│   └── docker-compose.yml         # Docker المباشر
│
└── /etc/
    ├── nginx/sites-available/
    │   └── nexus_unified           # إعدادات Nginx الموحدة
    └── letsencrypt/live/
        └── mrf103.com/             # شهادة SSL Wildcard
```

---

## 📊 ملخص الأرقام

| المقياس | القيمة |
|---------|--------|
| إجمالي الملفات | ~55,000+ |
| حجم النظام الموحد | 3.9 GB |
| GitHub Repos (نشطة) | 9 |
| GitHub Repos (أرشيف) | 21 |
| منتجات | 7 |
| كواكب (وكلاء ذكاء) | 12 |
| تكاملات | 5 |
| حاويات Docker | 5 نشطة + 1 معرّف |
| دومينات فرعية | 15 |
| أتمتة n8n | 3 |
| نتيجة الاختبار | 100% (41/41) ✅ |
| المساحة المحررة | 13 GB |
| المساحة المستخدمة | 191 GB / 451 GB (45%) |

---

## ⚡ أوامر سريعة

```bash
# تشغيل النظام
cd /root/NEXUS_PRIME_UNIFIED && bash scripts/IGNITION.sh

# حالة النظام
docker ps && systemctl status nginx

# مزامنة GitHub
bash /root/NEXUS_PRIME_UNIFIED/scripts/git_sync_all.sh

# اختبار شامل
bash /root/NEXUS_PRIME_UNIFIED/scripts/final_test.sh

# إعادة تشغيل Docker
cd /root/nexus_prime && docker compose restart

# تجديد SSL
certbot renew

# فحص DNS
bash /root/NEXUS_PRIME_UNIFIED/scripts/setup_dns.sh
```

---

## 📅 سجل التغييرات

| التاريخ | الحدث |
|---------|-------|
| 2026-02-10 | المرحلة 0: الاكتشاف (105GB) |
| 2026-02-10 | المرحلة 1: التوحيد (13GB محررة) |
| 2026-02-11 | المرحلة 2: التحويل لمنتجات (7 منتجات) |
| 2026-02-12 | المرحلة 3: التكامل (5 مكونات) |
| 2026-02-16 | المرحلة 4: التتجير (Stripe, DNS, SSL, n8n) |
| 2026-02-17 | مزامنة GitHub (9/9 repos) |
| 2026-02-17 | التوثيق الشامل v2.1.0 |
| 2026-02-17 | إصلاح أمني: إزالة مفاتيح API مكشوفة (OpenAI + Gemini) |
| 2026-02-18 | اختبار شامل: 41/41 = 100% ✅ |
| 2026-02-18 | إصلاح nexus-backup: mysqldump → pg_dump |
| 2026-02-18 | استطلاع عميق للنظام + تحديث التوثيق v2.2.0 |
| 2026-02-18 | إضافة: Model Vault، API Map، Security Fixes |

---

> **NEXUS PRIME v2.2.0** - Built by MrF  
> آخر تحديث: 18 فبراير 2026
