# Ecosystem API (8005)

**الحالة:** خدمة منفصلة — خارج docker-compose الرئيسي  
**المصدر:** `SOURCE_CODE_EXTRACTED/integration/ecosystem-api/`  
**المنفذ:** 8005

---

## الوصف

Ecosystem API هي نقطة دخول موحدة للـ APIs تُستخدم من nginx للدومينات:
- mrf103.com (/api/)
- sultan.mrf103.com (/api/)
- admin.mrf103.com (/api/)
- api.mrf103.com
- platform.mrf103.com (/api/)
- data.mrf103.com

## التشغيل

```bash
# من مجلد المشروع
cd SOURCE_CODE_EXTRACTED/integration/ecosystem-api
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8005
```

أو عبر pm2/systemd حسب الإعداد الحالي.

## Endpoints

| المسار | الوصف |
|--------|-------|
| GET / | رسالة ترحيب |
| GET /api/v1/health | حالة الصحة — clone_hub، ecosystem_api، nexus_prime |
| GET /api/v1/products | قائمة المنتجات |
| GET /api/v1/products/{name} | تفاصيل منتج |
| POST /api/v1/approvals | إنشاء طلب موافقة |

## التوحيد المستقبلي

لإضافة Ecosystem API إلى docker-compose، انسخ مجلد `integration/ecosystem-api` خارج SOURCE_CODE_EXTRACTED ثم أضف خدمة في docker-compose.yml.
