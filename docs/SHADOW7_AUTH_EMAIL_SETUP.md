# الظل السابع — إعداد التسجيل والإيميل

## ما تم تنفيذه

### 1. Nginx — إضافة `/rest/v1/` لتسجيل الدخول
- **الملف:** `infrastructure/nginx/nexus_unified.conf`
- **التعديل:** إضافة `location /rest/v1/` لتوجيه طلبات Supabase (login, register) إلى PostgREST (3001)

### 2. الفرونت — إيميل الترحيب بعد التسجيل
- **الملف:** `products/shadow-seven-publisher/Pages/LoginPage.jsx`
- **التعديل:** استدعاء `/api/shadow7/email/template` بعد نجاح التسجيل لإرسال إيميل الترحيب

### 3. الربط
| المكون | المصدر | الوجهة |
|--------|--------|--------|
| تسجيل / دخول | Supabase client → `/rest/v1/rpc/` | PostgREST (3001) → nexus_db |
| إيميل الترحيب | LoginPage → `/api/shadow7/email/template` | shadow7_api (8002) → nexus_db (email_log) |
| المخطوطات | UploadPage → `/api/shadow7/manuscripts/upload` | shadow7_api → nexus_db (manuscripts) |

---

## أوامر يجب تنفيذها يدوياً

```bash
# 1. إعادة تحميل Nginx
sudo nginx -t && sudo systemctl reload nginx

# 2. بناء ونشر الفرونت
cd /root/products/shadow-seven-publisher && npm run build
sudo cp -r dist/* /var/www/publisher/
```

---

## التحقق

```bash
# اختبار تسجيل عبر REST
curl -sk -X POST https://publisher.mrf103.com/rest/v1/rpc/register \
  -H "Content-Type: application/json" \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoid2ViX2Fub24iLCJpYXQiOjE3NzE4OTMyMjMsImV4cCI6OTk5OTk5OTk5OX0.sONQE61sh6WTmd4XRDu2NZfifHBkR7AR-6UOHJZzw3s" \
  -d '{"p_email":"test@example.com","p_password":"123456","p_full_name":"Test"}'
```

---

## إعداد SMTP (لإرسال الإيميلات فعلياً)

في `products/shadow-seven-publisher/backend/config.py` أو `.env`:
```
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
FROM_EMAIL=publisher@mrf103.com
```

بدون SMTP، الإيميلات تُسجّل في `email_log` فقط ولا تُرسل.
