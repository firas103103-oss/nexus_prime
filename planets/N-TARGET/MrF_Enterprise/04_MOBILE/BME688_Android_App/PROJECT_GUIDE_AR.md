# دليل المشروع الشامل - BME688 Sensor Monitor

## 📱 نظرة عامة

تطبيق Android احترافي لمراقبة مستشعر البيئة BME688 عبر Bluetooth Low Energy (BLE) في الوقت الفعلي. يوفر قراءات لحظية ورسوم بيانية تاريخية وإحصائيات متقدمة.

## 🎯 الميزات الرئيسية

### 1. **الاتصال الذكي**
- اكتشاف تلقائي للأجهزة البلوتوث
- إدارة متقدمة للاتصال والقطع
- إعادة اتصال تلقائية عند الانقطاع

### 2. **عرض البيانات الحية**
- قراءات درجة الحرارة والرطوبة والضغط وجودة الهواء
- تحديث فوري للبيانات
- تنبيهات عند تجاوز الحدود

### 3. **الرسوم البيانية التفاعلية**
- رسم بياني لدرجة الحرارة بمرور الوقت
- رسم بياني للرطوبة
- رسم بياني للضغط
- إمكانية التمرير والتكبير

### 4. **الإحصائيات والتحليل**
- الحد الأدنى والأقصى والمتوسط
- حفظ البيانات التاريخية
- تصدير البيانات إلى CSV

### 5. **واجهة حديثة**
- Material Design 3
- دعم الوضع الليلي
- واجهة سهلة الاستخدام

## 📋 المتطلبات

### الأجهزة
- جهاز Android (هاتف ذكي أو جهاز لوحي)
- الإصدار: Android 5.0 (API 21) أو أحدث
- Bluetooth LE مدعوم
- ESP32 مع مستشعر BME688

### البرامج
- Android Studio 2022.1.1 أو أحدث
- Java 11+
- Gradle 8.0+
- Kotlin 1.8+

### المكتبات الرئيسية
```gradle
- AndroidX Core & AppCompat
- Material Design 3
- Lifecycle & ViewModel
- Coroutines
- MPAndroidChart
- Gson
```

## 🚀 البدء السريع

### 1. تثبيت المشروع

```bash
# استنساخ المشروع
git clone https://github.com/yourusername/BME688_Android_App.git
cd BME688_Android_App

# فتح في Android Studio
# File > Open > اختر المجلد
```

### 2. إعداد البيئة

```bash
# مزامنة Gradle
# Tools > Gradle > Sync Now

# أو من سطر الأوامر
./gradlew sync
```

### 3. تشغيل التطبيق

```bash
# تشغيل على هاتف متصل
./gradlew installDebug

# أو اضغط Shift+F10 في Android Studio
```

## 📁 هيكل المشروع

```
BME688_Android_App/
├── src/main/
│   ├── kotlin/com/bme688/sensorapp/
│   │   ├── BLEManager.kt              # إدارة Bluetooth
│   │   ├── SensorData.kt              # نماذج البيانات
│   │   ├── SensorViewModel.kt         # منطق التطبيق
│   │   ├── MainActivity.kt            # الشاشة الرئيسية
│   │   ├── DeviceListActivity.kt      # قائمة الأجهزة
│   │   ├── DeviceDetailActivity.kt    # تفاصيل الجهاز
│   │   ├── DeviceAdapter.kt           # محول القائمة
│   │   └── ...
│   │
│   ├── res/
│   │   ├── layout/
│   │   │   ├── activity_main.xml
│   │   │   ├── activity_device_detail.xml
│   │   │   ├── device_item.xml
│   │   │   └── ...
│   │   │
│   │   ├── values/
│   │   │   ├── strings.xml
│   │   │   ├── colors.xml
│   │   │   ├── themes.xml
│   │   │   └── ...
│   │   │
│   │   └── drawable/
│   │
│   └── AndroidManifest.xml
│
├── build.gradle
├── settings.gradle
├── gradle.properties
├── README.md
├── QUICK_START.md
└── ...
```

## 🔧 معمارية التطبيق

### MVVM Pattern
```
View (Activity/Fragment)
  ↓
ViewModel (SensorViewModel)
  ↓
LiveData
  ↓
Repository/Manager (BLEManager)
```

### مكونات رئيسية

#### 1. **BLEManager**
- إدارة الاتصال بـ Bluetooth
- إرسال واستقبال الأوامر
- معالجة الإشعارات

```kotlin
val bleManager = BLEManager(context)
bleManager.connectToDevice(device)
bleManager.startStreaming()
bleManager.onDataReceived = { data -> ... }
```

#### 2. **SensorViewModel**
- إدارة حالة التطبيق
- معالجة البيانات
- تحديث الواجهة

```kotlin
class SensorViewModel(app: Application) : AndroidViewModel(app)
viewModel.currentReadings.observe(this) { readings -> ... }
viewModel.startStreaming()
```

#### 3. **SensorData Models**
```kotlin
data class SensorReadings(
    val temperature: Float,
    val humidity: Float,
    val pressure: Float,
    val airQuality: Float,
    val iaq: Float,
    ...
)
```

## 📡 بروتوكول الاتصال

### UUIDs
```
Service UUID:        6E400001-B5A3-F393-E0A9-E50E24DCCA9E
TX Characteristic:   6E400003-B5A3-F393-E0A9-E50E24DCCA9E
RX Characteristic:   6E400002-B5A3-F393-E0A9-E50E24DCCA9E
```

### الأوامر المدعومة

```
start [sensor] [rate] [outputs...]    # بدء البث
stop                                  # إيقاف البث
setlabel [label_id]                  # تعيين التسمية
setlabelinfo [label] [name] [desc]   # معلومات التسمية
setrtctime [timestamp]               # ضبط الوقت
getrtctime                           # قراءة الوقت
getfwversion                         # رقم الإصدار
```

### بيانات الاستقبال (JSON)
```json
{
  "temperature": 25.5,
  "humidity": 45.3,
  "pressure": 1013.25,
  "air_quality": 65.2,
  "gas_resistance": 50000,
  "iaq": 45,
  "iaq_accuracy": 3,
  "timestamp": 1702046400000
}
```

## 🎨 تقييم جودة الهواء

| النطاق | التصنيف | اللون |
|------|---------|--------|
| 0-50 | ممتاز | 🟢 أخضر |
| 51-100 | جيد | 🟢 أخضر فاتح |
| 101-150 | ملوث قليلاً | 🟡 أصفر |
| 151-200 | ملوث معتدلاً | 🟠 برتقالي |
| 201-300 | ملوث كثيراً | 🔴 أحمر |
| 301+ | ملوث بشدة | 🔴 أحمر غامق |

## 🔐 الأذونات المطلوبة

```xml
<!-- Bluetooth -->
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />

<!-- Location (required for BLE scanning) -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

<!-- Hardware Feature -->
<uses-feature android:name="android.hardware.bluetooth_le" android:required="true" />
```

## 🧪 الاختبار

### اختبار الوحدة
```bash
./gradlew test
```

### اختبار التكامل
```bash
./gradlew connectedAndroidTest
```

### تشغيل على محاكي
```bash
./gradlew installDebug -Pdisable_precompiled_modules=true
```

## 📊 بناء APK

### Debug Build
```bash
./gradlew assembleDebug
# الملف: app/build/outputs/apk/debug/app-debug.apk
```

### Release Build
```bash
./gradlew assembleRelease
# الملف: app/build/outputs/apk/release/app-release.apk
```

## 🐛 استكشاف الأخطاء الشائعة

### مشكلة: "لا يظهر الجهاز عند البحث"
**الحل:**
```
1. تأكد من تشغيل ESP32
2. فعّل البلوتوث على الهاتف
3. امنح الأذونات المطلوبة
4. أعد تشغيل التطبيق
```

### مشكلة: "فشل الاتصال"
**الحل:**
```
1. تأكد من قرب الأجهزة
2. أعد تشغيل ESP32
3. امسح ذاكرة التطبيق
4. أعد تثبيت التطبيق
```

### مشكلة: "لا تظهر البيانات"
**الحل:**
```
1. تأكد من بدء البث (Start Streaming)
2. راجع رسائل السجل
3. تحقق من التوصيلات الفيزيائية
4. أعد ضبط معدل العينة
```

### مشكلة: "Build Failed"
**الحل:**
```bash
# تنظيف والإعادة
./gradlew clean build

# أو إعادة تعيين Gradle
./gradlew --stop
rm -rf .gradle
./gradlew build
```

## 📚 الموارد الإضافية

- [وثائق Android الرسمية](https://developer.android.com)
- [Kotlin الرسمية](https://kotlinlang.org/docs/)
- [Material Design 3](https://m3.material.io/)
- [وثائق Bosch BME688](https://www.bosch-sensortec.com/bme688/)

## 📝 الترخيص

```
BSD-3-Clause License
Copyright (c) 2024 Bosch Sensortec GmbH

See LICENSE file for details
```

## 👥 المساهمون

- Bosch Sensortec GmbH
- GitHub Copilot (Development Assistance)

## 📞 الدعم

للمساعدة والدعم:
1. راجع QUICK_START.md
2. ابحث في Issue Tracker
3. أنشئ Issue جديد
4. تواصل مع Bosch Sensortec

---

**آخر تحديث:** ديسمبر 2024  
**النسخة:** 1.0.0  
**الحالة:** جاهز للإنتاج ✅
