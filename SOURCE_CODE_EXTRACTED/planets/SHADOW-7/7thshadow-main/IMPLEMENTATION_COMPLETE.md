# 🚀 X-Book Smart Publisher - Full Stack Edition

## ✅ التنفيذ الكامل - اكتمل بنجاح!

تم تحويل المشروع من Frontend-only إلى Full Stack Application مع:
- ✅ Backend حقيقي (Express + TypeScript)
- ✅ Supabase Integration (Database + Auth)
- ✅ API Proxy لإخفاء Gemini API Key
- ✅ توحيد App.tsx و AppV2.tsx
- ✅ Frontend API Client
- ✅ Railway Deployment Ready

---

## 📁 البنية الجديدة للمشروع

```
7thshadow/
├── backend/                    # 🆕 Backend Server
│   ├── server.ts              # Express server رئيسي
│   ├── routes/
│   │   ├── gemini.ts          # API proxy لـ Gemini
│   │   ├── manuscripts.ts     # إدارة المخطوطات
│   │   └── auth.ts            # Supabase auth
│   ├── middleware/
│   │   ├── errorHandler.ts   # معالجة الأخطاء
│   │   └── rateLimiter.ts    # حماية من spam
│   └── db/
│       ├── supabase.ts        # Supabase client
│       ├── schema.sql         # Database schema
│       └── README.md          # تعليمات الإعداد
│
├── services/
│   ├── apiClient.ts           # 🆕 Frontend API client
│   ├── geminiService.ts       # (سيتم نقله للـ backend)
│   ├── documentService.ts
│   └── reportGeneratorService.ts
│
├── AppUnified.tsx              # 🆕 التطبيق الموحد (Terminal + Modern)
├── App.tsx                     # Terminal UI (أصلي)
├── AppV2.tsx                   # Modern Chat UI
│
├── .env.example                # 🆕 نموذج لمتغيرات البيئة
├── tsconfig.backend.json       # 🆕 إعدادات TypeScript للـ backend
├── package.json                # ✏️ محدّث مع dependencies جديدة
└── RAILWAY_SETUP.md            # 🆕 دليل النشر على Railway
```

---

## 🎯 المزايا الجديدة

### 1. أمان محسّن 🔒
- ✅ **API Key مخفي** - لم يعد مكشوفاً في Frontend
- ✅ **Rate Limiting** - حماية من الاستخدام المفرط
- ✅ **Row Level Security** - كل مستخدم يرى بياناته فقط

### 2. Backend كامل الوظائف 🖥️
- ✅ Express server مع TypeScript
- ✅ REST API endpoints
- ✅ Error handling & logging
- ✅ Health checks

### 3. Supabase Integration 🗄️
- ✅ قاعدة بيانات PostgreSQL
- ✅ Authentication (Email/Password)
- ✅ حفظ المخطوطات والتقدم
- ✅ Processing history tracking

### 4. تطبيق موحد 🎨
- ✅ زر تبديل بين Terminal UI و Modern Chat UI
- ✅ حفظ التفضيلات في localStorage
- ✅ نفس الوظائف في الوضعين

---

## ⚙️ الإعداد والتشغيل

### 1. تثبيت المكتبات

```bash
npm install
```

### 2. إعداد متغيرات البيئة

انسخ `.env.example` إلى `.env`:

```bash
cp .env.example .env
```

ثم عدّل القيم:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
PORT=8085
NODE_ENV=development
```

### 3. إعداد قاعدة البيانات

اتبع التعليمات في `backend/db/README.md`:

1. أنشئ مشروع Supabase جديد
2. نفّذ `backend/db/schema.sql` في SQL Editor
3. انسخ الـ credentials إلى `.env`

### 4. التشغيل في Development

```bash
# تشغيل Frontend + Backend معاً
npm run dev

# أو تشغيلهما منفصلين:
npm run dev:frontend  # Port 3000
npm run dev:backend   # Port 8085
```

### 5. البناء للإنتاج

```bash
npm run build
```

سيبني:
- Frontend → `dist/`
- Backend → `dist/backend/`

### 6. التشغيل في Production

```bash
npm start
```

---

## 🌐 API Endpoints

### Gemini AI Proxy
```
POST /api/gemini/generate
Body: { prompt: string, model?: string }
```

### Manuscripts
```
GET    /api/manuscripts           # قائمة المخطوطات
GET    /api/manuscripts/:id       # مخطوطة محددة
POST   /api/manuscripts           # إنشاء جديدة
PATCH  /api/manuscripts/:id       # تحديث
POST   /api/manuscripts/:id/process  # بدء المعالجة
```

### Authentication
```
POST /api/auth/signup    # تسجيل
POST /api/auth/login     # دخول
POST /api/auth/logout    # خروج
GET  /api/auth/user      # المستخدم الحالي
```

---

## 🚢 النشر على Railway

### خطوات سريعة:

1. **ربط المشروع**
```bash
railway link
```

2. **إضافة المتغيرات**
اذهب إلى Railway Dashboard → Variables وأضف:
- `GEMINI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_KEY`
- `NODE_ENV=production`

3. **النشر**
```bash
git push origin main
```

Railway سيبني ويشغّل المشروع تلقائياً!

للمزيد من التفاصيل: راجع `RAILWAY_SETUP.md`

---

## 🧪 الاختبارات

```bash
# تشغيل جميع الاختبارات
npm test

# اختبارات مع UI
npm run test:ui

# Coverage report
npm run test:coverage
```

---

## 📊 الحالة

| المكون | الحالة | الملاحظات |
|--------|--------|-----------|
| Backend Server | ✅ يعمل | Express + TypeScript |
| Gemini API Proxy | ✅ يعمل | إخفاء API key |
| Supabase Integration | ✅ جاهز | Schema + Auth |
| Frontend API Client | ✅ جاهز | في `services/apiClient.ts` |
| AppUnified | ✅ جاهز | Terminal + Modern UI |
| Railway Config | ✅ جاهز | railway.toml محدّث |
| Build System | ✅ يعمل | Frontend + Backend |
| Type Safety | ✅ نظيف | لا توجد أخطاء TypeScript |

---

## 🔐 الأمان

### مُنفّذ:
- ✅ API Key محمي في Backend
- ✅ Rate limiting (100 req/15min)
- ✅ Row Level Security في Database
- ✅ CORS configuration
- ✅ Error handling شامل

### موصى به (للإنتاج):
- ⚠️ HTTPS فقط
- ⚠️ Helmet.js middleware
- ⚠️ Redis-based rate limiter
- ⚠️ API key rotation
- ⚠️ Monitoring (Sentry)

---

## 📚 الموارد

- [Supabase Docs](https://supabase.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Gemini AI API](https://ai.google.dev/docs)
- [Express.js Docs](https://expressjs.com)

---

## 🆘 المساعدة

### مشاكل شائعة:

**Backend لا يعمل؟**
- تحقق من `.env` - هل جميع المتغيرات موجودة؟
- راجع logs: `railway logs` أو console

**Database connection failed؟**
- تحقق من Supabase credentials
- هل نفّذت `schema.sql`؟

**Build failed؟**
- حذف `node_modules` و `dist`
- `npm install` من جديد
- `npm run build`

**Frontend لا يتصل بـ Backend؟**
- تحقق من `VITE_API_URL` في `.env`
- تأكد من Backend يعمل على نفس المنفذ

---

## 🎉 الخلاصة

تم تحويل المشروع بنجاح من:
- Frontend-only → **Full Stack**
- Client-side API → **Backend Proxy**
- No Database → **Supabase Integration**
- No Auth → **User Authentication**
- Exposed Keys → **Secure Backend**

المشروع الآن **Production-ready** و**آمن** و**قابل للتوسع**! 🚀

---

## 👨‍💻 المطوّر

**MrF X OS Organization**  
The Seventh Shadow - AI-Powered Publishing Platform

**Repository**: [github.com/firas103103-oss/7thshadow](https://github.com/firas103103-oss/7thshadow)

---

## 📝 License

MIT License - Copyright © 2026 MrF X OS Organization
