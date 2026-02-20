package com.bme688.sensorapp

import kotlin.math.pow
import kotlin.math.sqrt

class OdorMatcher {
    
    fun findMatches(
        currentReading: SensorReadings,
        profiles: List<OdorProfile>
    ): List<MatchResult> {
        return profiles
            .map { profile ->
                val similarity = calculateSimilarity(currentReading, profile)
                MatchResult(
                    odorId = profile.id,
                    odorName = profile.name,
                    category = profile.category,
                    confidence = similarity,
                    sampleCount = profile.sampleCount
                )
            }
            .sortedByDescending { it.confidence }
    }

    private fun calculateSimilarity(
        current: SensorReadings,
        profile: OdorProfile
    ): Float {
        // Euclidean Distance Calculation
        val tempDiff = (current.temperature - profile.avgTemp).pow(2)
        val humidDiff = (current.humidity - profile.avgHumidity).pow(2)
        val pressDiff = (current.pressure - profile.avgPressure).pow(2)
        val iaqDiff = (current.iaq - profile.avgIaq).pow(2)

        val distance = sqrt(tempDiff + humidDiff + pressDiff + iaqDiff)
        
        // Convert distance to confidence score (0-100%)
        return (100 / (1.0f + distance)).coerceIn(0f, 100f)
    }

    data class MatchResult(
        val odorId: Int,
        val odorName: String,
        val category: String,
        val confidence: Float,
        val sampleCount: Int
    )
}
