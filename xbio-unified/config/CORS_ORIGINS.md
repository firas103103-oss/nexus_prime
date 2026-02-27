# CORS Origins — xbio_core.py

النطاقات المسموحة حاليماً لطلبات الـ API من المتصفح:

| النطاق | الاستخدام |
|--------|-----------|
| https://xbio.mrf103.com | X-BIO API نفسه |
| https://dashboard.mrf103.com | لوحة التحكم الرئيسية |
| https://publisher.mrf103.com | Shadow Seven |
| https://mrf103.com | الموقع الرئيسي |
| http://localhost:5001 | تطوير Dashboard |
| http://localhost:3000 | تطوير React/Vite |

**إضافة نطاق جديد:** عدّل `allow_origins` في `products/xbio-sentinel/xbio_core.py`.
