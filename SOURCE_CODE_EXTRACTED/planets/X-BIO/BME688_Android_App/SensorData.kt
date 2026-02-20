package com.bme688.sensorapp

import com.google.gson.annotations.SerializedName

data class SensorReadings(
    @SerializedName("temperature")
    val temperature: Float = 0f,
    
    @SerializedName("humidity")
    val humidity: Float = 0f,
    
    @SerializedName("pressure")
    val pressure: Float = 0f,
    
    @SerializedName("air_quality")
    val airQuality: Float = 0f,
    
    @SerializedName("gas_resistance")
    val gasResistance: Float = 0f,
    
    @SerializedName("iaq")
    val iaq: Float = 0f,
    
    @SerializedName("iaq_accuracy")
    val iaqAccuracy: Int = 0,
    
    @SerializedName("timestamp")
    val timestamp: Long = System.currentTimeMillis()
)

data class SensorStats(
    val minTemp: Float = 0f,
    val maxTemp: Float = 0f,
    val avgTemp: Float = 0f,
    val minHumidity: Float = 0f,
    val maxHumidity: Float = 0f,
    val avgHumidity: Float = 0f,
    val minPressure: Float = 0f,
    val maxPressure: Float = 0f,
    val avgPressure: Float = 0f
)

enum class AirQualityLevel {
    EXCELLENT,      // IAQ 0-50
    GOOD,           // IAQ 51-100
    LIGHTLY_POLLUTED, // IAQ 101-150
    MODERATELY_POLLUTED, // IAQ 151-200
    HEAVILY_POLLUTED,   // IAQ 201-300
    SEVERELY_POLLUTED   // IAQ 301+
}

fun getAirQualityLevel(iaq: Float): AirQualityLevel {
    return when {
        iaq <= 50 -> AirQualityLevel.EXCELLENT
        iaq <= 100 -> AirQualityLevel.GOOD
        iaq <= 150 -> AirQualityLevel.LIGHTLY_POLLUTED
        iaq <= 200 -> AirQualityLevel.MODERATELY_POLLUTED
        iaq <= 300 -> AirQualityLevel.HEAVILY_POLLUTED
        else -> AirQualityLevel.SEVERELY_POLLUTED
    }
}
