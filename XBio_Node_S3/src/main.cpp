/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * X-BIO Sentinel — The First Breath (Phase 1)
 * ESP32-S3 N16R8 + BME688 | Signature X (Spike Detection)
 * NEXUS PRIME
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Wiring: SDA=8, SCL=9, ADDR=GND → I2C 0x76
 */

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
#include <ArduinoJson.h>

#define SDA_PIN 8
#define SCL_PIN 9
#define BME_ADDR 0x76
#define LOOP_INTERVAL_MS 2000
#define BASELINE_READINGS 10
#define ANOMALY_THRESHOLD 0.15f  // 15% gas drop = anomaly

Adafruit_BME680 bme;
const char* NODE_ID = "XBIO_S3_01";

// Signature X: 10-reading rolling baseline
uint32_t gasBaseline[BASELINE_READINGS];
uint8_t baselineIdx = 0;
uint8_t baselineCount = 0;
float baselineMean = 0.0f;

void updateBaseline(uint32_t gas) {
  gasBaseline[baselineIdx] = gas;
  baselineIdx = (baselineIdx + 1) % BASELINE_READINGS;
  if (baselineCount < BASELINE_READINGS) baselineCount++;

  float sum = 0;
  for (uint8_t i = 0; i < baselineCount; i++) sum += gasBaseline[i];
  baselineMean = sum / baselineCount;
}

bool isAnomaly(uint32_t gas) {
  if (baselineCount < BASELINE_READINGS) return false;
  if (baselineMean <= 0) return false;
  float drop = (baselineMean - (float)gas) / baselineMean;
  return drop > ANOMALY_THRESHOLD;
}

void setup() {
  Serial.begin(115200);
  delay(1500);

  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(400000);

  if (!bme.begin(BME_ADDR)) {
    Serial.println("{\"error\":\"BME688 not found at 0x76\"}");
    for (;;) delay(1000);
  }

  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);

  Serial.println("{\"node_id\":\"XBIO_S3_01\",\"status\":\"ready\"}");
}

void loop() {
  if (!bme.performReading()) {
    Serial.println("{\"error\":\"read_fail\"}");
    delay(LOOP_INTERVAL_MS);
    return;
  }

  float temp = bme.temperature;
  uint32_t gas = bme.gas_resistance;

  updateBaseline(gas);
  bool anomaly = isAnomaly(gas);

  JsonDocument doc;
  doc["node_id"] = NODE_ID;
  doc["temp"] = roundf(temp * 10.0f) / 10.0f;
  doc["gas"] = (long)gas;
  doc["anomaly"] = anomaly;

  serializeJson(doc, Serial);
  Serial.println();

  delay(LOOP_INTERVAL_MS);
}
