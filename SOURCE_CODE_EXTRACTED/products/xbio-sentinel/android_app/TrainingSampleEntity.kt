package com.bme688.sensorapp

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(
    tableName = "training_samples",
    foreignKeys = [
        ForeignKey(
            entity = OdorEntity::class,
            parentColumns = ["id"],
            childColumns = ["odorId"]
        )
    ]
)
data class TrainingSampleEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val odorId: Int,
    val temperature: Float,
    val humidity: Float,
    val pressure: Float,
    val airQuality: Float,
    val gasResistance: Float,
    val duration: Long,
    val userNotes: String = "",
    val created: Long = System.currentTimeMillis()
)
