#include <Arduino.h>
#include <LittleFS.h>
#include <Wire.h>
#include "state_machine.h"
#include "config_storage.h"
#include "session_logger.h"
#include "ble_service.h"
// #include "bme688_sensor.h"  // مُعطَّل مؤقتاً
#include "session_sync.h"

// تعريف أطراف I2C للـ ESP32-S3 (عدّل حسب تصميمك)
#define I2C_SDA 21
#define I2C_SCL 22

#define BUTTON_PIN 0   // عدل حسب توصيلتك الفعلية

volatile bool g_buttonPressed = false;

void IRAM_ATTR buttonISR() {
  g_buttonPressed = true;
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println();
  Serial.println("=== X-Bio Sentinel Firmware (BSEC2 + BME688) ===");

  // تهيئة I2C
  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.setClock(400000); // 400kHz Fast Mode
  Serial.println("[MAIN] I2C initialized");

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);

  if (!mountFileSystem()) {
    Serial.println("[MAIN] FS mount failed (LittleFS)");
  }

  stateMachineInit();
  bleServiceInit();
  sessionSyncInit();

  Serial.println("[MAIN] Setup done. Device in IDLE.");
  Serial.printf("[MAIN] Free heap: %u bytes\n", ESP.getFreeHeap());
  Serial.printf("[MAIN] Free PSRAM: %u bytes\n", ESP.getFreePsram());
}

void loop() {
  if (g_buttonPressed) {
    g_buttonPressed = false;
    stateMachineOnTrigger();
  }

  stateMachineStep();
  bleServiceLoop();
  sessionSyncLoop();

  delay(10);
}
