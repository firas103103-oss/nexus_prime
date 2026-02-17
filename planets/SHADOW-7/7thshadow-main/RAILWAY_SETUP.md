# Railway Deployment Configuration

## متغيرات البيئة المطلوبة في Railway

أضف هذه المتغيرات في Railway Dashboard → Variables:

```
GEMINI_API_KEY=<your_gemini_api_key>
SUPABASE_URL=<your_supabase_url>
SUPABASE_ANON_KEY=<your_supabase_anon_key>
SUPABASE_SERVICE_KEY=<your_supabase_service_key>
PORT=8085
NODE_ENV=production
FRONTEND_URL=https://your-app.railway.app
```

## خطوات النشر

### ١. إعداد Railway Project

```bash
# تثبيت Railway CLI
npm i -g @railway/cli

# تسجيل الدخول
railway login

# ربط المشروع
railway link
```

### ٢. إضافة المتغيرات

```bash
# إضافة متغيرات البيئة
railway variables set GEMINI_API_KEY=<key>
railway variables set SUPABASE_URL=<url>
railway variables set SUPABASE_ANON_KEY=<key>
railway variables set SUPABASE_SERVICE_KEY=<key>
railway variables set NODE_ENV=production
```

### ٣. النشر

```bash
# نشر تلقائي
git push origin main

# أو نشر يدوي
railway up
```

## Health Check

سيتحقق Railway من `/health.json` كل ٦٠ ثانية:

```json
{
  "status": "ok",
  "timestamp": "2026-01-15T...",
  "service": "x-book-backend"
}
```

## Logs & Monitoring

```bash
# عرض الـ logs
railway logs

# متابعة الـ logs بشكل مباشر
railway logs -f
```

## Custom Domain (اختياري)

1. اذهب إلى Settings → Domains
2. أضف Domain مخصص
3. اضبط DNS records

## Troubleshooting

### المشكلة: Build Failed
```bash
# تحقق من الـ logs
railway logs

# تأكد من وجود جميع المتغيرات
railway variables
```

### المشكلة: Health Check Failed
- تحقق من أن `/health.json` يعمل
- تأكد من PORT صحيح
- راجع backend logs

### المشكلة: Database Connection Failed
- تحقق من Supabase credentials
- تأكد من أن IP allowed في Supabase
- راجع connection string

## Performance Optimization

### تفعيل Caching
```toml
[build]
cacheMount = "node_modules"
```

### تحسين Build Time
```json
{
  "scripts": {
    "railway:build": "npm ci --legacy-peer-deps && npm run build"
  }
}
```

## Backup & Rollback

```bash
# عرض التنصيبات السابقة
railway deployments

# الرجوع لنسخة سابقة
railway rollback <deployment-id>
```
