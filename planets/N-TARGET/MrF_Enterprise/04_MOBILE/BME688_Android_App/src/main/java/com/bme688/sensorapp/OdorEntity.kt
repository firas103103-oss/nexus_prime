package com.bme688.sensorapp

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "odors")
data class OdorEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "name")
    val name: String,
    
    @ColumnInfo(name = "category")
    val category: String,
    
    @ColumnInfo(name = "intensity")
    val intensity: Int,
    
    @ColumnInfo(name = "sensor_reading")
    val sensorReading: Float,
    
    @ColumnInfo(name = "created")
    val created: Long = System.currentTimeMillis()
)
