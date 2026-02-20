#pragma once
#include <Arduino.h>

enum class ModeType : uint8_t { MODE_A = 0, MODE_B = 1, MODE_C = 2 };

enum class DeviceState : uint8_t {
  IDLE = 0,
  LOAD_CONFIG_A,
  MEASURE_A,
  LOAD_CONFIG_B,
  MEASURE_B,
  LOAD_CONFIG_C,
  MEASURE_C,
  SAVE_RESULTS,
  READY_FOR_SYNC,
  ERROR_STATE
};

struct SampleRaw {
  float temperature_c;
  float humidity_pct;
  float pressure_hpa;
  float gas_res_ohm;
  uint32_t timestamp_ms;
  uint8_t heater_step;
};

struct SampleBsec {
  float iaq = NAN;
  float voc_index = NAN;
  float co2_eq = NAN;
  float breath_voc_eq = NAN;
};

struct ModeSample {
  ModeType mode;
  SampleRaw raw;
  SampleBsec bsec;
};

struct SampleBuffer {
  uint32_t capacity;
  uint32_t count;
  ModeSample samples[];   // flexible array member
};

struct DeviceContext {
  DeviceState state = DeviceState::IDLE;
  uint32_t cycle_id = 0;
  String device_id = "XBIO-S3-0001";
  SampleBuffer* sample_buffer = nullptr;
  unsigned long state_started_ms = 0;
  bool modeA_done = false;
  bool modeB_done = false;
  bool modeC_done = false;
  int last_error = 0;
};

extern DeviceContext g_ctx;

void stateMachineInit();
void stateMachineStep();
void stateMachineOnTrigger();  // button / BLE trigger
void stateMachineOnBsecSample(const ModeSample& sample);
bool stateMachineHasPendingSession();
