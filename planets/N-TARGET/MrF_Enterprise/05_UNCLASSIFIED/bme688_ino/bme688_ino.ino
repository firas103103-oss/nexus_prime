#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>

// I2C pins on your ESP32-S3 board
#define I2C_SDA 19
#define I2C_SCL 20

// I2C address of BME688/BME680
// 0x76 if ADDR pin -> GND
// 0x77 if ADDR pin -> 3V3
#define BME_ADDR 0x76

Adafruit_BME680 bme;  // I2C constructor (we'll set Wire manually)

void setup() {
  Serial.begin(115200);
  delay(2000);

  Serial.println();
  Serial.println(F("Starting ESP32-S3 + BME688 (I2C)..."));

  // Start I2C on the chosen pins
  Wire.begin(I2C_SDA, I2C_SCL);

  if (!bme.begin(BME_ADDR, &Wire)) {
    Serial.println(F("Could not find a valid BME680/BME688 sensor, check wiring!"));
    while (1) {
      delay(1000);
    }
  }

  // Configure sensor settings
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);  // 320°C for 150 ms
}

void loop() {
  if (!bme.performReading()) {
    Serial.println(F("Failed to perform reading :("));
    return;
  }

  Serial.println(F("===== BME688 Reading ====="));
  Serial.print(F("Temperature: "));
  Serial.print(bme.temperature);
  Serial.println(F(" *C"));

  Serial.print(F("Pressure: "));
  Serial.print(bme.pressure / 100.0);
  Serial.println(F(" hPa"));

  Serial.print(F("Humidity: "));
  Serial.print(bme.humidity);
  Serial.println(F(" %"));

  Serial.print(F("Gas resistance: "));
  Serial.print(bme.gas_resistance / 1000.0);
  Serial.println(F(" KOhms"));

  Serial.println();
  delay(2000);  // read every 2 seconds
}
