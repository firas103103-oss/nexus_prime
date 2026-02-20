package com.bme688.sensorapp

import android.annotation.SuppressLint
import android.bluetooth.*
import android.content.Context
import android.os.Build
import android.util.Log
import kotlinx.coroutines.*
import java.util.*

class BLEManager(private val context: Context) {
    private val bluetoothAdapter: BluetoothAdapter? = BluetoothAdapter.getDefaultAdapter()
    private var bluetoothGatt: BluetoothGatt? = null
    private var gattCallback: BluetoothGattCallback? = null
    
    // UUIDs from ESP32 firmware
    private val SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    private val CHARACTERISTIC_UUID_TX = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
    private val CHARACTERISTIC_UUID_RX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    private val CLIENT_CHARACTERISTIC_CONFIG = "00002902-0000-1000-8000-00805f9b34fb"

    var onDataReceived: ((String) -> Unit)? = null
    var onConnectionStateChange: ((Boolean) -> Unit)? = null
    var onError: ((String) -> Unit)? = null

    @SuppressLint("MissingPermission")
    fun startScan(callback: (BluetoothDevice) -> Unit) {
        if (bluetoothAdapter?.isEnabled == true) {
            bluetoothAdapter?.startDiscovery()
        }
    }

    @SuppressLint("MissingPermission")
    fun connectToDevice(device: BluetoothDevice) {
        gattCallback = object : BluetoothGattCallback() {
            override fun onConnectionStateChange(gatt: BluetoothGatt?, status: Int, newState: Int) {
                if (newState == BluetoothProfile.STATE_CONNECTED) {
                    Log.d("BLE", "Connected to device: ${device.name}")
                    bluetoothGatt = gatt
                    gatt?.discoverServices()
                    onConnectionStateChange?.invoke(true)
                } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                    Log.d("BLE", "Disconnected from device")
                    onConnectionStateChange?.invoke(false)
                    disconnect()
                }
            }

            override fun onServicesDiscovered(gatt: BluetoothGatt?, status: Int) {
                if (status == BluetoothGatt.GATT_SUCCESS) {
                    setupNotifications()
                }
            }

            override fun onCharacteristicChanged(
                gatt: BluetoothGatt?,
                characteristic: BluetoothGattCharacteristic?
            ) {
                characteristic?.let {
                    val data = String(it.value, Charsets.UTF_8)
                    Log.d("BLE_DATA", "Received: $data")
                    onDataReceived?.invoke(data)
                }
            }

            override fun onCharacteristicWrite(
                gatt: BluetoothGatt?,
                characteristic: BluetoothGattCharacteristic?,
                status: Int
            ) {
                if (status == BluetoothGatt.GATT_SUCCESS) {
                    Log.d("BLE", "Command sent successfully")
                }
            }
        }

        bluetoothAdapter?.bluetoothLeScanner?.let {
            device.connectGatt(context, false, gattCallback)
        }
    }

    @SuppressLint("MissingPermission")
    private fun setupNotifications() {
        val service = bluetoothGatt?.getService(UUID.fromString(SERVICE_UUID))
        val characteristic = service?.getCharacteristic(UUID.fromString(CHARACTERISTIC_UUID_TX))

        if (characteristic != null) {
            bluetoothGatt?.setCharacteristicNotification(characteristic, true)
            val descriptor = characteristic.getDescriptor(UUID.fromString(CLIENT_CHARACTERISTIC_CONFIG))
            descriptor?.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            bluetoothGatt?.writeDescriptor(descriptor)
        }
    }

    @SuppressLint("MissingPermission")
    fun sendCommand(command: String) {
        val service = bluetoothGatt?.getService(UUID.fromString(SERVICE_UUID))
        val characteristic = service?.getCharacteristic(UUID.fromString(CHARACTERISTIC_UUID_RX))

        characteristic?.let {
            it.value = command.toByteArray(Charsets.UTF_8)
            bluetoothGatt?.writeCharacteristic(it)
        }
    }

    fun startStreaming(sensorNum: Int = 0, sampleRate: Int = 30, outputIds: IntArray = intArrayOf(4, 5, 6)) {
        val command = buildString {
            append("start $sensorNum $sampleRate")
            outputIds.forEach { append(" $it") }
        }
        sendCommand(command)
    }

    fun stopStreaming() {
        sendCommand("stop")
    }

    fun setLabel(label: Int) {
        sendCommand("setlabel $label")
    }

    fun getRTCTime() {
        sendCommand("getrtctime")
    }

    fun setRTCTime(timestamp: Long) {
        sendCommand("setrtctime $timestamp")
    }

    @SuppressLint("MissingPermission")
    fun disconnect() {
        bluetoothGatt?.disconnect()
        bluetoothGatt?.close()
        bluetoothGatt = null
    }

    fun isConnected(): Boolean = bluetoothGatt != null
}
