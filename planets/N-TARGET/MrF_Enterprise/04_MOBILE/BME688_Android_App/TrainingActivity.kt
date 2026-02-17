package com.bme688.sensorapp

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
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
    
    private var trainingStartTime = 0L
    private val TRAINING_DURATION = 30000L // 30 ثانية
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_training)
        
        supportActionBar?.title = "X-Bio • تدريب النظام"
        
        database = OdorDatabase.getDatabase(this)
        initializeViews()
        setupListeners()
    }
    
    private fun initializeViews() {
        odorNameInput = findViewById(R.id.odorNameInput)
        categorySpinner = findViewById(R.id.categorySpinner)
        intensitySlider = findViewById(R.id.intensitySlider)
        notesInput = findViewById(R.id.notesInput)
        startButton = findViewById(R.id.startTrainingButton)
        statusText = findViewById(R.id.statusText)
        progressBar = findViewById(R.id.trainingProgress)
        
        setupCategorySpinner()
    }
    
    private fun setupCategorySpinner() {
        val categories = arrayOf("عطر", "طعام", "أزهار", "عشبي", "أخرى")
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, categories)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        categorySpinner.adapter = adapter
    }
    
    private fun setupListeners() {
        startButton.setOnClickListener {
            startTraining()
        }
    }
    
    private fun startTraining() {
        val odorName = odorNameInput.text.toString().trim()
        
        if (odorName.isEmpty()) {
            Toast.makeText(this, "الرجاء إدخال اسم الرائحة", Toast.LENGTH_SHORT).show()
            return
        }
        
        startButton.isEnabled = false
        statusText.text = "جاري التدريب..."
        progressBar.progress = 0
        trainingStartTime = System.currentTimeMillis()
        
        lifecycleScope.launch {
            // حفظ الرائحة الجديدة
            val odorEntity = OdorEntity(
                name = odorName,
                category = categorySpinner.selectedItem.toString(),
                intensity = intensitySlider.progress,
                sensorReading = 0f
            )
            
            val odorId = database.odorDao().insertOdor(odorEntity).toInt()
            
            // محاكاة التدريب
            simulateTraining(odorId)
        }
    }
    
    private suspend fun simulateTraining(odorId: Int) {
        for (i in 0..100 step 5) {
            progressBar.progress = i
            statusText.text = "جاري التدريب... ${i}%"
            
            val sample = TrainingSampleEntity(
                odorId = odorId,
                temperature = 25.5f + (i % 10) * 0.1f,
                humidity = 45.0f + (i % 8) * 0.5f,
                pressure = 1013.25f + (i % 5) * 0.2f,
                airQuality = 65.0f + (i % 10) * 1.0f,
                gasResistance = 50000f,
                duration = TRAINING_DURATION,
                userNotes = notesInput.text.toString()
            )
            
            database.odorDao().insertTrainingSample(sample)
            Thread.sleep(300)
        }
        
        progressBar.progress = 100
        statusText.text = "✅ تم التدريب بنجاح!"
        resetForm()
        startButton.isEnabled = true
    }
    
    private fun resetForm() {
        odorNameInput.text.clear()
        notesInput.text.clear()
        intensitySlider.progress = 5
        Toast.makeText(this, "تم حفظ الرائحة", Toast.LENGTH_SHORT).show()
    }
}
