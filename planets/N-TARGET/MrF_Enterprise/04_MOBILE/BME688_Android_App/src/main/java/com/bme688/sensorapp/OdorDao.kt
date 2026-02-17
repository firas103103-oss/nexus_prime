package com.bme688.sensorapp

import androidx.room.*

@Dao
interface OdorDao {

    // ===== CRUD Operations =====
    
    @Insert
    suspend fun insertOdor(odor: OdorEntity): Long

    @Insert
    suspend fun insertTrainingSample(sample: TrainingSampleEntity): Long

    @Insert
    suspend fun insertDetectionHistory(history: DetectionHistoryEntity): Long

    @Update
    suspend fun updateOdor(odor: OdorEntity)

    @Delete
    suspend fun deleteOdor(odor: OdorEntity)

    // ===== Query Operations =====

    @Query("SELECT * FROM odors")
    suspend fun getAllOdors(): List<OdorEntity>

    @Query("SELECT * FROM odors WHERE id = :odorId")
    suspend fun getOdorById(odorId: Int): OdorEntity?

    @Query("SELECT * FROM training_samples WHERE odor_id = :odorId")
    suspend fun getTrainingSamplesForOdor(odorId: Int): List<TrainingSampleEntity>

    @Query("SELECT * FROM detection_history WHERE detected_odor_id = :odorId")
    suspend fun getDetectionHistoryForOdor(odorId: Int): List<DetectionHistoryEntity>

    // ===== Statistics Queries =====

    @Query("SELECT AVG(temperature) FROM training_samples WHERE odor_id = :odorId")
    suspend fun getAverageTemperature(odorId: Int): Float?

    @Query("SELECT AVG(humidity) FROM training_samples WHERE odor_id = :odorId")
    suspend fun getAverageHumidity(odorId: Int): Float?

    @Query("SELECT AVG(pressure) FROM training_samples WHERE odor_id = :odorId")
    suspend fun getAveragePressure(odorId: Int): Float?

    @Query("SELECT AVG(air_quality) FROM training_samples WHERE odor_id = :odorId")
    suspend fun getAverageAirQuality(odorId: Int): Float?

    @Query("SELECT COUNT(*) FROM detection_history")
    suspend fun getDetectionCount(): Int

    @Query("SELECT COUNT(*) FROM detection_history WHERE is_correct = 1")
    suspend fun getCorrectDetectionCount(): Int

    @Query("SELECT AVG(confidence) FROM detection_history WHERE detected_odor_id = :odorId")
    suspend fun getAverageConfidenceForOdor(odorId: Int): Float?

    // ===== Aggregation Queries =====

    @Query("""
        SELECT 
            o.id,
            o.name,
            o.category,
            COUNT(ts.id) as sample_count,
            AVG(ts.temperature) as avg_temp,
            AVG(ts.humidity) as avg_humidity,
            AVG(ts.pressure) as avg_pressure,
            AVG(ts.air_quality) as avg_air_quality
        FROM odors o
        LEFT JOIN training_samples ts ON o.id = ts.odor_id
        GROUP BY o.id
    """)
    suspend fun getOdorsWithStatistics(): List<OdorStatistic>

    @Query("SELECT * FROM detection_history ORDER BY timestamp DESC LIMIT :limit")
    suspend fun getRecentDetections(limit: Int = 10): List<DetectionHistoryEntity>

    // ===== Cleanup Queries =====

    @Query("DELETE FROM detection_history WHERE detected_odor_id = :odorId")
    suspend fun deleteDetectionHistoryForOdor(odorId: Int)

    @Query("DELETE FROM training_samples WHERE odor_id = :odorId")
    suspend fun deleteTrainingSamplesForOdor(odorId: Int)
}

// Data class for statistics query results
data class OdorStatistic(
    val id: Int,
    val name: String,
    val category: String,
    val sample_count: Int,
    val avg_temp: Float?,
    val avg_humidity: Float?,
    val avg_pressure: Float?,
    val avg_air_quality: Float?
)
