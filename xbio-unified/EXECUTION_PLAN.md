# خطة تنفيذ X-BIO Unified — خطوة بخطوة

## المتطلبات المسبقة

- [ ] ESP32-S3 + BME680 (SDA=8, SCL=9, ADDR=GND → 0x76)
- [ ] PlatformIO أو Arduino IDE
- [ ] Python 3 مع pyserial, requests
- [ ] Postgres (للـ nexus_xbio)
- [ ] Docker (اختياري للنشر)

---

## الخطوة 1: إعداد Firmware WiFi

**الملف:** `NEXUS_PRIME_UNIFIED/xbio-unified/firmware/src/arduino_secrets.h`

```c
#define WIFI_SSID "اسم_الشبكة_الحقيقي"
#define WIFI_PASS "كلمة_المرور"
#define XBIO_INGEST_URL "https://xbio.mrf103.com/api/ingest"
```

**تنفيذ:**
1. افتح `arduino_secrets.h`
2. استبدل `YOUR_WIFI_SSID` و `YOUR_WIFI_PASSWORD`
3. احفظ الملف
4. أضف `src/arduino_secrets.h` إلى `.gitignore` إن لم يكن مضافاً

---

## الخطوة 2: بناء Firmware

**بناء شامل (موصى به):**
```bash
cd NEXUS_PRIME_UNIFIED/xbio-unified
chmod +x build_all.sh   # مرة واحدة فقط
./build_all.sh
```

**OMEGA (Serial فقط):**
```bash
cd NEXUS_PRIME_UNIFIED/xbio-unified/firmware
pio run -e esp32s3_omega
```

**OMEGA مع WiFi (للإنتاج):**
```bash
pio run -e esp32s3_omega_wifi
pio run -e esp32s3_omega_wifi -t upload
```

**First Breath (Signature X):**
```bash
pio run -e esp32s3_first_breath
pio run -e esp32s3_first_breath -t upload
```

**مراقبة Serial:**
```bash
# OMEGA: 921600
pio device monitor -b 921600

# First Breath: 115200
pio device monitor -b 115200
```

---

## الخطوة 3: التحقق من CORS

**الملف:** `products/xbio-sentinel/xbio_core.py`

النطاقات المسموحة: xbio.mrf103.com, dashboard.mrf103.com, publisher.mrf103.com, mrf103.com, localhost:5001, localhost:3000

---

## الخطوة 4: تشغيل Backend

**عبر Docker:**
```bash
cd NEXUS_PRIME_UNIFIED
docker compose up -d nexus_xbio
```

**محلياً:**
```bash
cd products/xbio-sentinel
export DATABASE_URL="postgresql://user:pass@localhost:5432/nexus_db"
uvicorn xbio_core:app --host 0.0.0.0 --port 8080
```

---

## الخطوة 5: تشغيل Serial Bridge V2 (Production)

**البنية:** Serial → HTTP `/api/ingest` و/أو MQTT `xbio/{device_id}/data` → Dashboard-ARC real-time.
**السجلات:** `logs/bridge.log` (RotatingFileHandler: 5MB×5 ملفات).

```bash
cd NEXUS_PRIME_UNIFIED/xbio-unified
pip install -r requirements.txt
python serial_bridge.py --port /dev/ttyUSB0 --url https://xbio.mrf103.com
```

**CLI V2:**
| الخيار | الوصف |
|--------|-------|
| `--port` | المنفذ التسلسلي (افتراضي: /dev/ttyUSB0) |
| `--mqtt` | نشر إلى MQTT فقط |
| `--mqtt-broker` | عنوان الـ broker (افتراضي: localhost:1883) |
| `--both` | HTTP + MQTT معاً |
| `-v` / `--verbose` | تسجيل تفصيلي |
| `--dry-run` | طباعة فقط، لا إرسال |

**MQTT (Real-time للـ Dashboard):**
```bash
python serial_bridge.py --port /dev/ttyUSB0 --mqtt --mqtt-broker localhost:1883
```

**HTTP + MQTT معاً:**
```bash
python serial_bridge.py --port /dev/ttyUSB0 --both
```

**First Breath (115200):**
```bash
python serial_bridge.py --port /dev/ttyUSB0 --baud 115200 --device-id XBIO_S3_01
```

**تجربة بدون إرسال:**
```bash
python serial_bridge.py --port /dev/ttyUSB0 --dry-run
```

---

## الخطوة 6: تشغيل Dashboard

```bash
cd NEXUS_PRIME_UNIFIED/dashboard-arc
npm install && npm run dev
```

**الوصول:** https://dashboard.mrf103.com أو http://localhost:5001

---

## الخطوة 7: اختبار التكامل

| # | الإجراء | النتيجة المتوقعة |
|---|---------|------------------|
| 1 | ESP32 OMEGA + Serial Monitor | JSON كل ~200ms |
| 2 | Serial Bridge يعمل | `[OK] VOID_STABLE truth=98.x` |
| 3 | `curl .../api/ingest` مع payload | `{"status":"ACK"}` |
| 4 | Dashboard مفتوح | بطاقات SRI, MSI, SPI, Truth Score |
| 5 | WiFi firmware + ESP32 | بيانات تظهر في Dashboard |

---

## استكشاف الأخطاء

**لا تظهر بيانات في Dashboard:** تحقق من nexus_xbio، DATABASE_URL، CORS.

**ESP32 لا يتصل بالـ WiFi:** راجع arduino_secrets.h.

**Serial Bridge لا يقرأ:** تحقق من المنفذ، السرعة (921600 أو 115200)، صلاحيات dialout.
