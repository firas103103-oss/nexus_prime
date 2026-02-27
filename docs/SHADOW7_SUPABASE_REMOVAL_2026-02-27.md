# الظل السابع — إزالة Supabase واستبداله بـ PostgreSQL
**التاريخ:** 27 شباط 2026

---

## ملخص التنفيذ

تم إزالة Supabase بالكامل واستبداله بـ PostgreSQL عبر FastAPI Backend.

---

## التغييرات المنفذة

### 1. Backend (main.py)
- إضافة مسارات Auth: `/api/shadow7/auth/login`, `register`, `validate`, `logout`, `update-profile`
- استدعاء دوال PostgreSQL: `login()`, `register()`, `validate_session()`, `logout()`, `update_profile()`

### 2. Frontend
- **حذف:** `api/supabaseClient.js`
- **إنشاء:** `api/backendClient.js` — authApi, manuscriptsApi, uploadManuscriptFile
- **تحديث:** `api/index.js` — استخدام backendClient بدل supabaseClient
- **تحديث:** `contexts/AuthContext.jsx` — استخدام authApi
- **تحديث:** `contexts/CollaborationContext.jsx` — إزالة Supabase Realtime (no-op)
- **تحديث:** `api/fileService.js` — استخدام uploadManuscriptFile
- **تحديث:** `Pages/AnalyticsDashboardPage.jsx` — استخدام manuscriptsApi

### 3. التبعيات
- **إزالة:** `@supabase/supabase-js` من package.json

### 4. الملفات المحذوفة
- `api/supabaseClient.js`
- `scripts/generate-postgrest-jwt.js`
- `scripts/supabase-init.sql`

### 5. الإعدادات
- `.env.example` — إزالة VITE_SUPABASE_*
- `tests/setup.js` — VITE_API_URL
- `scripts/check-railway-ready.sh` — VITE_API_URL
- `docs/ENV_SETUP.md` — تحديث كامل

---

## مسارات Auth الجديدة

| المسار | الوظيفة |
|-------|---------|
| POST /api/shadow7/auth/login | تسجيل الدخول |
| POST /api/shadow7/auth/register | التسجيل |
| POST /api/shadow7/auth/validate | التحقق من الجلسة |
| POST /api/shadow7/auth/logout | تسجيل الخروج |
| POST /api/shadow7/auth/update-profile | تحديث الملف الشخصي |

---

## الاختبار

- ✅ اختبار الرفع: 4/4 مراحل نجحت
- ✅ Build: نجح
- ✅ shadow7_api: يعمل

---

## النشر

```bash
cd /root/products/shadow-seven-publisher
npm run build
cp -r dist/* /var/www/publisher/

cd /root/NEXUS_PRIME_UNIFIED
docker compose build shadow7_api
docker compose up -d shadow7_api
```
