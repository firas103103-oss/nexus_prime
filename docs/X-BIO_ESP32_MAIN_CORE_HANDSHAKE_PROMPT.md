# X-BIO Electric Nose — Prompt/Script for Main Core Developer

**Purpose:** Send this to the main core developer to get all infrastructure info needed to start ESP32-S3 + BME688 + Waveshare AI Board development, database sync, AI core integration, and APK build.

**Hardware:** ESP32-S3 Dev Module N16R8 + BME688 + Waveshare AI Board + 6 wires  
**Project:** X-BIO Sentinel — Electric Nose (patent), VOC/env anomaly, 19 algorithms, edge-local biometric sensor

---

## 1. What We Need From You (Main Core Dev)

Please reply with the following so we can start clean:

### A. Database & Sync
1. **PostgreSQL schema** for X-BIO sensor data:
   - Table names (e.g. `sensor_readings`, `sensor_data_stream`, `xbio_telemetry`)
   - Column definitions: `device_id`, `temperature`, `humidity`, `pressure`, `gas_resistance`, `iaq_score`, `voc_equivalent`, `timestamp`, etc.
   - Any RLS policies, indexes, or API keys for insert
2. **Insert endpoint** or direct DB connection:
   - REST API URL (e.g. `https://api.mrf103.com/xbio/telemetry` or `nexus_xbio`)
   - Auth: API key, JWT, or service role
   - JSON payload format expected
3. **Supabase** (if used): URL, anon key, service role, table names for `missions`, `sensor_data`, etc.

### B. X-BIO Core API (nexus_xbio:8080)
1. **Endpoints** we must call from ESP32 or gateway:
   - `POST /api/algorithms/pad` — gas_readings, sample_interval_sec
   - `POST /api/algorithms/efii` — turbulence, thermal_drop
   - `POST /api/algorithms/bmei` — pressure, temp, gas
   - `POST /api/defense/evaluate` — threat_level, sei_cleared
   - Any **webhook** for real-time push from ESP32?
2. **Webhook secret** (`XBIO_WEBHOOK_SECRET`) for Dify/sovereign_dify_bridge integration
3. **CORS** — is `nerve.mrf103.com` or `xbio.mrf103.com` allowed for cross-origin from mobile APK?

### C. AI Core & Nerve
1. **Nerve API** (`nexus_nerve:8200`):
   - `GET /api/consciousness` — Soul Monitor (mood, soul_tier)
   - `GET /api/innovation/score` — Innovation Index
   - Any endpoint for X-BIO telemetry injection?
2. **Dify workflow** triggered by X-BIO anomaly — workflow ID, input schema
3. **action_ledger** — how does X-BIO log actions? Table, API, format

### D. Network & Deployment
1. **ESP32 connectivity:**
   - WiFi SSID/password for local server (or config via BLE?)
   - Does ESP32 talk to server directly (HTTP/MQTT) or only via BLE → APK → server?
2. **MQTT** (if used): broker URL, topic for `xbio/telemetry`, credentials
3. **Docker network:** `nexus_network` — can a gateway service receive ESP32 data and forward to nexus_xbio?

### E. Existing Schemas (Reference)
We found these in the codebase — please confirm or correct:

```sql
-- biosentinel_database_schema.sql (dashboard-arc)
CREATE TABLE sensor_readings (
  id UUID PRIMARY KEY,
  device_id VARCHAR(64),
  temperature REAL, humidity REAL, pressure REAL, gas_resistance REAL,
  iaq_score INTEGER, iaq_accuracy INTEGER, voc_equivalent REAL,
  created_at TIMESTAMPTZ
);

-- supabase_arc_v2_schema.sql
CREATE TABLE sensor_data_stream (
  device_id, timestamp, temperature, humidity, pressure,
  gas_resistance, iaq_score, voc_equivalent, ...
);
```

---

## 2. Hardware Wiring (ESP32-S3 N16R8 + BME688 + 6 Wires)

### Option A: I2C (4 wires — standard)
| BME688 Pin | ESP32-S3 Pin (Waveshare) | Wire Color (suggested) |
|------------|--------------------------|------------------------|
| VCC        | 3.3V                     | Red                    |
| GND        | GND                      | Black                  |
| SDA        | GPIO 8 or 21*            | Blue                   |
| SCL        | GPIO 9 or 22*            | Yellow                 |

*Current firmware uses SDA=21, SCL=22. Waveshare ESP32-S3-DEV-KIT-NxR8 may use different default I2C — confirm from board pinout.*

### Option B: 6 Wires (if SPI or extra pins)
If using SPI: add MOSI, MISO, CS, SCK. Or if 6 wires = I2C + INT + ADDR select.

**BME688 I2C address:** 0x76 or 0x77 (configurable via ADDR pin)

**Please confirm:**
- Exact GPIO for SDA, SCL on your Waveshare board
- Whether BME688 is 0x76 or 0x77
- Pull-up resistors: BME688 has internal pull-ups; external 4.7kΩ on SDA/SCL if long cables

---

## 3. Software Stack & Tools

### Recommended
| Tool | Purpose |
|------|---------|
| **PlatformIO** (VS Code) | ESP32 firmware — already in `planets/X-BIO/xbio_projects/xbio_firmware` and `products/xbio-sentinel/firmware` |
| **Arduino framework** | ESP32-S3 support |
| **BSEC2** (Bosch) | BME688 gas/IAQ/VOC — requires Bosch developer account, add lib manually |
| **NimBLE** | BLE for APK sync — already in firmware |
| **LittleFS** | Config, BSEC state — already in firmware |
| **Android Studio** | APK — `products/xbio-sentinel/mobile-app` (Kotlin, BLE, MVVM) |

### ESP32 Clean/Format (Assume Corrupted)
1. **Erase flash:** `pio run -t erase` or `esptool.py erase_flash`
2. **Partition:** Use `partitions.csv` (16MB flash, 8MB PSRAM)
3. **First boot:** Init LittleFS, load BSEC config from SPIFFS/LittleFS, calibrate

---

## 4. Firmware Locations (Existing)

| Path | Description |
|------|-------------|
| `planets/X-BIO/xbio_projects/xbio_firmware/` | PlatformIO project — BME688, BLE, session_sync, state_machine |
| `products/xbio-sentinel/firmware/` | May be duplicate or canonical — confirm |
| `products/xbio-sentinel/` | xbio_core.py (FastAPI 8080), xbio_algorithms.py (19 patents) |

**Current firmware status:**
- `bme688_sensor.h` uses BSEC2 — lib commented out in platformio.ini (add manually)
- BLE service for session sync (chunks 180 bytes)
- State machine: IDLE → LOAD_CONFIG_A → MEASURE_A → ... → READY_FOR_SYNC
- I2C: SDA=21, SCL=22 — **verify for Waveshare N16R8**

---

## 5. Data Flow (Target Architecture)

```
[BME688] ──I2C──> [ESP32-S3] ──BLE──> [Android APK] ──HTTP──> [api.mrf103.com / nexus_xbio]
    │                    │                    │                        │
    │                    │                    │                        ├──> PostgreSQL (sensor_readings)
    │                    │                    │                        ├──> xbio_algorithms (PAD, EFII, BMEI...)
    │                    │                    │                        └──> Dify webhook (anomaly)
    │                    │                    │
    │                    └──[WiFi?]───────────┴──> Direct to server (if ESP32 has WiFi)
```

**Alternative:** ESP32 → WiFi → MQTT/HTTP → server (no APK for data path, APK only for control/monitoring)

---

## 6. APK (Existing)

- **Path:** `products/xbio-sentinel/mobile-app/`
- **Stack:** Kotlin, MVVM, BLE (Nordic UART UUIDs)
- **Features:** Scan BLE, connect, stream sensor data, charts (MPAndroidChart)
- **Gap:** Needs to POST to NEXUS PRIME API for DB sync (not just display)
- **Build:** `./gradlew assembleDebug` → `app/build/outputs/apk/debug/app-debug.apk`

---

## 7. 19 Algorithms (Already Implemented in xbio_algorithms.py)

| Code | Name | Input | Use |
|------|------|-------|-----|
| PAD-02 | Predictive Anomaly Dilation | gas_readings | Fire/leak 5–10s prediction |
| EFII-22 | Ethereal Field Instability | turbulence, thermal_drop | Chaos + cold correlation |
| BMEI | Bio-Metric Environmental Index | pressure, temp, gas | Trauma detection |
| CVP-04 | Cross-Verification Protocol | node_readings | Multi-sensor consensus |
| FDIP-11 | Final Defense Initiation | threat_level, sei_cleared | Kinetic Silo, Silent Wave |
| RATP-14 | Resonance Augmentation | base_freq, room_resonance | Acoustic |
| SEI-10 | Security/Integrity Check | aggression | Pass/fail |
| DSS-99 | Dynamic Sensor Sync | gas_ts, audio_ts | Timestamp alignment |
| QTL-08 | Quantum-Temporal Lock | value, sensor_id | Anti-spoofing hash |

---

## 8. Quick Start Checklist (After Main Core Replies)

- [ ] Confirm wiring (SDA, SCL, VCC, GND)
- [ ] Add BSEC2 lib to platformio.ini (Bosch)
- [ ] Erase ESP32, flash clean firmware
- [ ] Test BME688 I2C scan (0x76 or 0x77)
- [ ] Test BLE with existing APK
- [ ] Implement HTTP/MQTT push from ESP32 or APK to nexus_xbio/API
- [ ] Verify sensor_readings insert
- [ ] Wire PAD/EFII/BMEI from telemetry to xbio_algorithms
- [ ] Add Dify webhook on anomaly
- [ ] Build release APK with NEXUS PRIME branding

---

## 9. Copy-Paste Prompt (Send to Main Core Dev)

```
I'm starting X-BIO Electric Nose development: ESP32-S3 N16R8 + BME688 + Waveshare AI Board.

I need from you (main core / NEXUS PRIME backend):

1. PostgreSQL schema for X-BIO sensor telemetry (table names, columns, RLS). 
   Or REST API endpoint + auth + JSON format for inserting sensor_readings.

2. nexus_xbio (8080) — which endpoints should ESP32/gateway call? 
   Webhook URL for anomaly → Dify? XBIO_WEBHOOK_SECRET?

3. Nerve API — any endpoint for X-BIO mood/innovation injection?

4. Network: Does ESP32 talk to server via WiFi (HTTP/MQTT) or only BLE→APK→HTTP?
   If WiFi: broker/API URL, credentials.

5. Confirm or correct: sensor_readings (device_id, temp, humidity, pressure, gas_resistance, iaq_score, voc, created_at).

6. Waveshare ESP32-S3 N16R8 — default I2C pins for BME688 (SDA/SCL)? 
   Our firmware uses 21/22 — is that correct for this board?

Reply with the above and I'll start clean firmware + APK sync.
```

---

*Generated for NEXUS PRIME X-BIO MVP — Electric Nose, VOC, 19 algorithms, edge-local, hormones/pheromones roadmap.*
