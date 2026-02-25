# NEXUS PRIME — الخطوات اليدوية فقط

**التاريخ:** 2026-02-25

---

## ما تم تنفيذه آلياً

- Nginx، SSL، الحاويات، المنافذ
- Dify مضبوط على LiteLLM: `http://nexus_litellm:4000/v1`

---

## ما تحتاج تنفيذه (3 خطوات)

### 1. Cloudflare
SSL/TLS → Full (strict) | DNS → Proxied

### 2. Cloudflare DNS
أضف سجل: `llm` → `46.224.225.96` (أو IP السيرفر)

### 3. Dify Model Provider
Settings → Model Provider → **OpenAI**:
- API Key: `sk-nexus-sovereign-mrf103`
- API Base: `https://llm.mrf103.com` (بدون /v1 — Dify يضيفه)
- Model Name: `gpt-4o`

### 4. Dify Knowledge (اختياري)
Knowledge → Create → ارفع `docs/SOVEREIGN_ENCYCLOPEDIA.md`

---

## التحقق
```bash
./scripts/verify_nexus_pulse.sh
```
