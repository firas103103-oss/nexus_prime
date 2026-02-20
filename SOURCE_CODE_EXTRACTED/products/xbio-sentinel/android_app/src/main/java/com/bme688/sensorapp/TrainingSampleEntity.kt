package com.bme688.sensorapp

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "training_samples",
    foreignKeys = [
        ForeignKey(
            entity = OdorEntity::class,
            parentColumns = ["id"],
            childColumns = ["odor_id"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class TrainingSampleEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "odor_id")
    val odorId: Int,
    
    @ColumnInfo(name = "temperature")
    val temperature: Float,
    
    @ColumnInfo(name = "humidity")
    val humidity: Float,
    
    @ColumnInfo(name = "pressure")
    val pressure: Float,
    
    @ColumnInfo(name = "air_quality")
    val airQuality: Float,
    
    @ColumnInfo(name = "gas_resistance")
    val gasResistance: Float,
    
    @ColumnInfo(name = "duration")
    val duration: Long,
    
    @ColumnInfo(name = "user_notes")
    val userNotes: String = "",
    
    @ColumnInfo(name = "timestamp")
    val timestamp: Long = System.currentTimeMillis()
)
