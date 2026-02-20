package com.bme688.sensorapp

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "detection_history",
    foreignKeys = [
        ForeignKey(
            entity = OdorEntity::class,
            parentColumns = ["id"],
            childColumns = ["detected_odor_id"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class DetectionHistoryEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "detected_odor_id")
    val detectedOdorId: Int,
    
    @ColumnInfo(name = "confidence")
    val confidence: Float,
    
    @ColumnInfo(name = "is_correct")
    val isCorrect: Boolean = false,
    
    @ColumnInfo(name = "user_correction")
    val userCorrection: String? = null,
    
    @ColumnInfo(name = "temperature")
    val temperature: Float,
    
    @ColumnInfo(name = "humidity")
    val humidity: Float,
    
    @ColumnInfo(name = "pressure")
    val pressure: Float,
    
    @ColumnInfo(name = "air_quality")
    val airQuality: Float,
    
    @ColumnInfo(name = "timestamp")
    val timestamp: Long = System.currentTimeMillis()
)
