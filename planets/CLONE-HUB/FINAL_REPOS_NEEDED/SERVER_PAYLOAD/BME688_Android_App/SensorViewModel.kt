package com.bme688.sensorapp

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.google.gson.Gson
import kotlinx.coroutines.launch

class SensorViewModel(application: Application) : AndroidViewModel(application) {
    private val bleManager = BLEManager(application)
    private val gson = Gson()

    private val _currentReadings = MutableLiveData<SensorReadings>()
    val currentReadings: LiveData<SensorReadings> = _currentReadings

    private val _sensorHistory = MutableLiveData<List<SensorReadings>>(emptyList())
    val sensorHistory: LiveData<List<SensorReadings>> = _sensorHistory

    private val _isConnected = MutableLiveData<Boolean>(false)
    val isConnected: LiveData<Boolean> = _isConnected

    private val _isStreaming = MutableLiveData<Boolean>(false)
    val isStreaming: LiveData<Boolean> = _isStreaming

    private val _stats = MutableLiveData<SensorStats>()
    val stats: LiveData<SensorStats> = _stats

    private val _errorMessage = MutableLiveData<String>()
    val errorMessage: LiveData<String> = _errorMessage

    init {
        setupBLECallbacks()
    }

    private fun setupBLECallbacks() {
        bleManager.onDataReceived = { data ->
            viewModelScope.launch {
                parseAndUpdateData(data)
            }
        }

        bleManager.onConnectionStateChange = { connected ->
            _isConnected.postValue(connected)
            if (!connected) {
                _isStreaming.postValue(false)
            }
        }

        bleManager.onError = { error ->
            _errorMessage.postValue(error)
        }
    }

    private fun parseAndUpdateData(jsonData: String) {
        try {
            val readings = gson.fromJson(jsonData, SensorReadings::class.java)
            _currentReadings.postValue(readings)

            // Update history
            val history = _sensorHistory.value?.toMutableList() ?: mutableListOf()
            history.add(readings)
            
            // Keep last 100 readings
            if (history.size > 100) {
                history.removeAt(0)
            }
            _sensorHistory.postValue(history)

            // Calculate stats
            updateStats(history)
        } catch (e: Exception) {
            Log.e("SensorViewModel", "Error parsing sensor data: ${e.message}")
            _errorMessage.postValue("Error parsing sensor data: ${e.message}")
        }
    }

    private fun updateStats(history: List<SensorReadings>) {
        if (history.isEmpty()) return

        val temps = history.map { it.temperature }
        val humidities = history.map { it.humidity }
        val pressures = history.map { it.pressure }

        val stats = SensorStats(
            minTemp = temps.minOrNull() ?: 0f,
            maxTemp = temps.maxOrNull() ?: 0f,
            avgTemp = temps.average().toFloat(),
            minHumidity = humidities.minOrNull() ?: 0f,
            maxHumidity = humidities.maxOrNull() ?: 0f,
            avgHumidity = humidities.average().toFloat(),
            minPressure = pressures.minOrNull() ?: 0f,
            maxPressure = pressures.maxOrNull() ?: 0f,
            avgPressure = pressures.average().toFloat()
        )

        _stats.postValue(stats)
    }

    fun connectToDevice(deviceAddress: String) {
        // Implementation depends on how device is selected
    }

    fun startStreaming() {
        if (_isConnected.value == true) {
            bleManager.startStreaming()
            _isStreaming.postValue(true)
        }
    }

    fun stopStreaming() {
        bleManager.stopStreaming()
        _isStreaming.postValue(false)
    }

    fun setLabel(label: Int) {
        bleManager.setLabel(label)
    }

    fun disconnect() {
        stopStreaming()
        bleManager.disconnect()
        _isConnected.postValue(false)
        _sensorHistory.postValue(emptyList())
    }

    override fun onCleared() {
        super.onCleared()
        disconnect()
    }
}
