#pragma once
#include <Arduino.h>

// في النسخة الحالية، نستخدمه فقط للتحقق من وجود ملفات config.
// لاحقاً تضيف تحميل حقيقي لـ .bmeconfig إلى RAM.

bool mountFileSystem();
bool loadAllConfigs(); // ترجع true لو الملفات الأساسية موجودة
