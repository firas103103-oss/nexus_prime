# ملاحظات التقليل والتوحيد — Consolidation Notes

**التاريخ:** 2026-02-23

---

## 1. SOURCE_CODE_EXTRACTED

**الحالة:** أرشيف للكود المستخرج — يُستخدم لـ:
- integration/ecosystem-api (Ecosystem API على 8005)
- integration/clone-hub (Clone Hub — نسخة في integration/)
- نسخ من المنتجات للمرجع

**التوصية:**
- عدم حذف — قد يُستخدم ecosystem-api
- عند التوحيد: نسخ `integration/ecosystem-api` و `integration/clone-hub` خارج SOURCE_CODE_EXTRACTED إلى مجلد `integration/` رئيسي
- إضافة docker-compose service لـ ecosystem-api إن أمكن

---

## 2. GRAVEYARD_DIG

**الموقع:** `SOURCE_CODE_EXTRACTED/products/aura-ar-3d/GRAVEYARD_DIG/`

**المحتوى:** نسخ أرشيفية من مشاريع (mrf103ArUserXp، arc-namer-cli، إلخ)

**التوصية:**
- الإبقاء على aura-ar-3d كمصدر رئيسي
- GRAVEYARD_DIG للتاريخ فقط — لا يُستخدم في التشغيل
- عند التنظيف: أرشفة GRAVEYARD_DIG كـ .tar.gz خارج المشروع إن احتجنا مساحة

---

## 3. X-BIO توحيد

**المواقع:**
- `planets/X-BIO/` — هوية الكوكب
- `products/xbio-sentinel/` — قد يكون في مكان آخر
- `nexus_xbio` في docker-compose

**التوصية:**
- planets/X-BIO = الهوية (identity.json)
- nexus_xbio = الخدمة التشغيلية (من docker-compose)
- توثيق الربط بينهما في MRF_MASTER_SOURCE_DOCUMENT
