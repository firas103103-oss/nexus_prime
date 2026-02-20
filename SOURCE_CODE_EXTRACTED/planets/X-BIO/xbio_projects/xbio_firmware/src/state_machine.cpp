#include "state_machine.h"
#include "config_storage.h"
#include "session_logger.h"
#include "ble_service.h"
// #include "bme688_sensor.h"  // مُعطَّل مؤقتاً

#include <esp_heap_caps.h>

DeviceContext g_ctx;

// عدد العينات الأقصى في الدورة الواحدة (تعديل حسب الحاجة)
static const uint32_t MAX_SAMPLES = 5000;

// نحفظ الوقت لعمل sampling وهمي (مؤقتاً لحين إضافة BME688)
static uint32_t last_fake_sample_ms = 0;

// تطبيق تكوين BSEC حسب الوضع (stub مؤقتاً)
static bool applyBsecConfigForMode(ModeType mode) {
  Serial.printf("[BSEC] Apply config for mode %d (stub - BME688 disabled)\n", static_cast<int>(mode));
  return true;
}

// نولّد Sample وهمي كل 200 ms أثناء MEASURE_* (مؤقتاً)
static void maybeGenerateFakeSample(ModeType mode) {
  if (!g_ctx.sample_buffer) return;
  uint32_t now = millis();
  if (now - last_fake_sample_ms < 200) return;
  last_fake_sample_ms = now;

  if (g_ctx.sample_buffer->count >= g_ctx.sample_buffer->capacity) return;

  ModeSample s{};
  s.mode = mode;
  s.raw.timestamp_ms = now;
  s.raw.heater_step = (now / 200) % 16;
  s.raw.temperature_c = 30.0f + (float)(s.raw.heater_step);
  s.raw.humidity_pct = 40.0f + (float)((now / 1000) % 10);
  s.raw.pressure_hpa = 1000.0f;
  s.raw.gas_res_ohm = 100000.0f + 1000.0f * (float)(s.raw.heater_step);

  s.bsec.iaq = 50.0f + (float)(s.raw.heater_step);
  s.bsec.voc_index = 100.0f + (float)((now / 1000) % 20);
  s.bsec.co2_eq = 500.0f;
  s.bsec.breath_voc_eq = 0.8f;

  g_ctx.sample_buffer->samples[g_ctx.sample_buffer->count++] = s;
}

void stateMachineOnBsecSample(const ModeSample& sample) {
  // هذا الهاندلر للاستخدام مع BSEC الحقيقي لاحقاً
  if (!g_ctx.sample_buffer) return;
  if (g_ctx.sample_buffer->count >= g_ctx.sample_buffer->capacity) return;
  g_ctx.sample_buffer->samples[g_ctx.sample_buffer->count++] = sample;
}

void stateMachineOnTrigger() {
  if (g_ctx.state == DeviceState::IDLE || g_ctx.state == DeviceState::READY_FOR_SYNC) {
    Serial.println("[SM] Trigger received");
    g_ctx.cycle_id++;
    if (g_ctx.sample_buffer) {
      g_ctx.sample_buffer->count = 0;
    }
    g_ctx.modeA_done = g_ctx.modeB_done = g_ctx.modeC_done = false;
    g_ctx.state = DeviceState::LOAD_CONFIG_A;
    g_ctx.state_started_ms = millis();
    bleNotifyState(g_ctx);
  }
}

void stateMachineInit() {
  // allocate SampleBuffer في PSRAM
  size_t bytes = sizeof(SampleBuffer) + MAX_SAMPLES * sizeof(ModeSample);
  SampleBuffer* buf = (SampleBuffer*)heap_caps_malloc(bytes, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
  if (!buf) {
    Serial.println("[SM] Failed to alloc SampleBuffer in PSRAM");
    g_ctx.last_error = 1;
  } else {
    buf->capacity = MAX_SAMPLES;
    buf->count = 0;
    g_ctx.sample_buffer = buf;
    Serial.printf("[SM] SampleBuffer allocated: %u samples\n", MAX_SAMPLES);
  }

  if (!loadAllConfigs()) {
    Serial.println("[SM] Config load failed (stub, will continue anyway)");
  }

  // BME688 مُعطَّل مؤقتاً - سيتم تفعيله لاحقاً
  Serial.println("[SM] BME688 disabled - using fake samples");

  sessionLoggerInit();
}

static bool timeoutSince(uint32_t startMs, uint32_t timeoutMs) {
  return (millis() - startMs) > timeoutMs;
}

bool stateMachineHasPendingSession() {
  return (g_ctx.state == DeviceState::READY_FOR_SYNC);
}

void stateMachineStep() {
  // BME688 مُعطَّل مؤقتاً
  // g_bme688.run();
  
  switch (g_ctx.state) {
    case DeviceState::IDLE:
      break;

    case DeviceState::LOAD_CONFIG_A:
      if (applyBsecConfigForMode(ModeType::MODE_A)) {
        Serial.println("[SM] Mode A config applied");
        g_ctx.state = DeviceState::MEASURE_A;
        g_ctx.state_started_ms = millis();
      } else {
        g_ctx.state = DeviceState::ERROR_STATE;
        g_ctx.last_error = 3;
      }
      bleNotifyState(g_ctx);
      break;

    case DeviceState::MEASURE_A:
      maybeGenerateFakeSample(ModeType::MODE_A);
      if (timeoutSince(g_ctx.state_started_ms, 20 * 1000UL)) {
        g_ctx.state = DeviceState::LOAD_CONFIG_B;
        g_ctx.modeA_done = true;
        g_ctx.state_started_ms = millis();
        bleNotifyState(g_ctx);
      }
      break;

    case DeviceState::LOAD_CONFIG_B:
      if (applyBsecConfigForMode(ModeType::MODE_B)) {
        Serial.println("[SM] Mode B config applied");
        g_ctx.state = DeviceState::MEASURE_B;
        g_ctx.state_started_ms = millis();
      } else {
        g_ctx.state = DeviceState::ERROR_STATE;
        g_ctx.last_error = 5;
      }
      bleNotifyState(g_ctx);
      break;

    case DeviceState::MEASURE_B:
      maybeGenerateFakeSample(ModeType::MODE_B);
      if (timeoutSince(g_ctx.state_started_ms, 10 * 1000UL)) {
        g_ctx.state = DeviceState::LOAD_CONFIG_C;
        g_ctx.modeB_done = true;
        g_ctx.state_started_ms = millis();
        bleNotifyState(g_ctx);
      }
      break;

    case DeviceState::LOAD_CONFIG_C:
      if (applyBsecConfigForMode(ModeType::MODE_C)) {
        Serial.println("[SM] Mode C config applied");
        g_ctx.state = DeviceState::MEASURE_C;
        g_ctx.state_started_ms = millis();
      } else {
        g_ctx.state = DeviceState::ERROR_STATE;
        g_ctx.last_error = 7;
      }
      bleNotifyState(g_ctx);
      break;

    case DeviceState::MEASURE_C:
      maybeGenerateFakeSample(ModeType::MODE_C);
      if (timeoutSince(g_ctx.state_started_ms, 20 * 1000UL)) {
        g_ctx.state = DeviceState::SAVE_RESULTS;
        g_ctx.modeC_done = true;
        g_ctx.state_started_ms = millis();
        bleNotifyState(g_ctx);
      }
      break;

    case DeviceState::SAVE_RESULTS:
      if (saveCurrentCycle(g_ctx)) {
        g_ctx.state = DeviceState::READY_FOR_SYNC;
      } else {
        g_ctx.state = DeviceState::ERROR_STATE;
        g_ctx.last_error = 9;
      }
      bleNotifyState(g_ctx);
      break;

    case DeviceState::READY_FOR_SYNC:
      // هنا المفروض BLE يقول للموبايل أنه في Session جاهزة
      break;

    case DeviceState::ERROR_STATE:
      Serial.printf("[SM] ERROR, code=%d\n", g_ctx.last_error);
      bleNotifyState(g_ctx);
      break;
  }
}
