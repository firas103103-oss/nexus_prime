#pragma once
#include "state_machine.h"
#include <Arduino.h>

struct SessionMeta {
  uint32_t cycle_id;
  uint64_t started_unix_ms;
  uint64_t ended_unix_ms;
  String device_id;
};

bool sessionLoggerInit();
bool saveCurrentCycle(const DeviceContext& ctx);
String buildSessionFilename(const SessionMeta& meta);
