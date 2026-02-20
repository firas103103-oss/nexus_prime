#include "config_storage.h"
#include <LittleFS.h>

bool mountFileSystem() {
  if (!LittleFS.begin(true)) {
    Serial.println("[FS] LittleFS mount failed");
    return false;
  }
  Serial.println("[FS] LittleFS mounted");
  return true;
}

bool loadAllConfigs() {
  // TODO: لاحقاً اقرأ: /config/config_A.bmeconfig و B و C
  // الآن نكتفي بالتأكد أن المجلد موجود (أو إنشاؤه)
  if (!LittleFS.exists("/config")) {
    LittleFS.mkdir("/config");
    Serial.println("[CFG] /config created (no real configs yet)");
    return false;
  }
  Serial.println("[CFG] /config exists (stub)");
  return true;
}
