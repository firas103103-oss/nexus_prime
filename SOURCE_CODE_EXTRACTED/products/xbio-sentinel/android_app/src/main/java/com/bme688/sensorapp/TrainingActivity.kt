package com.bme688.sensorapp

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class TrainingActivity : AppCompatActivity() {

    private lateinit var database: OdorDatabase
    private lateinit var odorNameInput: EditText
    private lateinit var categorySpinner: Spinner
    private lateinit var intensitySlider: SeekBar
    private lateinit var notesInput: EditText
    private lateinit var startButton: Button
    private lateinit var statusText: TextView
    private lateinit var progressBar: ProgressBar

    private val trainingDurationMs = 30_000L

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_training)
        supportActionBar?.title = "X-Bio • تدريب النظام"

        database = OdorDatabase.getDatabase(this)
        initViews()
        setupListeners()
    }

    private fun initViews() {
        odorNameInput = findViewById(R.id.odorNameInput)
        categorySpinner = findViewById(R.id.categorySpinner)
        intensitySlider = findViewById(R.id.intensitySlider)
        notesInput = findViewById(R.id.notesInput)
        startButton = findViewById(R.id.startTrainingButton)
        statusText = findViewById(R.id.statusText)
        progressBar = findViewById(R.id.trainingProgress)

        val categories = arrayOf("عطر", "طعام", "أزهار", "عشبي", "أخرى")
        categorySpinner.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, categories)
    }

    private fun setupListeners() {
        startButton.setOnClickListener { startTraining() }
    }

    private fun startTraining() {
        val odorName = odorNameInput.text.toString().trim()
        if (odorName.isEmpty()) {
            Toast.makeText(this, "أدخل اسم الرائحة", Toast.LENGTH_SHORT).show()
            return
        }

        startButton.isEnabled = false
        progressBar.progress = 0
        statusText.text = "جاري التدريب..."

        lifecycleScope.launch {
            val odorId = database.odorDao().insertOdor(
                OdorEntity(
                    name = odorName,
                    category = categorySpinner.selectedItem.toString(),
                    intensity = intensitySlider.progress,
                    sensorReading = 0f
                )
            ).toInt()

            // محاكاة جمع عينات كل 1.5 ثانية لمدة 30 ثانية
            val steps = 20
            repeat(steps) { step ->
                progressBar.progress = ((step + 1) * 100 / steps)
                statusText.text = "التدريب... ${progressBar.progress}%"

                val sample = TrainingSampleEntity(
                    odorId = odorId,
                    temperature = 25.5f,
                    humidity = 45.0f,
                    pressure = 1013.25f,
                    airQuality = 65.0f,
                    gasResistance = 50_000f,
                    duration = trainingDurationMs,
                    userNotes = notesInput.text.toString()
                )
                database.odorDao().insertTrainingSample(sample)
                delay(trainingDurationMs / steps)
            }

            statusText.text = "✅ تم بنجاح!"
            odorNameInput.text.clear()
            notesInput.text.clear()
            intensitySlider.progress = 5
            startButton.isEnabled = true
        }
    }
}
