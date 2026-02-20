package com.bme688.sensorapp

data class OdorProfile(
    val id: Int,
    val name: String,
    val category: String,
    val avgTemp: Float,
    val avgHumidity: Float,
    val avgPressure: Float,
    val avgIaq: Float,
    val sampleCount: Int,
    val accuracy: Float
)
