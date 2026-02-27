# X-BIO Unified — حزمة موحدة

مجمع X-BIO: Firmware OMEGA، Serial Bridge، وثائق، وإعدادات. كل الملفات المطلوبة في مكان واحد.

## المحتويات

```
xbio-unified/
├── README.md                 # هذا الملف
├── EXECUTION_PLAN.md         # خطة تنفيذ خطوة بخطوة
├── PATHS.md                  # مسارات الملفات في المشروع
├── requirements.txt          # pyserial, requests, paho-mqtt
├── firmware/                 # Firmware OMEGA + First Breath
│   ├── src/
│   │   ├── main.cpp          # OMEGA V2.1 (Dual-Core)
│   │   ├── main_first_breath.cpp  # First Breath (Signature X)
│   │   └── arduino_secrets.h # عدّل قبل البناء للإنتاج
│   ├── platformio.ini
│   └── partitions.csv
├── serial_bridge.py          # V2: Serial → HTTP + MQTT, Rotating Logs
├── logs/                     # bridge.log (5MB×5 rotating)
├── config/
│   └── CORS_ORIGINS.md       # قائمة النطاقات المسموحة
└── backend/
    └── REFERENCE.md          # إشارة إلى products/xbio-sentinel
```

**Backend:** في `products/xbio-sentinel/`. راجع `backend/REFERENCE.md`.

**PlatformIO:** راجع `PLATFORMIO_SETUP.md` لإعداد محلي وسحابي.

**Patent Architecture:** راجع `PATENT_ARCHITECTURE.md` للهيكلية الابتكارية والبراءات.

**Hardware Integration:** راجع `HARDWARE_INTEGRATION_GUIDE.md` للتوصيل والفلاش والاختبار.

## البدء السريع

1. **Firmware OMEGA:** عدّل `firmware/src/arduino_secrets.h` ثم `cd firmware && pio run -e esp32s3_omega_wifi`
2. **Firmware First Breath:** `cd firmware && pio run -e esp32s3_first_breath`
3. **Backend:** شغّل nexus_xbio عبر Docker أو `uvicorn xbio_core:app --port 8080`
4. **Dashboard:** XBioSentinel.tsx يجلب من `/api/telemetry/latest`
5. **Serial Bridge V2:** `pip install -r requirements.txt && python serial_bridge.py --port /dev/ttyUSB0`
   - `--mqtt` — نشر إلى MQTT (nexus_broker) للـ Dashboard real-time
   - `--both` — HTTP + MQTT معاً
   - `-v` — تسجيل تفصيلي
   - السجلات: `logs/bridge.log` (5MB×5 rotating)
