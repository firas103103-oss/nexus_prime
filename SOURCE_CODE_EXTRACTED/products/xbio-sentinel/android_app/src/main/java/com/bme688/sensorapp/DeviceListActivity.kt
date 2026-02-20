package com.bme688.sensorapp

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton

class DeviceListActivity : AppCompatActivity() {

    private lateinit var bluetoothAdapter: BluetoothAdapter
    private val bleScanner by lazy { bluetoothAdapter.bluetoothLeScanner }
    private var isScanning = false
    private val handler = Handler(Looper.getMainLooper())

    private lateinit var recyclerView: RecyclerView
    private lateinit var statusText: TextView
    private lateinit var scanButton: MaterialButton

    private val deviceList = mutableListOf<BluetoothDevice>()
    private lateinit var deviceAdapter: DeviceAdapter

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            val device = result.device
            if (device.name != null && !deviceList.any { it.address == device.address }) {
                deviceList.add(device)
                deviceAdapter.notifyItemInserted(deviceList.size - 1)
            }
        }
    }

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions.values.all { it }) {
            startBleScan()
        } else {
            Toast.makeText(this, "Permissions denied", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_device_list)

        initializeComponents()
        setupBluetooth()
    }

    private fun initializeComponents() {
        recyclerView = findViewById(R.id.deviceList)
        statusText = findViewById(R.id.statusText)
        scanButton = findViewById(R.id.scanButton)

        deviceAdapter = DeviceAdapter(deviceList) { device ->
            onDeviceSelected(device)
        }

        recyclerView.apply {
            layoutManager = LinearLayoutManager(this@DeviceListActivity)
            adapter = deviceAdapter
        }

        scanButton.setOnClickListener {
            if (isScanning) {
                stopBleScan()
            } else {
                requestPermissionsAndScan()
            }
        }
    }

    private fun setupBluetooth() {
        val bluetoothManager = getSystemService(BluetoothManager::class.java)
        bluetoothAdapter = bluetoothManager.adapter

        if (!bluetoothAdapter.isEnabled) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            startActivity(enableBtIntent)
        }
    }

    private fun requestPermissionsAndScan() {
        val requiredPermissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            arrayOf(
                Manifest.permission.BLUETOOTH_SCAN,
                Manifest.permission.BLUETOOTH_CONNECT,
                Manifest.permission.ACCESS_FINE_LOCATION
            )
        } else {
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
        }

        val missingPermissions = requiredPermissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }.toTypedArray()

        if (missingPermissions.isNotEmpty()) {
            permissionLauncher.launch(missingPermissions)
        } else {
            startBleScan()
        }
    }

    private fun startBleScan() {
        deviceList.clear()
        deviceAdapter.notifyDataSetChanged()

        bleScanner.startScan(scanCallback)
        isScanning = true
        statusText.text = "Scanning for BLE devices..."
        scanButton.text = "Stop Scan"

        // Stop scan after a set period.
        handler.postDelayed({
            stopBleScan()
        }, SCAN_PERIOD)
    }

    private fun stopBleScan() {
        bleScanner.stopScan(scanCallback)
        isScanning = false
        statusText.text = "Scan complete"
        scanButton.text = "Scan Again"
    }

    private fun onDeviceSelected(device: BluetoothDevice) {
        stopBleScan() // Stop scanning when a device is selected
        val intent = Intent(this, DeviceDetailActivity::class.java)
        intent.putExtra("device", device)
        startActivity(intent)
    }

    override fun onPause() {
        super.onPause()
        if (isScanning) {
            stopBleScan()
        }
    }

    companion object {
        private const val SCAN_PERIOD: Long = 10000 // Stops scanning after 10 seconds.
    }
}
