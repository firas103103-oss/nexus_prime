/**
 * @file main.cpp
 * @project X-BIO OMEGA SENTINEL (ABDALA MRF)
 * @version 2.1 (FIXED, SYNCHRONIZED & HARDENED)
 * @level SOVEREIGN_GOD_LEVEL - ADM_GOD_MODE
 * @logic DUAL-CORE NEURAL FUSION WITH MUTEX PROTECTION
 * @source xbio-unified
 */

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#ifdef OMEGA_WIFI
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#endif

// --- Hardware Overclocking & Mapping ---
#define I2C_SDA 8
#define I2C_SCL 9
#define LAZARUS_PIN 12      // Hardware Rebirth (Connect to MOSFET/Reset)
#define TELEMETRY_BAUD 921600

Adafruit_BME680 bme;
SemaphoreHandle_t bmeMutex;

// --- The God Mode Structures ---
struct SovereignWitness {
    float msi;
    float spi;
    float sri;
    float truthScore;
    String state;
    bool isAnomaly;
} oracle;

// --- Global Assets ---
float rollingBaseline = 0;
float resonanceBuffer[20] = {0};
int resonanceIdx = 0;
const float OMEGA_ALPHA = 0.04;

TaskHandle_t SensingTask;
TaskHandle_t AnalyticsTask;

#ifdef OMEGA_WIFI
#include "arduino_secrets.h"
#define DEVICE_ID "OMEGA_S3_01"
#endif

// --- System Fail-Safes ---
void lazarusRebirth() {
    Serial.println(">>> [CRITICAL] PHYSICAL LAZARUS REBIRTH TRIGGERED...");
    digitalWrite(LAZARUS_PIN, LOW);
    delay(500);
    digitalWrite(LAZARUS_PIN, HIGH);
    delay(100);
    ESP.restart();
}

// --- CORE 0: HIGH-SPEED SENSING ---
void SensingLoop(void * pvParameters) {
    for (;;) {
        if (xSemaphoreTake(bmeMutex, portMAX_DELAY)) {
            if (!bme.performReading()) {
                xSemaphoreGive(bmeMutex);
                vTaskDelay(100 / portTICK_PERIOD_MS);
                continue;
            }
            xSemaphoreGive(bmeMutex);
        }
        vTaskDelay(250 / portTICK_PERIOD_MS);
    }
}

// --- CORE 1: FORENSIC ANALYTICS & SRI ENGINE ---
void AnalyticsLoop(void * pvParameters) {
    for (;;) {
        float rawGas, humidity;

        if (xSemaphoreTake(bmeMutex, portMAX_DELAY)) {
            rawGas = bme.gas_resistance;
            humidity = bme.humidity;
            xSemaphoreGive(bmeMutex);
        }

        float gasCompensated = rawGas * (1.0 + ((humidity - 40.0) * 0.045));

        if (rollingBaseline == 0) rollingBaseline = gasCompensated;

        float currentDelta = abs(gasCompensated - rollingBaseline);
        resonanceBuffer[resonanceIdx] = currentDelta;
        resonanceIdx = (resonanceIdx + 1) % 20;

        float rSum = 0;
        for (int i = 0; i < 20; i++) rSum += resonanceBuffer[i];
        oracle.sri = (rSum / 20.0) / 100.0;

        float deviation = ((rollingBaseline - gasCompensated) / rollingBaseline) * 100.0;
        oracle.msi = (deviation * 0.6) + (oracle.sri * 0.4);
        oracle.spi = (deviation * 0.4) + (oracle.sri * 0.6);

        oracle.truthScore = 100.0 - (abs(oracle.msi - oracle.spi) * 2.0);
        if (oracle.truthScore < 0) oracle.truthScore = 0;

        oracle.isAnomaly = (oracle.sri > 5.0 || oracle.msi > 15.0 || oracle.spi > 10.0);
        oracle.state = oracle.isAnomaly ? "RESONANCE_DISTURBANCE" : "VOID_STABLE";

        // Serial Telemetry
        Serial.printf("{\"v\":\"OMEGA_2.1\",\"s\":\"%s\",\"sri\":%.3f,\"msi\":%.2f,\"spi\":%.2f,\"truth\":%.1f,\"alert\":%s}\n",
                      oracle.state.c_str(), oracle.sri, oracle.msi, oracle.spi, oracle.truthScore,
                      oracle.isAnomaly ? "true" : "false");

        if (!oracle.isAnomaly && oracle.sri < 1.0) {
            rollingBaseline = (gasCompensated * OMEGA_ALPHA) + (rollingBaseline * (1.0 - OMEGA_ALPHA));
        }

#ifdef OMEGA_WIFI
        if (WiFi.status() == WL_CONNECTED) {
            HTTPClient http;
            http.begin(XBIO_INGEST_URL);
            http.addHeader("Content-Type", "application/json");
            http.setTimeout(3000);

            JsonDocument doc;
            doc["device_id"] = DEVICE_ID;
            doc["v"] = "OMEGA_2.1";
            doc["s"] = oracle.state.c_str();
            doc["sri"] = roundf(oracle.sri * 1000) / 1000;
            doc["msi"] = roundf(oracle.msi * 100) / 100;
            doc["spi"] = roundf(oracle.spi * 100) / 100;
            doc["truth"] = roundf(oracle.truthScore * 10) / 10;
            doc["alert"] = oracle.isAnomaly;
            doc["ts"] = (long)(millis() / 1000);

            String payload;
            serializeJson(doc, payload);
            int code = http.POST(payload);
            http.end();
        }
#endif

        vTaskDelay(200 / portTICK_PERIOD_MS);
    }
}

void setup() {
    Serial.begin(TELEMETRY_BAUD);
    pinMode(LAZARUS_PIN, OUTPUT);
    digitalWrite(LAZARUS_PIN, HIGH);

    bmeMutex = xSemaphoreCreateMutex();
    if (bmeMutex == NULL) {
        Serial.println(">>> [FATAL] MUTEX CREATION FAILED. REBIRTHING...");
        lazarusRebirth();
    }

    Serial.println("\n>>> [ABDALA_MRF] X-BIO OMEGA V2.1 SYNCHRONIZED");

    Wire.begin(I2C_SDA, I2C_SCL);
    Wire.setClock(400000);

    if (!bme.begin(0x76)) {
        lazarusRebirth();
    }

    bme.setTemperatureOversampling(BME680_OS_16X);
    bme.setHumidityOversampling(BME680_OS_16X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_127);
    bme.setGasHeater(400, 100);

#ifdef OMEGA_WIFI
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    Serial.println(">>> WiFi connecting...");
#endif

    xTaskCreatePinnedToCore(SensingLoop, "Sensing", 10000, NULL, 1, &SensingTask, 0);
    xTaskCreatePinnedToCore(AnalyticsLoop, "Analytics", 10000, NULL, 1, &AnalyticsTask, 1);

    Serial.println(">>> SOVEREIGN WITNESS SYNCED. READY FOR FORENSIC DEPLOYMENT.");
}

void loop() {
    // Core processes are task-managed by FreeRTOS. Loop remains idle for peak efficiency.
}
