# قائمة جاهزية الإطلاق — Launch Readiness

**التاريخ:** 2026-02-23  
**الهدف:** توليد إيرادات من Shadow Seven، xBio Sentinel، Cognitive Boardroom

---

## 1. Shadow Seven Publisher

| البند | الحالة | ملاحظات |
|-------|--------|---------|
| API (8002) | ✅ | يعمل |
| PostgREST (3001) | ✅ | يعمل |
| publisher.mrf103.com | ✅ | مُعد في nginx |
| تسعير | ✅ | $49–$199–$499/شهر (Starter، Pro، Enterprise) |
| صفحة تسعير | ✅ | /pricing — PricingPage.jsx |
| Stripe/Payment | 🔲 | Ecosystem API — يتطلب STRIPE_SECRET_KEY |
| أول 10 عملاء | 🔲 | استهداف |

---

## 2. xBio Sentinel

| البند | الحالة | ملاحظات |
|-------|--------|---------|
| API (8080) | ✅ | يعمل |
| xbio.mrf103.com | ✅ | مُعد |
| تسعير | ✅ | $299 + $19/شهر |
| صفحة منتج | ✅ | docs/xbio-product-page.html |
| تطبيق أندرويد | 🔲 | ربط بالـ API |
| ESP32/Firmware | 🔲 | توثيق للمشتري |

---

## 3. Cognitive Boardroom

| البند | الحالة | ملاحظات |
|-------|--------|---------|
| Boardroom (8501) | ✅ | يعمل |
| boardroom.mrf103.com | ✅ | مُعد |
| تسعير Enterprise | 🔲 | $500/مقعد أو Custom |
| عرض تجريبي | 🔲 | Demo لـ C-Suite |
| دراسة حالة | 🔲 | إعداد Case Study |

---

## 4. البنية التحتية

| البند | الحالة |
|-------|--------|
| full_health_check | ✅ |
| Ethical Gate | ✅ |
| Clone Hub | ✅ Operational |
| 19 خدمة | ✅ |
| Monitoring (Grafana) | ✅ |

---

## 5. التوثيق

| البند | الحالة |
|-------|--------|
| MRF_MASTER_SOURCE_DOCUMENT | ✅ |
| MRF_OPERATIONAL_PLAN_UNIFIED | ✅ |
| MRF_FINAL_COMPLETE_DOCUMENT | ✅ (بعد التنفيذ) |
| README_AR محدّث | ✅ |
| ECOSYSTEM_API_README | ✅ |
| .env.example (Dify، Stripe) | ✅ |
| RUNBOOK | ✅ |

---

## 6. Ecosystem API (8005)

| البند | الحالة |
|-------|--------|
| integration/ecosystem-api | ✅ نسخ خارج SOURCE_CODE_EXTRACTED |
| Dockerfile | ✅ |
| docker-compose | ✅ مضاف |
| /health، /api/v1/health | ✅ |
| ملاحظة | إن كان 8005 مستخدماً، أوقف الخدمة القديمة ثم: docker compose up -d ecosystem_api |

---

## 7. Compliance Shield (Identity & Compliance Protocol — Kier)

**المرجع:** `docs/IDENTITY_COMPLIANCE_PROTOCOL_KIER.md`

| البند | الحالة | ملاحظات |
|-------|--------|---------|
| Proof of Residency (PoR) | 🔲 | فاتورة/كشف بنكي سعودي ≤3 أشهر |
| Source of Funds (SoF) | 🔲 | سرد + مستندات داعمة |
| Source of Wealth (SoW) | 🔲 | كيف تراكمت الثروة |
| AML Policy (1 صفحة) | 🔲 | لـ Stripe ومعالجات الدفع |
| Document Index | 🔲 | جدول محتويات موحد، أسماء وتواريخ متطابقة |
| Entity-First Onboarding | ✅ | التقديم كشركة UK أولاً |
| Provider Stack | 🔲 | Wise → Revolut → Stripe (بالترتيب) |

**التوجيه:** تقديم الكيان UK كطرف متعاقد؛ Kier كمدير/UBO عند الطلب فقط. تجنب حزم كبيرة — إرسال المستندات المطلوبة فقط.

---

## الإجراءات القادمة (ولد)

1. ~~إنشاء صفحات تسعير لـ Shadow Seven~~ ✅
2. ~~إعداد عرض xBio Sentinel ($299 + $19)~~ ✅
3. إعداد Demo لـ Boardroom
4. تفعيل Stripe (STRIPE_SECRET_KEY في .env)
5. استهداف 50 عميل Beta
6. **Compliance Shield:** إعداد SoF، PoR، SoW، AML Policy، Document Index
