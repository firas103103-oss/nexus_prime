# PATENT_ARCHITECTURE: X-BIO Sentinel Ecosystem

## 1. Abstract (الملخص الابتكاري)

نظام سيادي (Sovereign) لمراقبة المؤشرات الحيوية والبيئية يعتمد على معالجة هجينة (Edge-AI) وتشفير بيانات لا مركزي، مع قدرة "التنفس الأول" (First Breath) للتعرف التلقائي على العقد. يجمع النظام بين 19 خوارزمية براءات اختراع، وحدات استشعار BME688/BME680، وبروتوكول MQTT موحد، وواجهة ARC التفاعلية.

---

## 2. System Components (المكونات السيادية)

| المكون | الوصف | الموقع التقني |
|--------|-------|---------------|
| **OMEGA Core (V2.1)** | وحدة المعالجة المركزية لاتخاذ القرار — SRI, MSI, SPI, Truth Score | `firmware/src/main.cpp` |
| **Sentinel Nodes** | وحدات الاستشعار الموزعة (First Breath Protocol) | `firmware/src/main_first_breath.cpp` |
| **Unified Bridge** | طبقة الربط البروتوكولي لتحويل السيريال إلى تدفق بيانات ذكي (HTTP + MQTT) | `serial_bridge.py` |
| **ARC Interface** | واجهة القيادة والتحكم التفاعلية — Real-time WebSocket | `dashboard-arc/client/src/pages/XBioSentinel.tsx` |
| **19 Patent Algorithms** | PAD-02, EFII-22, BMEI, CVP-04, QTL-08, DSS-99, FDIP-11, إلخ | `products/xbio-sentinel/xbio_algorithms.py` |

---

## 3. Claim 1: Autonomous Node Discovery (First Breath)

**الابتكار:** قدرة النظام على تعريف نفسه وتخصيص هوية (Unique Node ID) بمجرد التشغيل الأول دون تدخل بشري، مع ربطها بالـ Sovereign Node.

**التنفيذ:**
- First Breath firmware يرسل `node_id` تلقائياً مع أول قراءة (temp, gas, anomaly)
- Serial Bridge يقرأ الهوية ويوجه البيانات إلى `xbio/{node_id}/data`
- IoT Service يسجل الجهاز تلقائياً عند أول اتصال (Auto-register)

**المرجع:** `firmware/src/main_first_breath.cpp`, `serial_bridge.py` (First Breath format)

---

## 4. Claim 2: Unified Telemetry Ingestion

**الابتكار:** بروتوكول موحد قادر على تفسير بيانات متباينة (Multi-modal) وتحويلها إلى Payload موحد يدعم الـ AI Diagnostic Engines.

**الصيغ المدعومة:**
- **OMEGA:** `v`, `s`, `sri`, `msi`, `spi`, `truth`, `alert`
- **First Breath:** `node_id`, `temp`, `gas`, `anomaly`
- **Standard Ingest:** `device_id`, `temp`, `humidity`, `pressure`, `gas`, `iaq`, `voc`

**التدفق:** Serial → Bridge → MQTT `xbio/{id}/data` + HTTP `/api/ingest` → IoT Service → WebSocket → Dashboard

**المرجع:** `serial_bridge.py` (`build_ingest_payload`, `to_mqtt_payload`), `iot_service.ts`

---

## 5. Patent Family 2 — Predictive Sensoring

الخوارزميات الأساسية مُوثقة في:
- [PATENT_02_Predictive_Sensoring.md](../docs/Science_and_RnD/PATENT_02_Predictive_Sensoring.md)
- [xbio_algorithms.py](../../products/xbio-sentinel/xbio_algorithms.py)

| الخوارزمية | الوظيفة |
|------------|---------|
| PAD-02 | تنبؤ تسرب كيميائي/حريق 5–10 ثوانٍ قبل العتبة |
| EFII-22 | كشف الشذوذ عبر اضطراب الهواء والانخفاض الحراري |
| BMEI | دمج ضغط/حرارة/غاز لمؤشر صدمة بيئية |
| CVP-04 | إجماع عقد متعددة لمنع الإيجابيات الكاذبة |
| QTL-08 | توقيع زمني مشفر لمكافحة التزوير |
| DSS-99 | مزامنة زمنية لغاز + صوت |

---

## 6. Backend Reference

- **API:** `products/xbio-sentinel/` — FastAPI على المنفذ 8080
- **Endpoints:** `/api/ingest`, `/api/telemetry/latest`, `/api/patents`, `/health`
- **راجع:** [backend/REFERENCE.md](backend/REFERENCE.md)
