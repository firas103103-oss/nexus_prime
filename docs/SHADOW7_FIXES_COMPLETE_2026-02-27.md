# الظل السابع — إصلاحات كاملة 27 شباط 2026

## 1. خطأ 405 على /ai (Ollama)

**المشكلة:** `Ollama 405: Not Allowed` عند استدعاء المساعد الذكي أو التصدير.

**السبب:** لم يكن هناك `location /ai/` في Nginx لـ publisher.mrf103.com، فطلبات POST كانت تصل إلى `location /` (ملفات ثابتة) التي ترفض POST.

**الحل:** إضافة `location /ai/` في `infrastructure/nginx/nexus_unified.conf`:

```nginx
location /ai/ {
    if ($request_method = OPTIONS) { return 204; }
    proxy_pass http://127.0.0.1:11434/;
    proxy_set_header Host $host;
    proxy_http_version 1.1;
    proxy_read_timeout 300s;
    ...
}
```

**التحقق:** محلياً يعمل (HTTP 200):
```bash
curl -sk -X POST https://127.0.0.1/ai/v1/chat/completions \
  -H "Host: publisher.mrf103.com" -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:3b","messages":[{"role":"user","content":"hi"}],"stream":false}'
```

**إذا استمر 405 عبر Cloudflare:**
- Purge Cache في Cloudflare
- أو: Page Rule لـ `publisher.mrf103.com/ai/*` → Cache Level: Bypass
- أو: تحقق من WAF/Firewall Rules التي قد تحجب POST

---

## 2. إصلاحات Backend (Submit → n8n → Download)

| الملف | التعديل |
|-------|---------|
| main.py | Payload: إضافة target_audience, book_genre, tone على المستوى الأعلى |
| main.py | callback_url: `http://shadow7_api:8002/api/shadow7/callback` |
| main.py | save_outline: book_summary, chapter_count |
| main.py | save_chapter: chapter_title، إزالة ON CONFLICT |
| main.py | save_reports: DELETE ثم INSERT |
| main.py | create_package: chapter_title, book_summary, zip_file_size |
| main.py | create_package: إرجاع tracking_id |
| models.py | N8NCallbackPayload: إضافة حقل error |

---

## 3. إصلاحات n8n Workflow

| العقدة | الغرض |
|--------|-------|
| Restore Outline Data | استرجاع outline/chapters بعد Save Outline |
| Restore For Package | استرجاع tracking_id قبل Create Package |

---

## 4. أوامر التشغيل

```bash
# Nginx
sudo cp /root/NEXUS_PRIME_UNIFIED/infrastructure/nginx/nexus_unified.conf /etc/nginx/conf.d/
sudo nginx -t && sudo systemctl reload nginx

# shadow7_api
cd /root/NEXUS_PRIME_UNIFIED
docker compose build shadow7_api
docker compose up -d shadow7_api

# استيراد workflow في n8n
cd n8n-workflows
./deploy_workflows.sh
```

---

## 5. اختبار المسار الكامل

1. تسجيل / دخول → publisher.mrf103.com
2. رفع مخطوط أو Submit Wizard
3. Export (PDF/EPUB) → يستخدم /ai/v1/chat/completions
4. تحميل الحزمة من /api/shadow7/download/{tracking_id}
