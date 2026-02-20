# 🚀 دليل النشر على Railway

## المتطلبات الأساسية
- ✅ حساب على [Railway.app](https://railway.app/)
- ✅ مشروع Supabase نشط
- ✅ GitHub Repository متصل

## خطوات النشر

### 1️⃣ ربط المشروع
```bash
# اذهب إلى Railway Dashboard
# New Project > Deploy from GitHub repo
# اختر: firas103103-oss/777
```

### 2️⃣ إعداد المتغيرات البيئية

في تبويب **Variables** أضف:

```env
SUPABASE_URL=https://udcwitnnogxrvoxefrge.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVkY3dpdG5ub2d4cnZveGVmcmdlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzMTUwNTcsImV4cCI6MjA4MDg5MTA1N30.SfPkepVomW4bwFSi1lhS81d-nSlNgYQ3jhjtHri8hhg
GEMINI_API_KEY=AIzaSyCyHegfv5nzDNx-CaxZ2mI3daAukizoYUo
```

⚠️ **لا تضف** `SUPABASE_SERVICE_ROLE_KEY` في المتغيرات البيئية (خطير).

### 3️⃣ إعداد Supabase

1. افتح [Supabase Dashboard](https://app.supabase.com)
2. اذهب إلى: **Authentication** > **URL Configuration**
3. أضف رابط Railway في:
   - `Site URL`
   - `Redirect URLs`

### 4️⃣ انتظار البناء

Railway سيقوم تلقائياً بـ:
- ✅ تثبيت المكتبات (`npm install`)
- ✅ حقن المتغيرات البيئية
- ✅ بناء المشروع (`npm run build`)
- ✅ تشغيل السيرفر (`npm start`)

### 5️⃣ الوصول للموقع

بعد ظهور ✅ اضغط على الرابط المعطى من Railway.

---

## 🛠️ التطوير المحلي

```bash
# تثبيت
npm install

# تشغيل محلي
npm run dev

# بناء
npm run build

# تجربة الإنتاج
npm start
```

## 🔐 نظام التوثيق

- Magic Link عبر البريد الإلكتروني
- لا حاجة لكلمات مرور
- آمن بنسبة 100%

## ✅ حالة المشروع

- [x] البنية جاهزة
- [x] نظام التوثيق متكامل
- [x] حماية المسارات مفعلة
- [x] البناء يعمل بنجاح
- [x] Express Server جاهز
- [x] Environment Injection يعمل
