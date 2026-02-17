package com.bme688.sensorapp

import android.graphics.Color
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.google.android.material.button.MaterialButton
import com.google.android.material.card.MaterialCardView

class DeviceDetailActivity : AppCompatActivity() {
    private lateinit var viewModel: SensorViewModel

    // UI Components
    private lateinit var tempValue: TextView
    private lateinit var humidityValue: TextView
    private lateinit var pressureValue: TextView
    private lateinit var iaqValue: TextView
    private lateinit var airQualityStatus: TextView

    private lateinit var tempChart: LineChart
    private lateinit var humidityChart: LineChart
    private lateinit var pressureChart: LineChart

    private lateinit var startButton: MaterialButton
    private lateinit var stopButton: MaterialButton
    private lateinit var statsCard: MaterialCardView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_device_detail)

        // Set app brand title
        supportActionBar?.title = "X-Bio • Live Data"

        initializeComponents()
        setupViewModelObservers()
        setupCharts()
    }

    private fun initializeComponents() {
        viewModel = ViewModelProvider(this).get(SensorViewModel::class.java)

        tempValue = findViewById(R.id.tempValue)
        humidityValue = findViewById(R.id.humidityValue)
        pressureValue = findViewById(R.id.pressureValue)
        iaqValue = findViewById(R.id.iaqValue)
        airQualityStatus = findViewById(R.id.airQualityStatus)

        tempChart = findViewById(R.id.tempChart)
        humidityChart = findViewById(R.id.humidityChart)
        pressureChart = findViewById(R.id.pressureChart)

        startButton = findViewById(R.id.startButton)
        stopButton = findViewById(R.id.stopButton)
        statsCard = findViewById(R.id.statsCard)

        startButton.setOnClickListener { viewModel.startStreaming() }
        stopButton.setOnClickListener { viewModel.stopStreaming() }
    }

    private fun setupViewModelObservers() {
        viewModel.currentReadings.observe(this) { readings ->
            updateReadingsUI(readings)
        }

        viewModel.sensorHistory.observe(this) { history ->
            updateCharts(history)
        }

        viewModel.stats.observe(this) { stats ->
            updateStatsUI(stats)
        }

        viewModel.isStreaming.observe(this) { isStreaming ->
            startButton.isEnabled = !isStreaming
            stopButton.isEnabled = isStreaming
        }
    }

    private fun updateReadingsUI(readings: SensorReadings) {
        tempValue.text = String.format("%.2f°C", readings.temperature)
        humidityValue.text = String.format("%.2f%%", readings.humidity)
        pressureValue.text = String.format("%.2f hPa", readings.pressure)
        iaqValue.text = String.format("%.1f", readings.iaq)

        val airQualityLevel = getAirQualityLevel(readings.iaq)
        airQualityStatus.text = when (airQualityLevel) {
            AirQualityLevel.EXCELLENT -> "Excellent"
            AirQualityLevel.GOOD -> "Good"
            AirQualityLevel.LIGHTLY_POLLUTED -> "Lightly Polluted"
            AirQualityLevel.MODERATELY_POLLUTED -> "Moderately Polluted"
            AirQualityLevel.HEAVILY_POLLUTED -> "Heavily Polluted"
            AirQualityLevel.SEVERELY_POLLUTED -> "Severely Polluted"
        }

        airQualityStatus.setTextColor(when (airQualityLevel) {
            AirQualityLevel.EXCELLENT -> Color.GREEN
            AirQualityLevel.GOOD -> Color.parseColor("#90EE90")
            AirQualityLevel.LIGHTLY_POLLUTED -> Color.YELLOW
            AirQualityLevel.MODERATELY_POLLUTED -> Color.parseColor("#FF8C00")
            AirQualityLevel.HEAVILY_POLLUTED -> Color.RED
            AirQualityLevel.SEVERELY_POLLUTED -> Color.parseColor("#8B0000")
        })
    }

    private fun updateStatsUI(stats: SensorStats) {
        // Display stats in the stats card
        val statsText = StringBuilder()
        statsText.append("Temperature: ${String.format("%.2f", stats.minTemp)} - ${String.format("%.2f", stats.maxTemp)}°C (Avg: ${String.format("%.2f", stats.avgTemp)}°C)\n")
        statsText.append("Humidity: ${String.format("%.2f", stats.minHumidity)} - ${String.format("%.2f", stats.maxHumidity)}%% (Avg: ${String.format("%.2f", stats.avgHumidity)}%%)\n")
        statsText.append("Pressure: ${String.format("%.2f", stats.minPressure)} - ${String.format("%.2f", stats.maxPressure)} hPa (Avg: ${String.format("%.2f", stats.avgPressure)} hPa)")
    }

    private fun setupCharts() {
        setupChart(tempChart, "Temperature (°C)")
        setupChart(humidityChart, "Humidity (%)")
        setupChart(pressureChart, "Pressure (hPa)")
    }

    private fun setupChart(chart: LineChart, label: String) {
        chart.description.isEnabled = false
        chart.setTouchEnabled(true)
        chart.isDragEnabled = true
        chart.isScaleXEnabled = true
        chart.isScaleYEnabled = true
        chart.xAxis.setDrawGridLines(true)
        chart.axisLeft.setDrawGridLines(true)
        chart.axisRight.isEnabled = false
    }

    private fun updateCharts(history: List<SensorReadings>) {
        if (history.isEmpty()) return

        // Update temperature chart
        val tempEntries = history.mapIndexed { index, reading ->
            Entry(index.toFloat(), reading.temperature)
        }
        updateChart(tempChart, tempEntries, "Temperature", Color.RED)

        // Update humidity chart
        val humidityEntries = history.mapIndexed { index, reading ->
            Entry(index.toFloat(), reading.humidity)
        }
        updateChart(humidityChart, humidityEntries, "Humidity", Color.BLUE)

        // Update pressure chart
        val pressureEntries = history.mapIndexed { index, reading ->
            Entry(index.toFloat(), reading.pressure)
        }
        updateChart(pressureChart, pressureEntries, "Pressure", Color.GREEN)
    }

    private fun updateChart(chart: LineChart, entries: List<Entry>, label: String, color: Int) {
        val dataSet = LineDataSet(entries, label)
        dataSet.color = color
        dataSet.setCircleColor(color)
        dataSet.lineWidth = 2f
        dataSet.circleRadius = 3f
        dataSet.setDrawValues(false)

        val lineData = LineData(dataSet)
        chart.data = lineData
        chart.invalidate()
    }

    override fun onDestroy() {
        super.onDestroy()
        viewModel.stopStreaming()
    }
}
