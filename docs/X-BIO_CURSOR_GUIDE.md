# THE CURSOR GUIDE — X-BIO Node S3 (Where & How)

**Hardware:** ESP32-S3 Dev Module N16R8 + BME688 + Waveshare AI Board + 6 wires  
**Project:** X-BIO Sentinel — Electric Nose (patent), VOC/env anomaly, edge-local biometric sensor

---

## الخطوة 1: تهيئة المشروع (Project Setup)

1. افتح فولدر جديد بـ Cursor وسمّه مثلاً **XBio_Node_S3**.
2. من الـ Extensions بـ Cursor، تأكد إنك منزل إضافة **PlatformIO IDE**.
3. افتح الـ PlatformIO (أيقونة النملة الفضائية عاليسار)، واكبس **New Project**.
4. اختار البورد: **ESP32-S3 Dev Module**، والـ Framework: **Arduino**، واكبس **Finish**.

---

## الخطوة 2: توجيه الـ AI (The Prompt Location)

1. بس يخلص إنشاء المشروع، افتح شات كيرسر (**Ctrl+L** أو **Cmd+L**).
2. اعمل Tag للـ **@Codebase** ليفهم الـ AI إنو عم يشتغل ببيئة C++/PlatformIO.
3. انسخ الـ **Master Prompt** اللي تحت، واعمله Paste بالشات واكبس **Enter**.

---

## الخطوة 3: التنفيذ (Execution)

- Cursor رح يكتبلك ملفين أساسيين:
  1. **`platformio.ini`** — تعريفات الـ USB CDC، مكتبات Bosch BME68x، I2C pins.
  2. **`src/main.cpp`** — كود العصب الشمي والفلترة والاتصال بـ NEXUS PRIME.
- بس تراجعهم، اكبس زر **Upload** (السهم اللي بالزاوية تحت) لينزل السوفتوير عالبورد.

---

## Master Prompt (انسخ والصق)

```
@Codebase

المهمة: بناء firmware لـ X-BIO Electric Nose — ESP32-S3 Dev Module N16R8 + BME688 + Waveshare AI Board (6 wires).

السياق:
- المشروع: NEXUS PRIME / X-BIO Sentinel
- الهاردوير: ESP32-S3 N16R8، BME688 (I2C)، Waveshare AI Board
- التوصيل: 6 أسلاك — VCC, GND, SDA (GPIO 8), SCL (GPIO 9)، واختياري INT + ADDR
- عنوان I2C للـ BME688: 0x76 أو 0x77 (حسب ADDR pin)

المتطلبات:
1. platformio.ini:
   - Board: esp32-s3-devkitc-1 (أو esp32-s3-devkitc-1-n16r8)
   - Framework: Arduino
   - USB CDC: ARDUINO_USB_CDC_ON_BOOT=1
   - I2C: SDA=8, SCL=9 (Waveshare default)
   - مكتبات: BSEC/BME68x (Bosch)، NimBLE، ArduinoJson، PubSubClient، WiFiManager
   - Flash: 16MB، PSRAM: 8MB

2. src/main.cpp:
   - تهيئة I2C على GPIO 8 (SDA)، GPIO 9 (SCL)
   - تهيئة BME688 وقراءة: temperature, humidity, pressure, gas_resistance, iaq_score, voc_equivalent
   - إرسال القراءات عبر BLE (NimBLE) أو WiFi/HTTP إلى NEXUS PRIME API
   - فلترة أولية للقيم الشاذة
   - Serial output للـ debug (115200 baud)
   - دعم OTA إن أمكن

3. البنية:
   - setup(): Wire.begin(SDA, SCL), BME688 init, BLE advertise
   - loop(): قراءة BME688 كل 1–2 ثانية، إرسال عبر BLE أو HTTP
   - JSON format للبيانات: {"device_id":"XBIO-xxx","temp":24.5,"humidity":45,"pressure":1013,"gas":150000,"iaq":92,"voc":0.42,"ts":...}

المراجع (إن وُجدت في المشروع):
- docs/X-BIO_ESP32_WIRING_AND_CLEAN_START.md
- docs/X-BIO_ESP32_MAIN_CORE_HANDSHAKE_PROMPT.md
- dashboard-arc/firmware/esp32-xbio/

القيود:
- لا تستخدم SPI للـ BME688 إلا إذا الهاردوير يتطلب ذلك — الافتراضي I2C
- التكامل مع NEXUS PRIME: xbio.mrf103.com، dashboard.mrf103.com/xbio
- البيانات غير قابلة للحذف (immutable) — append only

المخرجات المتوقعة:
1. platformio.ini كامل
2. src/main.cpp يعمل مع BME688 و BLE
3. تعليمات التوصيل (wiring) في تعليقات
```

---

## الخطوة 4: التوصيل (Wiring)

| BME688 | ESP32-S3 (Waveshare N16R8) | لون مقترح |
|--------|---------------------------|-----------|
| VCC    | 3.3V                      | أحمر      |
| GND    | GND                       | أسود      |
| SDA    | GPIO 8                    | أزرق      |
| SCL    | GPIO 9                    | أصفر      |
| ADDR   | GND (0x76) أو 3.3V (0x77) | —         |
| INT    | (اختياري) GPIO            | —         |

**ملاحظة:** إن لوحتك تستخدم GPIO 21/22 للـ I2C، غيّر في `platformio.ini` أو `main.cpp`.

---

## الخطوة 5: التنظيف والفلاش (Clean & Flash)

إذا البورد فيه chunks أو أخطاء سابقة:

```bash
cd XBio_Node_S3
pio run -t erase    # مسح الـ flash
pio run -t upload   # رفع السوفتوير
pio device monitor -b 115200   # مراقبة الـ Serial
```

---

## المراجع

| الملف | الاستخدام |
|-------|-----------|
| [xbio-unified/](../xbio-unified/) | المجلد الموحد — OMEGA + First Breath + Serial Bridge |
| [X-BIO_ESP32_WIRING_AND_CLEAN_START.md](X-BIO_ESP32_WIRING_AND_CLEAN_START.md) | التوصيل، التنظيف، الـ DevOps flow |
| [X-BIO_ESP32_MAIN_CORE_HANDSHAKE_PROMPT.md](X-BIO_ESP32_MAIN_CORE_HANDSHAKE_PROMPT.md) | إرساله لمطور الـ Main Core للحصول على API و DB |
| [dashboard-arc/firmware/esp32-xbio/](../dashboard-arc/firmware/esp32-xbio/) | مشروع PlatformIO جاهز (MQTT/BLE) في NEXUS PRIME |

---

*X-BIO Sentinel — Electric Nose، VOC، 19 خوارزمية، edge-local، مسار هرمونات/فيرومونات.*
