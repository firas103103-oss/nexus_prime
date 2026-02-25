# Dify — التحقق الكامل + خريطة DNS

**تاريخ:** 2026-02-25

---

## 1. مقارنة DNS مع Nginx — لا يوجد ناقص

كل السجلات اللي عندك في Cloudflare موجودة في Nginx:

| DNS عندك | Nginx | البورت | الحالة |
|----------|-------|--------|--------|
| admin | admin.mrf103.com | 8005 | موصول |
| ai, chat, nexus | ai.mrf103.com, chat.mrf103.com, nexus.mrf103.com | 3000 | موصول |
| api | api.mrf103.com | 8005 | موصول |
| app, dashboard, dash | app, dashboard, dash.mrf103.com | 5001 | موصول |
| boardroom | boardroom.mrf103.com | 8501 | موصول |
| citadel | citadel.mrf103.com | static | موصول |
| cortex | cortex.mrf103.com | 8090 | موصول |
| data | data.mrf103.com | 8005 | موصول |
| dify | dify.mrf103.com | 8085 | موصول |
| finance | finance.mrf103.com | static | موصول |
| flow, n8n | flow, n8n.mrf103.com | 5678 | موصول |
| gateway | gateway.mrf103.com | 9999 | موصول |
| god, sovereign | god, sovereign.mrf103.com | 8888 | موصول |
| grafana | grafana.mrf103.com | 3002 | موصول |
| imperial | imperial.mrf103.com | static | موصول |
| jarvis | jarvis.mrf103.com | static | موصول |
| marketing | marketing.mrf103.com | static | موصول |
| memory | memory.mrf103.com | 9000 | موصول |
| monitor | monitor.mrf103.com | static | موصول |
| mrf103.com, www | mrf103.com, www | 8005 | موصول |
| nerve | nerve.mrf103.com | 8200 | موصول |
| nerve-ui | nerve-ui.mrf103.com | static+8200 | موصول |
| oracle | oracle.mrf103.com | 8100 | موصول |
| platform | platform.mrf103.com | 8005 | موصول |
| prime | prime.mrf103.com | static | موصول |
| publisher | publisher.mrf103.com | 3001+8002 | موصول |
| sultan | sultan.mrf103.com | 8005 | موصول |
| voice | voice.mrf103.com | 5050 | موصول |
| xbio | xbio.mrf103.com | 8080 | موصول |

**النتيجة:** ما في شي ناقص. كل الـ DNS عندك موصولة وبروكسيد.

---

## 2. Dify — التحقق الكامل

### 2.1 الربط الحالي

| المكون | القيمة | الحالة |
|--------|--------|--------|
| **Host/URL** | https://dify.mrf103.com | موصول |
| **Port** | 8085 (Nginx → dify-nginx:80) | موصول |
| **CONSOLE_API_URL** | https://dify.mrf103.com | مضبوط |
| **APP_API_URL** | https://dify.mrf103.com | مضبوط |
| **FILES_URL** | https://dify.mrf103.com | مضبوط |
| **OPENAI_API_BASE** | http://nexus_litellm:4000/v1 | محلي (LiteLLM) |
| **Database** | db_postgres (PostgreSQL) | Dify DB خاص فيه |
| **Redis** | redis (داخل Dify stack) | موصول |
| **Vector DB** | Weaviate | موصول |
| **Network** | nexus_network (عبر override) | يصل لـ nexus_litellm |

### 2.2 الـ Data Flow

```
المتصفح → Cloudflare → Nginx (443) → dify-nginx:8085
                              ↓
                    dify-web:3000 (واجهة)
                    dify-api:5001 (API)
                              ↓
                    nexus_litellm:4000 (LLM محلي)
                    db_postgres (قاعدة Dify)
                    redis (كاش)
```

### 2.3 أوامر التحقق

```bash
# هل Dify يرد؟
curl -sI https://dify.mrf103.com/   # يتوقع 307 أو 200

# هل الحاويات شغالة؟
cd /root/NEXUS_PRIME_UNIFIED/dify/docker
docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify ps
```

### 2.4 إعادة التشغيل (إذا احتجت)

```bash
cd /root/NEXUS_PRIME_UNIFIED/dify/docker
docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify down
docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify up -d
# انتظر ~60 ثانية ثم جرّب https://dify.mrf103.com
```

### 2.5 إصلاح 502 Bad Gateway

إذا ظهر 502 بعد `docker compose up`، السبب غالباً: dify-nginx لا يصل لـ dify-web (Connection refused).

```bash
cd /root/NEXUS_PRIME_UNIFIED/dify/docker
docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify restart nginx web
# انتظر ~15 ثانية ثم جرّب https://dify.mrf103.com
```

### 2.6 إعادة تعيين كلمة مرور الأدمن

```bash
docker exec -it dify-api-1 flask reset-password
```

---

## 3. ملخص

- **DNS:** كل السجلات موصولة، ما في شي ناقص.
- **Dify:** مضبوط، محلي، موصول بـ nexus_litellm وقاعدة بياناته و Redis.
- **الخطوة التالية:** افتح https://dify.mrf103.com، سجّل دخول أو أنشئ حساب أدمن، وارفع موسوعة السلطان كـ Knowledge Base إذا حاب.
