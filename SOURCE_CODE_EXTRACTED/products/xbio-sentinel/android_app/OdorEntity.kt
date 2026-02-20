package com.bme688.sensorapp

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "odors")
data class OdorEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val name: String,
    val category: String,
    val intensity: Int,
    val sensorReading: Float,
    val created: Long = System.currentTimeMillis()
)
