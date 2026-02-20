#include "bme688_sensor.h"
#include <LittleFS.h>
#include <Wire.h>

// Global instance
BME688Sensor g_bme688;

// Static callback wrapper - BSEC2 يستدعيه عند توفر بيانات جديدة
static BME688Sensor* g_bme688Instance = nullptr;

BME688Sensor::BME688Sensor() 
  : sampleCallback(nullptr), bsecReady(false), currentMode(ModeType::MODE_A) {
  g_bme688Instance = this;
}

bool BME688Sensor::begin(uint8_t i2cAddr) {
  Wire.begin();
  
  // تهيئة BSEC2
  if (!bsec.begin(BME68X_I2C_INTF, bme68xI2CRead, bme68xI2CWrite, bme68xDelayUs, nullptr)) {
    lastError = "BSEC init failed";
    Serial.println("[BME688] " + lastError);
    return false;
  }
  
  // تعيين I2C address
  bsec.setConfig(bme68xI2CConfig);
  
  // قائمة الـ outputs المطلوبة من BSEC
  bsecSensor sensorList[] = {
    BSEC_OUTPUT_RAW_TEMPERATURE,
    BSEC_OUTPUT_RAW_PRESSURE,
    BSEC_OUTPUT_RAW_HUMIDITY,
    BSEC_OUTPUT_RAW_GAS,
    BSEC_OUTPUT_IAQ,
    BSEC_OUTPUT_STATIC_IAQ,
    BSEC_OUTPUT_CO2_EQUIVALENT,
    BSEC_OUTPUT_BREATH_VOC_EQUIVALENT,
    BSEC_OUTPUT_SENSOR_HEAT_COMPENSATED_TEMPERATURE,
    BSEC_OUTPUT_SENSOR_HEAT_COMPENSATED_HUMIDITY,
  };
  
  if (!bsec.updateSubscription(sensorList, ARRAY_LEN(sensorList), BSEC_SAMPLE_RATE_LP)) {
    lastError = "BSEC subscription failed";
    Serial.println("[BME688] " + lastError);
    return false;
  }
  
  bsecReady = true;
  Serial.println("[BME688] Sensor initialized successfully");
  return true;
}

bool BME688Sensor::loadBsecConfig(const uint8_t* configData, uint32_t configLen) {
  if (!configData || configLen == 0) {
    lastError = "Invalid config data";
    return false;
  }
  
  if (bsec.setConfig(configData) != BSEC_OK) {
    lastError = "Failed to set BSEC config";
    Serial.println("[BME688] " + lastError);
    return false;
  }
  
  Serial.println("[BME688] BSEC config loaded successfully");
  return true;
}

bool BME688Sensor::loadBsecState(const uint8_t* stateData, uint32_t stateLen) {
  if (!stateData || stateLen == 0) {
    lastError = "Invalid state data";
    return false;
  }
  
  if (bsec.setState(stateData) != BSEC_OK) {
    lastError = "Failed to set BSEC state";
    Serial.println("[BME688] " + lastError);
    return false;
  }
  
  Serial.println("[BME688] BSEC state loaded successfully");
  return true;
}

bool BME688Sensor::saveBsecState(uint8_t* stateData, uint32_t& stateLen) {
  if (!stateData) {
    lastError = "Invalid state buffer";
    return false;
  }
  
  if (bsec.getState(stateData) != BSEC_OK) {
    lastError = "Failed to get BSEC state";
    Serial.println("[BME688] " + lastError);
    return false;
  }
  
  stateLen = BSEC_MAX_STATE_BLOB_SIZE;
  Serial.println("[BME688] BSEC state saved successfully");
  return true;
}

void BME688Sensor::run() {
  if (!bsecReady) return;
  
  // استدعاء BSEC للحصول على قراءات جديدة
  if (!bsec.run()) {
    // في حال وجود خطأ، سجّله
    if (bsec.status != BSEC_OK) {
      lastError = "BSEC run error: " + String(bsec.status);
    }
    return;
  }
  
  // إذا كانت هناك بيانات جديدة
  if (bsec.newDataAvailable()) {
    bsecOutputs outputs = bsec.getOutputs();
    bme68xData sensorData = bsec.getData();
    
    // تحويل إلى ModeSample
    ModeSample sample{};
    sample.mode = currentMode;
    
    // البيانات الخام
    sample.raw.temperature_c = sensorData.temperature;
    sample.raw.humidity_pct = sensorData.humidity;
    sample.raw.pressure_hpa = sensorData.pressure / 100.0f; // Pa to hPa
    sample.raw.gas_res_ohm = sensorData.gas_resistance;
    sample.raw.timestamp_ms = millis();
    sample.raw.heater_step = sensorData.gas_index;
    
    // بيانات BSEC
    processBsecOutputs(outputs, sample);
    
    // استدعاء callback إذا كان مسجلاً
    if (sampleCallback) {
      sampleCallback(sample);
    }
  }
}

void BME688Sensor::setSampleCallback(BsecCallback callback) {
  sampleCallback = callback;
}

void BME688Sensor::processBsecOutputs(const bsecOutputs& outputs, ModeSample& sample) {
  for (uint8_t i = 0; i < outputs.nOutputs; i++) {
    const bsecData& output = outputs.output[i];
    
    switch (output.sensor_id) {
      case BSEC_OUTPUT_IAQ:
        sample.bsec.iaq = output.signal;
        break;
      case BSEC_OUTPUT_STATIC_IAQ:
        // يمكن استخدامه كبديل أو إضافي
        break;
      case BSEC_OUTPUT_CO2_EQUIVALENT:
        sample.bsec.co2_eq = output.signal;
        break;
      case BSEC_OUTPUT_BREATH_VOC_EQUIVALENT:
        sample.bsec.breath_voc_eq = output.signal;
        break;
      case BSEC_OUTPUT_RAW_GAS:
        // يمكن استخدامه كـ VOC index تقريبي
        sample.bsec.voc_index = output.signal / 1000.0f; // normalization
        break;
    }
  }
}

bool BME688Sensor::readRawData(SampleRaw& rawData) {
  if (!bsecReady) {
    lastError = "Sensor not ready";
    return false;
  }
  
  // قراءة بيانات خام بدون BSEC processing
  bme68xData data = bsec.getData();
  
  rawData.temperature_c = data.temperature;
  rawData.humidity_pct = data.humidity;
  rawData.pressure_hpa = data.pressure / 100.0f;
  rawData.gas_res_ohm = data.gas_resistance;
  rawData.timestamp_ms = millis();
  rawData.heater_step = data.gas_index;
  
  return true;
}

// ============================================================================
// تطبيق تكوينات الأوضاع المختلفة
// ============================================================================

bool applyModeAConfig() {
  Serial.println("[BME688] Applying Mode A config");
  
  // محاولة تحميل config من ملف
  if (LittleFS.exists("/config/config_A.bmeconfig")) {
    File f = LittleFS.open("/config/config_A.bmeconfig", "r");
    if (f) {
      size_t size = f.size();
      uint8_t* configData = new uint8_t[size];
      f.read(configData, size);
      f.close();
      
      bool result = g_bme688.loadBsecConfig(configData, size);
      delete[] configData;
      
      if (result) {
        Serial.println("[BME688] Mode A config loaded from file");
        return true;
      }
    }
  }
  
  // إذا لم يكن هناك ملف، استخدم التكوين الافتراضي
  Serial.println("[BME688] Using default Mode A config");
  
  // هنا يمكن تعيين معايير heater profile مخصصة
  // مثال: وضع قياس IAQ عام
  return true;
}

bool applyModeBConfig() {
  Serial.println("[BME688] Applying Mode B config");
  
  if (LittleFS.exists("/config/config_B.bmeconfig")) {
    File f = LittleFS.open("/config/config_B.bmeconfig", "r");
    if (f) {
      size_t size = f.size();
      uint8_t* configData = new uint8_t[size];
      f.read(configData, size);
      f.close();
      
      bool result = g_bme688.loadBsecConfig(configData, size);
      delete[] configData;
      
      if (result) {
        Serial.println("[BME688] Mode B config loaded from file");
        return true;
      }
    }
  }
  
  Serial.println("[BME688] Using default Mode B config");
  return true;
}

bool applyModeCConfig() {
  Serial.println("[BME688] Applying Mode C config");
  
  if (LittleFS.exists("/config/config_C.bmeconfig")) {
    File f = LittleFS.open("/config/config_C.bmeconfig", "r");
    if (f) {
      size_t size = f.size();
      uint8_t* configData = new uint8_t[size];
      f.read(configData, size);
      f.close();
      
      bool result = g_bme688.loadBsecConfig(configData, size);
      delete[] configData;
      
      if (result) {
        Serial.println("[BME688] Mode C config loaded from file");
        return true;
      }
    }
  }
  
  Serial.println("[BME688] Using default Mode C config");
  return true;
}
