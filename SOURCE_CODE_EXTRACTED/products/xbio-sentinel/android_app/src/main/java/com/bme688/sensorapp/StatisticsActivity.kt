package com.bme688.sensorapp

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import kotlinx.coroutines.launch

class StatisticsActivity : AppCompatActivity() {

    private lateinit var database: OdorDatabase
    private lateinit var statsRecycler: RecyclerView
    private lateinit var totalOdorsText: TextView
    private lateinit var totalDetectionsText: TextView
    private lateinit var averageAccuracyText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_statistics)
        supportActionBar?.title = "X-Bio • الإحصائيات"

        database = OdorDatabase.getDatabase(this)
        initializeViews()
        loadStatistics()
    }

    private fun initializeViews() {
        statsRecycler = findViewById(R.id.statsRecycler)
        totalOdorsText = findViewById(R.id.totalOdorsText)
        totalDetectionsText = findViewById(R.id.totalDetectionsText)
        averageAccuracyText = findViewById(R.id.averageAccuracyText)

        statsRecycler.layoutManager = LinearLayoutManager(this)
    }

    private fun loadStatistics() {
        lifecycleScope.launch {
            val allOdors = database.odorDao().getAllOdors()
            val totalDetections = database.odorDao().getDetectionCount()

            totalOdorsText.text = "الروائح المدربة: ${allOdors.size}"
            totalDetectionsText.text = "عدد الاستكشافات: $totalDetections"

            // حساب دقة المتوسط
            if (totalDetections > 0) {
                val correctDetections = database.odorDao().getCorrectDetectionCount()
                val accuracy = (correctDetections.toFloat() / totalDetections * 100).toInt()
                averageAccuracyText.text = "الدقة: $accuracy%"
            }
        }
    }
}
