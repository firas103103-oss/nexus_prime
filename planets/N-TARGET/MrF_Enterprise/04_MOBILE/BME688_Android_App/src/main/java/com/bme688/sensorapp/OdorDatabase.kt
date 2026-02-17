package com.bme688.sensorapp

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [OdorEntity::class, TrainingSampleEntity::class, DetectionHistoryEntity::class],
    version = 1,
    exportSchema = false
)
abstract class OdorDatabase : RoomDatabase() {
    
    abstract fun odorDao(): OdorDao

    companion object {
        @Volatile
        private var instance: OdorDatabase? = null

        fun getDatabase(context: Context): OdorDatabase {
            return instance ?: synchronized(this) {
                val db = Room.databaseBuilder(
                    context.applicationContext,
                    OdorDatabase::class.java,
                    "odor_database"
                )
                    .fallbackToDestructiveMigration()
                    .build()
                instance = db
                db
            }
        }
    }
}
