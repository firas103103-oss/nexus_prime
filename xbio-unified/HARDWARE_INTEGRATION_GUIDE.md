# X-BIO Hardware Integration Guide — ESP32-S3 + BME680/BME688

## Task 1: Hardware Mapping & Wiring

### I2C Pins (from firmware)

| Source | SDA | SCL | Address |
|--------|-----|-----|---------|
| `main_first_breath.cpp` | GPIO 8 | GPIO 9 | 0x76 |
| `main.cpp` (OMEGA) | GPIO 8 | GPIO 9 | 0x76 |

### Wiring Table — ESP32-S3 ↔ BME680/BME688 (Waveshare)

| BME680/BME688 Pin | ESP32-S3 Pin | Notes |
|-------------------|--------------|-------|
| VCC | 3.3V | **Do not use 5V** |
| GND | GND | Common ground |
| SDA | GPIO 8 | I2C Data |
| SCL | GPIO 9 | I2C Clock |
| SDO / ADDR | GND | 0x76 address (tie to GND) |
| SDO / ADDR | 3.3V | 0x77 address (if needed) |

**6-Wire Setup (recommended):** VCC, GND, SDA, SCL, SDO→GND, (optional CS if SPI).

### Address Selection

- **SDO = GND** → I2C address **0x76** (default in firmware)
- **SDO = VCC** → I2C address **0x77**

### Lazarus Pin (OMEGA only)

- **GPIO 12** — Physical reset/rebirth. Connect to MOSFET gate or leave floating for First Breath.

---

## Task 2: Flashing the Firmware

### Step 1: Verify Serial Port

```bash
# List serial devices
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

# Or use PlatformIO
cd /root/NEXUS_PRIME_UNIFIED/xbio-unified/firmware
export PATH="$HOME/.local/bin:$PATH"
pio device list
```

**Expected:** `/dev/ttyUSB0` or `/dev/ttyACM0` when ESP32-S3 is connected via USB.

### Step 2: Build & Flash First Breath

```bash
cd /root/NEXUS_PRIME_UNIFIED/xbio-unified/firmware
export PATH="$HOME/.local/bin:$PATH"

# Build
pio run -e esp32s3_first_breath

# Flash (replace /dev/ttyUSB0 with your port if different)
pio run -e esp32s3_first_breath -t upload
```

**Or use the unified script:**

```bash
cd /root/NEXUS_PRIME_UNIFIED/xbio-unified
./build_all.sh
pio run -e esp32s3_first_breath -t upload
```

### Step 3: Monitor Serial Output

```bash
cd /root/NEXUS_PRIME_UNIFIED/xbio-unified/firmware
pio device monitor -b 115200 -e esp32s3_first_breath
```

**Expected JSON (every 2s):**
```json
{"node_id":"XBIO_S3_01","temp":24.5,"gas":150000,"anomaly":false}
```

---

## Task 3: End-to-End Integration Test

### Prerequisites

1. **nexus_broker** (Mosquitto) running: `docker compose up -d nexus_broker`
2. **nexus_dashboard** running (for WebSocket): `docker compose up -d nexus_dashboard`
3. ESP32-S3 flashed and connected

### Run Serial Bridge V2

```bash
cd /root/NEXUS_PRIME_UNIFIED/xbio-unified
pip install -r requirements.txt
python serial_bridge.py --port /dev/ttyUSB0 --both --verbose -v
```

**Flags:**
- `--both` — HTTP POST to `/api/ingest` + MQTT publish to `xbio/{device_id}/data`
- `-v` / `--verbose` — Detailed logging

### Verify Logs

```bash
tail -f /root/NEXUS_PRIME_UNIFIED/xbio-unified/logs/bridge.log
```

---

## Task 4: Dashboard Verification

1. Open **https://dashboard.mrf103.com** (or http://localhost:5001)
2. Navigate to **XBioSentinel** module
3. **Real-time WS:** Look for "Real-time WS" badge when WebSocket is connected
4. **Data:** OMEGA (SRI, MSI, SPI, Truth) or First Breath (temp, gas, anomaly) should update in real time

### Troubleshooting

| Issue | Check |
|-------|-------|
| No serial device | `ls /dev/tty*` — add user to `dialout`: `sudo usermod -aG dialout $USER` |
| BME not found | Wiring (SDA=8, SCL=9, SDO=GND for 0x76) |
| MQTT not received | `docker ps` — nexus_broker on 1883, nexus_dashboard running |
| Dashboard no data | WebSocket port 8081 exposed; IoTService initialized |
