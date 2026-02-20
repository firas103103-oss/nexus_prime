package com.bme688.sensorapp

import kotlin.math.sqrt
import kotlin.math.pow

class OdorMatcher {
    
    data class MatchResult(
        val odorId: Int,
        val odorName: String,
        val confidence: Float
    )
    
    fun findMatches(
        currentReadings: SensorReadings,
        allOdors: List<OdorProfile>
    ): List<MatchResult> {
        return allOdors.map { odor ->
            val confidence = calculateSimilarity(currentReadings, odor)
            MatchResult(
                odorId = odor.id,
                odorName = odor.name,
                confidence = (confidence * 100).coerceIn(0f, 100f)
            )
        }.sortByDescending { it.confidence }
    }
    
    private fun calculateSimilarity(
        current: SensorReadings,
        profile: OdorProfile
    ): Float {
        val tempDiff = (current.temperature - profile.avgTemp).pow(2)
        val humidDiff = (current.humidity - profile.avgHumidity).pow(2)
        val pressDiff = (current.pressure - profile.avgPressure).pow(2)
        val iaqDiff = (current.iaq - profile.avgIaq).pow(2)
        
        val distance = sqrt(tempDiff + humidDiff + pressDiff + iaqDiff)
        
        // تحويل المسافة إلى ثقة (كلما أقل المسافة أعلى الثقة)
        return 1.0f / (1.0f + distance)
    }
}

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
