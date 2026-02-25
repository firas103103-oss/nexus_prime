# متطلبات المصادقة الموحدة — كل مشروع ومنصة

**التاريخ:** 2026-02-25  
**المبدأ:** كل مشروع ومنصة لازم يكون فيه تسجيل دخول + إنشاء حساب + إلخ

---

## 1. الوضع الحالي (ماذا موجود)

| المنصة | الرابط | Login | Sign Up | ملاحظات |
|--------|--------|-------|---------|---------|
| **Dashboard ARC** | dashboard.mrf103.com | ✅ | ❌ | operator فقط (سري واحد) |
| **Publisher (Shadow Seven)** | publisher.mrf103.com | ✅ | ✅ | Supabase — يحتاج إعداد |
| **Dify** | dify.mrf103.com | ✅ | ❌ | إدمن فقط، flask reset-password |
| **nexus_auth** | — (8003) | ✅ | ❌ | admin/admin123 فقط — bootstrap |
| **Boardroom** | boardroom.mrf103.com | ❌ | ❌ | — |
| **X-BIO** | xbio.mrf103.com | ❌ | ❌ | — |
| **Platform** | platform.mrf103.com | ❌ | ❌ | — |
| **Chat/AI** | chat.mrf103.com | ❌ | ❌ | Open WebUI — له auth خاص |
| **Gateway/Sultan** | sultan.mrf103.com | ❌ | ❌ | — |
| **Landing** | mrf103.com | ❌ | ❌ | روابط فقط |

---

## 2. المطلوب (كل منصة)

| الميزة | الوصف |
|--------|-------|
| **تسجيل الدخول** | Login — بريد + كلمة مرور |
| **إنشاء حساب** | Sign Up — تسجيل مستخدم جديد |
| **نسيت كلمة المرور** | Password reset |
| **تسجيل خروج** | Logout |
| **جلسة موحدة** | SSO — دخول مرة واحدة لكل المنصات |

---

## 3. البنية المقترحة: nexus_auth كـ SSO

```
                    ┌─────────────────────┐
                    │   nexus_auth:8003   │
                    │   auth.mrf103.com   │
                    │                     │
                    │  • /login           │
                    │  • /signup          │
                    │  • /reset-password  │
                    │  • /verify          │
                    │  • JWKS (RS256)     │
                    └──────────┬──────────┘
                               │ JWT
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
    │Dashboard│          │Publisher│          │Boardroom│
    │         │          │         │          │         │
    │ يتحقق   │          │ يتحقق   │          │ يتحقق   │
    │ من JWT  │          │ من JWT  │          │ من JWT  │
    └─────────┘          └─────────┘          └─────────┘
```

---

## 4. خطة التنفيذ

### المرحلة 1: توسيع nexus_auth
- [ ] إضافة `/api/v1/auth/signup` — إنشاء حساب
- [ ] إضافة `/api/v1/auth/forgot-password` — طلب إعادة تعيين
- [ ] إضافة `/api/v1/auth/reset-password` — تنفيذ الإعادة
- [ ] تخزين المستخدمين في nexus_db (جدول users)
- [ ] إضافة hash لكلمات المرور (bcrypt)

### المرحلة 2: نطاق auth.mrf103.com
- [x] إضافة server block في nginx لـ auth.mrf103.com → 8003
- [ ] إضافة سجل DNS في Cloudflare (auth.mrf103.com → A record)

### المرحلة 3: واجهة تسجيل موحدة
- [ ] صفحة login/signup في auth.mrf103.com (أو مكون مشترك)
- [ ] إعادة توجيه بعد الدخول إلى return_url

### المرحلة 4: ربط المنصات
- [ ] Dashboard: يتحقق من JWT من nexus_auth
- [ ] Publisher: يستبدل Supabase بـ nexus_auth
- [ ] Boardroom: يضيف حماية بـ JWT
- [ ] X-BIO، Platform، إلخ: نفس الطريقة

---

## 5. جدول المستخدمين (nexus_db)

```sql
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 6. ملخص

| البند | الحالة |
|-------|--------|
| nexus_auth موجود | ✅ |
| login فقط (admin/admin123) | ✅ |
| signup | ❌ يحتاج إضافة |
| reset password | ❌ يحتاج إضافة |
| auth.mrf103.com | ✅ تم إضافة nginx (يحتاج DNS) |
| ربط المنصات | ❌ يحتاج تنفيذ |

**الخطوة التالية:** توسيع `integration/shared-auth/main.py` بإضافة signup و reset-password.
