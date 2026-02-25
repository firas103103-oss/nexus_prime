# X-BIO ESP32-S3 + BME688 — Wiring & Clean Start Guide

**Hardware:** ESP32-S3 Dev Module N16R8 + BME688 + Waveshare AI Board + 6 wires

---

## 1. Wiring: BME688 ↔ ESP32-S3 (6 Wires)

### Standard I2C (4 wires)
| BME688 | ESP32-S3 (Waveshare N16R8) | Notes |
|--------|----------------------------|-------|
| VCC    | 3.3V                       | 1.71–3.6V range |
| GND    | GND                        | Common ground |
| SDA    | **GPIO 8** or GPIO 21      | Data — check board pinout |
| SCL    | **GPIO 9** or GPIO 22      | Clock — 400 kHz Fast Mode |

### If 6 Wires (Extended)
- **Option A:** I2C (4) + **INT** (interrupt) + **ADDR** (address select 0x76/0x77)
- **Option B:** SPI — MOSI, MISO, SCK, CS, VCC, GND

**Waveshare ESP32-S3-DEV-KIT-NxR8:**  
Default I2C is often **GPIO 8 (SDA)**, **GPIO 9 (SCL)**. Verify from [Waveshare docs](https://www.waveshare.com/wiki/ESP32-S3-DEV-KIT-N16R8) or board silkscreen.

**Current firmware** (`planets/X-BIO/xbio_projects/xbio_firmware/src/main.cpp`):
```cpp
#define I2C_SDA 21
#define I2C_SCL 22
```
→ If your board uses 8/9, change these.

### BME688 I2C Address
- **0x76** — ADDR pin to GND  
- **0x77** — ADDR pin to VCC (default in `bme688_sensor.h`)

---

## 2. ESP32 Clean / Format (Assume Chunks, Errors)

### A. Erase Flash (Full Reset)
```bash
cd planets/X-BIO/xbio_projects/xbio_firmware
pio run -t erase
# or
esptool.py --port /dev/ttyUSB0 erase_flash
```

### B. Partition Table
`partitions.csv` already set for 16MB Flash, 8MB PSRAM. No change needed unless custom layout.

### C. First Boot After Erase
1. Flash firmware: `pio run -t upload`
2. Open monitor: `pio device monitor -b 115200`
3. Expect: LittleFS mount, I2C init, BLE advertise
4. BME688: If `bme688_sensor` is disabled (`#include` commented), you'll see I2C init only — enable after adding BSEC2 lib

---

## 3. PlatformIO Setup

### platformio.ini (Current)
```ini
[env:esp32s3]
platform = espressif32
board = esp32-s3-devkitc-1   # May need esp32-s3-devkitc-1-n16r8
framework = arduino
board_upload.flash_size = 16MB
board_build.partitions = partitions.csv
monitor_speed = 115200

lib_deps =
  lorol/LittleFS_esp32 @ ^1.0.6
  h2zero/NimBLE-Arduino @ ^1.4.2
  bblanchon/ArduinoJson @ ^6.21.3
  # Add after Bosch signup:
  # boschsensortec/BSEC2 Software Library
  # boschsensortec/BME68x Sensor library
```

### BSEC2 (BME688 Gas/IAQ)
1. Register at [Bosch Sensortec Developer](https://www.bosch-sensortec.com/software-tools/software/bsec/)
2. Download BSEC2 + BME68x Arduino library
3. Add to `lib/` or PlatformIO lib_deps
4. Uncomment `#include "bme688_sensor.h"` in `main.cpp`

---

## 4. Interface Decision

| Mode | Pros | Cons |
|------|------|------|
| **BLE → APK → HTTP** | No WiFi on ESP32, battery-friendly, APK already exists | APK must be running for sync |
| **ESP32 WiFi → HTTP** | Direct to server, no phone needed | More power, WiFi config on device |
| **ESP32 WiFi → MQTT** | Lightweight, good for many sensors | Need MQTT broker in NEXUS PRIME |
| **Hybrid** | BLE for config/control, WiFi for bulk upload | More complex |

**Recommendation for MVP:** BLE → APK → HTTP. APK receives BLE stream, batches readings, POSTs to `api.mrf103.com/xbio/telemetry` (or equivalent).

---

## 5. Fullstack DevOps Flow

```
┌─────────────┐     I2C      ┌─────────────┐     BLE      ┌─────────────┐
│   BME688    │ ──────────►  │  ESP32-S3   │ ──────────►  │  Android    │
│   (VOC etc) │              │  Firmware   │              │  APK        │
└─────────────┘              └─────────────┘              └──────┬──────┘
                                    │                            │
                                    │ (optional WiFi)            │ HTTP
                                    │                            ▼
                                    │                    ┌─────────────┐
                                    └───────────────────►│  NEXUS API  │
                                                         │  (8005)     │
                                                         └──────┬──────┘
                                                                │
                                    ┌───────────────────────────┼───────────────────────────┐
                                    ▼                           ▼                           ▼
                            ┌───────────────┐         ┌───────────────┐         ┌───────────────┐
                            │  nexus_db     │         │  nexus_xbio    │         │  Dify         │
                            │  sensor_      │         │  algorithms   │         │  webhook      │
                            │  readings     │         │  PAD, EFII…   │         │  (anomaly)    │
                            └───────────────┘         └───────────────┘         └───────────────┘
```

---

## 6. Files to Modify

| File | Change |
|------|--------|
| `main.cpp` | I2C_SDA, I2C_SCL if board differs; uncomment bme688_sensor |
| `platformio.ini` | Add BSEC2 lib; board = esp32-s3-devkitc-1-n16r8 if needed |
| `bme688_sensor.h/cpp` | I2C addr 0x76/0x77; BSEC config binary path |
| `session_sync.cpp` | Add HTTP POST to NEXUS API (if ESP32 has WiFi) |
| `mobile-app` | Add Retrofit/OkHttp POST to `api.mrf103.com` after BLE receive |
| `products/xbio-sentinel` | Add `/xbio/telemetry` endpoint if not exists |

---

## 7. References

- [NEXUS PRIME Technical Doc](NEXUS_PRIME_TECHNICAL_DOCUMENTATION_AR.md) — ports, services
- [Main Core Handshake Prompt](X-BIO_ESP32_MAIN_CORE_HANDSHAKE_PROMPT.md) — send to backend dev
- [BME688 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme688-ds000.pdf)
- [Waveshare ESP32-S3 N16R8](https://www.waveshare.com/wiki/ESP32-S3-DEV-KIT-N16R8) — pinout
