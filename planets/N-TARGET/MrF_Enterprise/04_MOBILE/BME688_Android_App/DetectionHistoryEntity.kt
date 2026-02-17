package com.bme688.sensorapp

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "detection_history",
    foreignKeys = [
        ForeignKey(
            entity = OdorEntity::class,
            parentColumns = ["id"],
            childColumns = ["detectedOdorId"]
        )
    ]
)
data class DetectionHistoryEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val detectedOdorId: Int,
    val confidence: Float,
    val isCorrect: Boolean = false,
    val userCorrection: String? = null,
    val temperature: Float,
    val humidity: Float,
    val pressure: Float,
    val airQuality: Float,
    val created: Long = System.currentTimeMillis()
)
