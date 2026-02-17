package com.bme688.sensorapp

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import com.google.android.material.floatingactionbutton.FloatingActionButton

class MainActivity : AppCompatActivity() {
    private lateinit var viewModel: SensorViewModel
    private lateinit var bluetoothAdapter: BluetoothAdapter
    private lateinit var recyclerView: RecyclerView
    private lateinit var scanButton: MaterialButton
    private lateinit var fabConnect: FloatingActionButton

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions.values.all { it }) {
            startBLEScan()
        } else {
            Log.e("MainActivity", "Permissions denied")
        }
    }

    private val enableBluetoothLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == RESULT_OK) {
            startBLEScan()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Set app brand title
        supportActionBar?.title = "X-Bio • Sensor Monitor"

        initializeComponents()
        setupViewModelObservers()
        requestPermissionsAndInitializeBLE()
    }

    private fun initializeComponents() {
        viewModel = ViewModelProvider(this).get(SensorViewModel::class.java)
        recyclerView = findViewById(R.id.deviceList)
        scanButton = findViewById(R.id.scanButton)
        fabConnect = findViewById(R.id.fabConnect)

        recyclerView.layoutManager = LinearLayoutManager(this)

        scanButton.setOnClickListener {
            requestPermissionsAndInitializeBLE()
        }

        fabConnect.setOnClickListener {
            val intent = Intent(this, DeviceDetailActivity::class.java)
            startActivity(intent)
        }
    }

    private fun setupViewModelObservers() {
        viewModel.isConnected.observe(this) { isConnected ->
            fabConnect.isEnabled = isConnected
            scanButton.text = if (isConnected) "Connected" else "Scan Devices"
        }

        viewModel.errorMessage.observe(this) { error ->
            Log.e("MainActivity", error)
        }
    }

    private fun requestPermissionsAndInitializeBLE() {
        val bluetoothManager = getSystemService(BluetoothManager::class.java)
        bluetoothAdapter = bluetoothManager.adapter

        if (!bluetoothAdapter.isEnabled) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            enableBluetoothLauncher.launch(enableBtIntent)
        } else {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val permissions = arrayOf(
                    Manifest.permission.BLUETOOTH_SCAN,
                    Manifest.permission.BLUETOOTH_CONNECT,
                    Manifest.permission.ACCESS_FINE_LOCATION
                )
                val missingPermissions = permissions.filter {
                    ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
                }.toTypedArray()

                if (missingPermissions.isNotEmpty()) {
                    permissionLauncher.launch(missingPermissions)
                } else {
                    startBLEScan()
                }
            } else {
                if (ContextCompat.checkSelfPermission(
                        this,
                        Manifest.permission.ACCESS_FINE_LOCATION
                    ) != PackageManager.PERMISSION_GRANTED
                ) {
                    permissionLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION))
                } else {
                    startBLEScan()
                }
            }
        }
    }

    private fun startBLEScan() {
        Log.d("MainActivity", "Starting BLE scan...")
        // Scan implementation here
    }

    override fun onDestroy() {
        super.onDestroy()
        viewModel.disconnect()
    }
}
