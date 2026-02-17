# 📱 كيفية بناء ملف APK

## الطريقة 1️⃣: باستخدام Android Studio (الأفضل والأسهل)

### الخطوات:

1. **تحميل Android Studio**
   - اذهب إلى: https://developer.android.com/studio
   - انقر على "Download Android Studio"
   - ثبّت البرنامج

2. **فتح المشروع**
   - افتح Android Studio
   - اضغط: File → Open
   - اختر المجلد: `c:\Users\FIRAS\BME688_Android_App`
   - انتظر حتى تنتهي مزامنة Gradle

3. **بناء APK**
   - اضغط: Build → Build Bundle(s) / APK(s) → Build APK(s)
   - سيظهر شريط التقدم
   - عند الانتهاء ستجد الملف في:
     ```
     c:\Users\FIRAS\BME688_Android_App\app\build\outputs\apk\debug\app-debug.apk
     ```

4. **تثبيت على الهاتف**
   - وصّل الهاتف بـ USB
   - فعّل "USB Debugging" من Developer Options
   - اضغط في Android Studio: Run (أو Shift+F10)
   - اختر جهازك

---

## الطريقة 2️⃣: باستخدام سطر الأوامر

### المتطلبات:
- Java 11+
- Android SDK
- Gradle (أو استخدام Gradle Wrapper)

### الخطوات:

```powershell
# 1. انتقل إلى مجلد المشروع
cd c:\Users\FIRAS\BME688_Android_App

# 2. بناء Debug APK
.\gradlew.bat assembleDebug

# 3. أو بناء Release APK
.\gradlew.bat assembleRelease
```

### ملفات الإخراج:
```
Debug:   app/build/outputs/apk/debug/app-debug.apk
Release: app/build/outputs/apk/release/app-release.apk
```

---

## الطريقة 3️⃣: باستخدام Windows (إذا فشلت الطرق السابقة)

```powershell
# 1. تحقق من Java
java -version

# 2. تحقق من Android SDK
echo $env:ANDROID_HOME

# 3. حاول البناء
cd c:\Users\FIRAS\BME688_Android_App
& "C:\Users\FIRAS\AppData\Local\Android\Sdk\cmdline-tools\latest\bin\sdkmanager.exe" --list
```

---

## 🔧 استكشاف الأخطاء

### ❌ "Could not find or load main class"
```
السبب: gradle-wrapper.jar ناقص
الحل: استخدم Android Studio بدلاً من Command Line
```

### ❌ "Java not found"
```
السبب: Java غير مثبت
الحل: ثبّت Java 11+: https://www.oracle.com/java/technologies/downloads/
```

### ❌ "Android SDK not found"
```
السبب: Android SDK غير مثبت
الحل: ثبّت Android Studio (يثبّت SDK تلقائياً)
```

---

## 📊 معلومات المشروع

| العنصر | التفاصيل |
|--------|----------|
| اسم التطبيق | BME688 Sensor Monitor |
| الحزمة | com.bme688.sensorapp |
| الإصدار | 1.0 |
| Android Min | API 21 (Android 5.0) |
| Android Target | API 34 |
| Language | Kotlin |

---

## ✅ ملفات المشروع جاهزة

```
✅ 7 ملفات Kotlin
✅ 10 ملفات XML
✅ 5 ملفات موارد
✅ 4 ملفات Gradle
✅ جميع الملفات الضرورية موجودة
```

---

## 🚀 التوصية

**استخدم Android Studio** - هو الأفضل والأسهل للمبتدئين!

---

**آخر تحديث:** ديسمبر 2024
