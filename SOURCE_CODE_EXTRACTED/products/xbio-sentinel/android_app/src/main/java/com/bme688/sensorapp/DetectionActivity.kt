package com.bme688.sensorapp

import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

class DetectionActivity : AppCompatActivity() {

    private lateinit var database: OdorDatabase
    private lateinit var matcher: OdorMatcher
    private lateinit var scanButton: Button
    private lateinit var resultsContainer: LinearLayout
    private lateinit var confirmButton: Button
    private var lastResult: OdorMatcher.MatchResult? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detection)
        supportActionBar?.title = "X-Bio • الاستكشاف"

        database = OdorDatabase.getDatabase(this)
        matcher = OdorMatcher()
        initViews()
        setupListeners()
    }

    private fun initViews() {
        scanButton = findViewById(R.id.scanButton)
        resultsContainer = findViewById(R.id.resultsContainer)
        confirmButton = findViewById(R.id.confirmButton)
        confirmButton.visibility = Button.GONE
    }

    private fun setupListeners() {
        scanButton.setOnClickListener { startDetection() }
        confirmButton.setOnClickListener { confirmDetection() }
    }

    private fun startDetection() {
        resultsContainer.removeAllViews()
        confirmButton.visibility = Button.GONE

        lifecycleScope.launch {
            val allOdors = database.odorDao().getAllOdors()
            if (allOdors.isEmpty()) {
                Toast.makeText(this@DetectionActivity, "لا توجد روائح مدربة", Toast.LENGTH_SHORT).show()
                return@launch
            }

            val profiles = allOdors.map { odor ->
                OdorProfile(
                    id = odor.id,
                    name = odor.name,
                    category = odor.category,
                    avgTemp = database.odorDao().getAverageTemperature(odor.id) ?: 25f,
                    avgHumidity = database.odorDao().getAverageHumidity(odor.id) ?: 45f,
                    avgPressure = database.odorDao().getAveragePressure(odor.id) ?: 1013f,
                    avgIaq = database.odorDao().getAverageAirQuality(odor.id) ?: 65f,
                    sampleCount = database.odorDao().getTrainingSamplesForOdor(odor.id).size,
                    accuracy = 0f
                )
            }

            // استبدل هذه القراءة بالبيانات الحقيقية القادمة من الحساس عبر BLE
            val currentReading = SensorReadings(
                temperature = 25.3f,
                humidity = 46.0f,
                pressure = 1013.5f,
                airQuality = 64.0f,
                iaq = 50f
            )

            val matches = matcher.findMatches(currentReading, profiles)
            displayResults(matches)
            lastResult = matches.firstOrNull()
        }
    }

    private fun displayResults(matches: List<OdorMatcher.MatchResult>) {
        confirmButton.visibility = Button.VISIBLE

        matches.take(3).forEach { match ->
            val resultView = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
                setPadding(16, 16, 16, 16)
            }

            resultView.addView(TextView(this).apply {
                text = match.odorName
                textSize = 16f
                setTypeface(null, android.graphics.Typeface.BOLD)
            })

            resultView.addView(TextView(this).apply {
                text = "الثقة: ${String.format("%.1f", match.confidence)}%"
                textSize = 14f
            })

            resultsContainer.addView(resultView)
        }
    }

    private fun confirmDetection() {
        lastResult?.let { result ->
            lifecycleScope.launch {
                val history = DetectionHistoryEntity(
                    detectedOdorId = result.odorId,
                    confidence = result.confidence,
                    isCorrect = true,
                    temperature = 25.3f,
                    humidity = 46.0f,
                    pressure = 1013.5f,
                    airQuality = 64.0f
                )
                database.odorDao().insertDetectionHistory(history)
                Toast.makeText(this@DetectionActivity, "✅ تم الحفظ", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
