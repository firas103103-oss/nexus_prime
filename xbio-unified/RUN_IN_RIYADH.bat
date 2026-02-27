@echo off
REM X-BIO Serial Bridge — Riyadh Station
REM Run this on Windows with ESP32 on COM4

echo [1] Force-killing pio, python, putty...
taskkill /F /IM pio.exe 2>nul
taskkill /F /IM platformio.exe 2>nul
taskkill /F /IM putty.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2] 10-second pulse verification on COM4 @ 115200...
python fix_serial_lock.py --port COM4 --baud 115200 --duration 10
if errorlevel 1 (
    echo [FAIL] No data. Check cable, press ESP32 RESET, then run again.
    pause
    exit /b 1
)

echo [3] Starting bridge to German server 46.224.225.96...
python serial_bridge.py --port COM4 --baud 115200 --url https://xbio.mrf103.com --mqtt-broker 46.224.225.96:1883 --both -v
pause
