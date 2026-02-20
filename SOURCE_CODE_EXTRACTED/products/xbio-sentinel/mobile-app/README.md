# xBio Sentinel — Mobile App

Android application for BME688 environmental sensor monitoring.

## Features
- ✅ Real-time temperature, humidity, pressure monitoring
- ✅ Air quality analysis (VOCs detection)
- ✅ Bluetooth LE connectivity with BME688 sensor
- ✅ Data visualization and trend analysis
- ✅ Historical data logging
- ✅ Alert notifications

## Tech Stack
- **Language:** Kotlin
- **Build System:** Gradle
- **Min SDK:** API 21 (Android 5.0)
- **Target SDK:** API 33 (Android 13)
- **Architecture:** MVVM
- **Dependencies:**
  - Bluetooth LE library
  - Charts library for visualization
  - Room Database for local storage

## BME688 Sensor Specifications
The Bosch BME688 is a low-power gas sensor with integrated:
- **Temperature:** -40°C to +85°C (±1°C accuracy)
- **Humidity:** 0-100% RH (±3% accuracy)
- **Pressure:** 300-1100 hPa (±1.0 hPa accuracy)
- **Gas (VOCs):** Air quality index (0-500 scale)

## Build Instructions
\`\`\`bash
cd mobile-app/BME688_Android_App
./gradlew assembleDebug

# Install on device
adb install -r app/build/outputs/apk/debug/app-debug.apk
\`\`\`

## Sensor Communication
- **Protocol:** Bluetooth Low Energy (BLE) 4.2+
- **Service UUID:** Custom BME688 profile
- **Characteristics:**
  - Temperature (Read/Notify)
  - Humidity (Read/Notify)
  - Pressure (Read/Notify)
  - Gas Resistance (Read/Notify)
  - Air Quality Index (Read/Notify)

## Project Structure
\`\`\`
BME688_Android_App/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/bme688/sensorapp/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── SensorService.kt
│   │   │   │   ├── BluetoothManager.kt
│   │   │   │   └── DataProcessor.kt
│   │   │   ├── res/
│   │   │   │   ├── layout/ (18 XML files)
│   │   │   │   └── values/
│   │   │   └── AndroidManifest.xml
│   ├── build.gradle
│   └── proguard-rules.pro
├── gradle/
└── build.gradle
\`\`\`

## Usage
1. **Pair Sensor:** Enable Bluetooth, scan for BME688 device
2. **Connect:** Tap on sensor from list
3. **Monitor:** View real-time readings on dashboard
4. **Analyze:** Check historical trends and air quality scores
5. **Alerts:** Set thresholds for temperature, humidity, air quality

## Development
\`\`\`bash
# Run tests
./gradlew test

# Generate signed APK
./gradlew assembleRelease
\`\`\`

## Permissions Required
\`\`\`xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
\`\`\`

---
**Restored from archive:** 2026-02-20  
**Version:** 1.0.0  
**Application ID:** com.bme688.sensorapp  
**Status:** ✅ Ready for development/deployment
