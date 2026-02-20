#include "session_logger.h"
#include <LittleFS.h>
#include <time.h>

bool sessionLoggerInit() {
  // مستقبلاً: مزامنة وقت حقيقي من الموبايل / الإنترنت
  return true;
}

static String iso8601FromMs(uint64_t ms) {
  time_t sec = ms / 1000;
  struct tm t;
  gmtime_r(&sec, &t);
  char buf[32];
  strftime(buf, sizeof(buf), "%Y-%m-%dT%H-%M-%SZ", &t);
  return String(buf);
}

String buildSessionFilename(const SessionMeta& meta) {
  String ts = iso8601FromMs(meta.started_unix_ms);
  char buf[128];
  snprintf(buf, sizeof(buf), "/sessions/%s_cycle_%04lu.json",
           ts.c_str(), (unsigned long)meta.cycle_id);
  return String(buf);
}

bool saveCurrentCycle(const DeviceContext& ctx) {
  if (!ctx.sample_buffer || ctx.sample_buffer->count == 0) {
    Serial.println("[LOG] No samples to save");
    return false;
  }

  SessionMeta meta;
  meta.cycle_id = ctx.cycle_id;
  meta.started_unix_ms = (uint64_t)millis();
  meta.ended_unix_ms = (uint64_t)millis();
  meta.device_id = ctx.device_id;

  String path = buildSessionFilename(meta);
  Serial.printf("[LOG] Writing session to %s\n", path.c_str());

  LittleFS.mkdir("/sessions");
  File f = LittleFS.open(path, "w");
  if (!f) {
    Serial.println("[LOG] Failed to open session file for write");
    return false;
  }

  f.print("{\n");
  f.printf("  \"version\":1,\n");
  f.printf("  \"device_id\":\"%s\",\n", meta.device_id.c_str());
  f.printf("  \"cycle_id\":%lu,\n", (unsigned long)meta.cycle_id);
  f.printf("  \"started_at\":\"%s\",\n", iso8601FromMs(meta.started_unix_ms).c_str());
  f.printf("  \"ended_at\":\"%s\",\n", iso8601FromMs(meta.ended_unix_ms).c_str());
  f.print("  \"samples\":[\n");

  for (uint32_t i = 0; i < ctx.sample_buffer->count; ++i) {
    const auto& s = ctx.sample_buffer->samples[i];
    char modeChar = (s.mode == ModeType::MODE_A) ? 'A' :
                    (s.mode == ModeType::MODE_B) ? 'B' : 'C';

    f.printf(
      "    {\"mode\":\"%c\",\"t_ms\":%lu,\"heater_step\":%u,"
      "\"raw\":{\"temp_c\":%.2f,\"humidity_pct\":%.2f,"
      "\"pressure_hpa\":%.2f,\"gas_res_ohm\":%.1f},"
      "\"bsec\":{\"iaq\":%.2f,\"voc_index\":%.2f,"
      "\"co2_eq\":%.2f,\"breath_voc_eq\":%.3f}}%s\n",
      modeChar,
      (unsigned long)s.raw.timestamp_ms,
      s.raw.heater_step,
      s.raw.temperature_c,
      s.raw.humidity_pct,
      s.raw.pressure_hpa,
      s.raw.gas_res_ohm,
      s.bsec.iaq,
      s.bsec.voc_index,
      s.bsec.co2_eq,
      s.bsec.breath_voc_eq,
      (i + 1 < ctx.sample_buffer->count) ? "," : ""
    );
  }

  f.print("  ]\n}\n");
  f.close();
  Serial.println("[LOG] Session saved");
  return true;
}
