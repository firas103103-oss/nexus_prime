#pragma once
#include <Arduino.h>
#include "state_machine.h"
#include <bsec2.h>

// I2C address للحساس (عادة 0x76 أو 0x77)
#define BME688_I2C_ADDR UINT8_C(0x77)

// Callback function type للحصول على العينات
typedef void (*BsecCallback)(const ModeSample& sample);

class BME688Sensor {
public:
  BME688Sensor();
  
  // تهيئة الحساس وBSEC
  bool begin(uint8_t i2cAddr = BME688_I2C_ADDR);
  
  // تحميل تكوين BSEC من ملف
  bool loadBsecConfig(const uint8_t* configData, uint32_t configLen);
  
  // تحميل حالة BSEC المحفوظة (للمعايرة)
  bool loadBsecState(const uint8_t* stateData, uint32_t stateLen);
  
  // حفظ حالة BSEC الحالية
  bool saveBsecState(uint8_t* stateData, uint32_t& stateLen);
  
  // بدء القياس (يجب استدعاؤها في loop)
  void run();
  
  // تسجيل callback للحصول على العينات
  void setSampleCallback(BsecCallback callback);
  
  // الحصول على آخر خطأ
  String getLastError() const { return lastError; }
  
  // التحقق من جاهزية الحساس
  bool isReady() const { return bsecReady; }
  
  // قراءة البيانات الخام فقط (بدون BSEC)
  bool readRawData(SampleRaw& rawData);

private:
  Bsec2 bsec;
  BsecCallback sampleCallback;
  String lastError;
  bool bsecReady;
  ModeType currentMode;
  
  // Helper function لتحويل output من BSEC
  void processBsecOutputs(const bsecOutputs& outputs, ModeSample& sample);
  
  // BSEC callback wrapper
  static void bsecOutputCallback(const bme68xData data, const bsecOutputs outputs, Bsec2 bsec);
};

// Global instance (يمكن الوصول إليه من state_machine)
extern BME688Sensor g_bme688;

// دوال مساعدة لتطبيق تكوينات الأوضاع المختلفة
bool applyModeAConfig();
bool applyModeBConfig();
bool applyModeCConfig();
