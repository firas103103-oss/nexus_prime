package com.bme688.sensorapp

import androidx.room.*

@Dao
interface OdorDao {
    // Odor operations
    @Insert
    suspend fun insertOdor(odor: OdorEntity): Long
    
    @Update
    suspend fun updateOdor(odor: OdorEntity)
    
    @Delete
    suspend fun deleteOdor(odor: OdorEntity)
    
    @Query("SELECT * FROM odors ORDER BY created DESC")
    suspend fun getAllOdors(): List<OdorEntity>
    
    @Query("SELECT * FROM odors WHERE id = :odorId")
    suspend fun getOdorById(odorId: Int): OdorEntity?
    
    // Training samples
    @Insert
    suspend fun insertTrainingSample(sample: TrainingSampleEntity): Long
    
    @Query("SELECT * FROM training_samples WHERE odorId = :odorId")
    suspend fun getTrainingSamplesForOdor(odorId: Int): List<TrainingSampleEntity>
    
    @Query("SELECT AVG(temperature) FROM training_samples WHERE odorId = :odorId")
    suspend fun getAverageTemperature(odorId: Int): Float?
    
    @Query("SELECT AVG(humidity) FROM training_samples WHERE odorId = :odorId")
    suspend fun getAverageHumidity(odorId: Int): Float?
    
    @Query("SELECT AVG(pressure) FROM training_samples WHERE odorId = :odorId")
    suspend fun getAveragePressure(odorId: Int): Float?
    
    @Query("SELECT AVG(airQuality) FROM training_samples WHERE odorId = :odorId")
    suspend fun getAverageAirQuality(odorId: Int): Float?
    
    // Detection history
    @Insert
    suspend fun insertDetectionHistory(history: DetectionHistoryEntity): Long
    
    @Query("SELECT * FROM detection_history ORDER BY created DESC LIMIT 50")
    suspend fun getDetectionHistory(): List<DetectionHistoryEntity>
    
    @Query("SELECT COUNT(*) FROM detection_history WHERE isCorrect = 1")
    suspend fun getCorrectDetections(): Int
    
    @Query("SELECT COUNT(*) FROM detection_history")
    suspend fun getTotalDetections(): Int
    
    @Query("SELECT AVG(confidence) FROM detection_history WHERE detectedOdorId = :odorId")
    suspend fun getAverageConfidenceForOdor(odorId: Int): Float?
}
