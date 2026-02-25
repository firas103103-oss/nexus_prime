# NEXUS PRIME — نظرة وحوصة

**التاريخ:** 2026-02-25

---

## 1. البنية المعمارية (نظرة عامة)

```
Cloudflare (Proxied) → Nginx (SSL) → خدمات Docker
```

| الطبقة | المكونات |
|--------|----------|
| **DNS** | Cloudflare — كل النطاقات على mrf103.com |
| **Reverse Proxy** | Nginx — SSL، توجيه حسب Host |
| **Core** | nexus_db, nexus_redis, nexus_ollama, nexus_litellm |
| **AI** | Dify, nexus_ai (Open WebUI), nexus_oracle |
| **Cortex** | nexus_cortex, nexus_nerve, neural_spine, reflex_agents |
| **Gateway** | sovereign_gateway, sovereign_dify_bridge |
| **Ecosystem** | ecosystem_api, shadow7_api, nexus_postgrest |

---

## 2. مسار الـ LLM (من Dify إلى Ollama)

```
المتصفح → dify.mrf103.com → Dify API
                ↓
         llm.mrf103.com (Nginx) → nexus_litellm:4000 (LiteLLM)
                ↓
         nexus_ollama:11434 (Ollama) → llama3.2:3b
```

- **Dify** يصل لـ LiteLLM عبر `https://llm.mrf103.com` (يصل من المتصفح)
- **LiteLLM** يوجّه `gpt-4o` إلى `llama3.2:3b` المحلي
- **Ollama** يشغّل النموذج محلياً

---

## 3. ما تم إنجازه (حوصة)

| البند | الحالة |
|-------|--------|
| Nginx | enabled + active |
| SSL | Let's Encrypt |
| الحاويات | 40+ Up (nexus + dify + monitoring) |
| Dify | يعمل على dify.mrf103.com |
| llm.mrf103.com | Nginx + DNS — للوصول من المتصفح |
| Model Provider | OpenAI → https://llm.mrf103.com |
| Chatflow | تم إنشاؤه مع gpt-4o |

---

## 4. الروابط الرئيسية

| النطاق | الخدمة |
|--------|--------|
| dify.mrf103.com | Dify — workflows و chatflows |
| dashboard.mrf103.com | Dashboard ARC |
| chat.mrf103.com, ai.mrf103.com | Open WebUI |
| api.mrf103.com | Ecosystem API |
| cortex.mrf103.com | Cortex API |
| gateway.mrf103.com | Sovereign Gateway |
| llm.mrf103.com | LiteLLM (للمطورين) |

---

## 5. الملفات المرجعية

| الملف | الغرض |
|-------|-------|
| docs/USER_CHECKLIST_MINIMAL.md | الخطوات اليدوية |
| docs/DIFY_VERIFICATION_AND_DNS_MAP.md | DNS + Dify |
| docs/SOVEREIGN_EXECUTIVE_CHECKLIST_FINAL_ACTIVATION.md | قائمة التفعيل |
| scripts/verify_nexus_pulse.sh | التحقق السريع |

---

## 6. أوامر التحقق

```bash
cd /root/NEXUS_PRIME_UNIFIED
./scripts/verify_nexus_pulse.sh
```

---

**التوقيع:** Principal Systems Architect
