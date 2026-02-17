# Supabase Database Setup

## إعداد قاعدة البيانات

### ١. إنشاء مشروع Supabase جديد

1. اذهب إلى [https://supabase.com](https://supabase.com)
2. أنشئ مشروع جديد
3. احفظ الـ credentials:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_KEY`

### ٢. تنفيذ Schema

1. افتح Supabase Dashboard → SQL Editor
2. انسخ محتوى `schema.sql`
3. نفذ الـ SQL script

### ٣. تفعيل Authentication

1. Authentication → Settings
2. فعّل Email/Password provider
3. اضبط Email Templates (اختياري)
4. اضبط Redirect URLs:
   - `http://localhost:3000`
   - `https://your-production-url.com`

### ٤. إعداد Storage (اختياري)

إذا أردت حفظ الملفات المرفوعة:

```sql
-- Create storage bucket for manuscripts
INSERT INTO storage.buckets (id, name, public)
VALUES ('manuscripts', 'manuscripts', false);

-- Storage policy
CREATE POLICY "Users can upload manuscripts"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'manuscripts' 
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can view own manuscripts"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'manuscripts' 
    AND auth.uid()::text = (storage.foldername(name))[1]
  );
```

### ٥. اختبار الـ Setup

```typescript
// Test connection
import { supabase } from './supabase';

async function testConnection() {
  const { data, error } = await supabase
    .from('manuscripts')
    .select('count');
  
  if (error) {
    console.error('Connection failed:', error);
  } else {
    console.log('✅ Connected to Supabase');
  }
}
```

## الجداول المنشأة

### 1. `users`
- يمتد من `auth.users`
- يحفظ معلومات إضافية للمستخدم

### 2. `manuscripts`
- يحفظ جميع المخطوطات
- RLS enabled - كل مستخدم يرى مخطوطاته فقط

### 3. `processing_history`
- يتتبع خطوات المعالجة
- مفيد للـ analytics والـ debugging

## Security Notes

- ✅ Row Level Security (RLS) مفعّل على جميع الجداول
- ✅ Users يمكنهم فقط الوصول لبياناتهم الخاصة
- ✅ Service Role key للـ backend operations فقط
- ⚠️ لا تشارك `SUPABASE_SERVICE_KEY` أبداً في Frontend!
