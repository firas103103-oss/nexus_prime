# الظل السابع — قائمة التحقق للرفع

**تم إصلاح أخطاء الرفع (Read length + 500).**

---

## ما تم إصلاحه (27 شباط 2026)

| المشكلة | الحل |
|---------|------|
| `max_part_size` غير مدعوم | ترقية Starlette إلى 0.40+ و FastAPI إلى 0.115+ |
| `column "metadata" does not exist` | إضافة عمود `metadata` إلى جدول manuscripts |

---

## 1. إعادة بناء وتشغيل shadow7_api

```bash
cd /root/NEXUS_PRIME_UNIFIED
docker compose build shadow7_api
docker compose up -d shadow7_api
```

---

## 2. إعادة تحميل Nginx

```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## 3. إضافة عمود metadata (إذا لزم)

```bash
docker exec nexus_db psql -U postgres -d nexus_db -c \
  "ALTER TABLE manuscripts ADD COLUMN IF NOT EXISTS metadata JSONB;"
```

---

## 4. اختبار الرفع

```bash
cd /root/NEXUS_PRIME_UNIFIED/products/shadow-seven-publisher/backend
SHADOW7_API_URL=http://127.0.0.1:8002 python3 test_upload_integrity.py
```

---

## 5. التحقق من السجلات

```bash
docker logs shadow7_api --tail 50
```

---

## ملخص الحالة

| البند | الحالة |
|-------|--------|
| Starlette 0.48 + max_part_size 100MB | ✅ |
| Backend: قراءة chunked | ✅ |
| Nginx: client_max_body_size 100M | ✅ |
| عمود metadata في manuscripts | ✅ |
| اختبار الرفع (~1MB) | ✅ نجح |
