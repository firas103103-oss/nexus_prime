#!/usr/bin/env python3
"""
X-BIO Serial Lock Fix — Force-release COM/serial port and verify data flow.
Usage:
  python fix_serial_lock.py                    # Auto-detect port (COM4 on Windows, /dev/ttyUSB0 on Linux)
  python fix_serial_lock.py --port COM4        # Windows
  python fix_serial_lock.py --port /dev/ttyUSB0 # Linux
  python fix_serial_lock.py --port COM4 --baud 115200  # First Breath firmware
"""
import argparse
import os
import platform
import subprocess
import sys
import time

try:
    import serial
except ImportError:
    print("Install: pip install pyserial")
    sys.exit(1)


def kill_serial_processes_windows(port: str) -> list[int]:
    """Kill processes that commonly hold COM ports on Windows."""
    killed = []
    my_pid = os.getpid()
    targets = ["pio.exe", "platformio.exe", "python.exe", "putty.exe", "serial_monitor.exe"]
    try:
        out = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, timeout=10
        )
        if out.returncode != 0:
            return killed
        for line in out.stdout.splitlines():
            for t in targets:
                if t.lower() in line.lower():
                    parts = line.split(",")
                    if len(parts) >= 2:
                        try:
                            pid = int(parts[1].strip('"'))
                            if pid == my_pid:
                                continue
                            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, timeout=5)
                            killed.append(pid)
                            print(f"[KILL] PID {pid} ({t})")
                        except (ValueError, subprocess.TimeoutExpired):
                            pass
                    break
    except Exception as e:
        print(f"[WARN] taskkill scan: {e}")
    return killed


def kill_serial_processes_linux(port: str) -> list[int]:
    """Kill processes holding the serial port on Linux."""
    killed = []
    try:
        # fuser -k sends SIGKILL
        r = subprocess.run(
            ["fuser", "-k", port],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0:
            print(f"[KILL] fuser -k {port} — released")
    except FileNotFoundError:
        try:
            # lsof to find PIDs
            r = subprocess.run(
                ["lsof", "-t", port],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0 and r.stdout.strip():
                for pid in r.stdout.strip().split():
                    try:
                        subprocess.run(["kill", "-9", pid], capture_output=True, timeout=3)
                        killed.append(int(pid))
                        print(f"[KILL] PID {pid}")
                    except (ValueError, subprocess.TimeoutExpired):
                        pass
        except FileNotFoundError:
            pass
    except Exception as e:
        print(f"[WARN] fuser/lsof: {e}")
    return killed


def get_kill_command(port: str, pid: int) -> str:
    """Return exact command to kill the PID holding the port."""
    if platform.system() == "Windows":
        return f"taskkill /F /PID {pid}"
    return f"kill -9 {pid}"


def main():
    p = argparse.ArgumentParser(description="Fix serial lock and verify ESP32 data")
    p.add_argument("--port", default=None, help="Serial port (COM4 or /dev/ttyUSB0)")
    p.add_argument("--baud", type=int, default=115200, help="Baud rate (115200 First Breath, 921600 OMEGA)")
    p.add_argument("--duration", type=int, default=10, help="Seconds to capture raw bytes")
    args = p.parse_args()

    port = args.port
    if not port:
        port = "COM4" if platform.system() == "Windows" else "/dev/ttyUSB0"
        print(f"[INFO] Auto port: {port}")

    print(f"[INFO] Killing processes holding {port}...")
    if platform.system() == "Windows":
        kill_serial_processes_windows(port)
    else:
        kill_serial_processes_linux(port)

    time.sleep(1.5)

    print(f"[INFO] Opening {port} @ {args.baud} baud...")
    try:
        ser = serial.Serial(port, args.baud, timeout=0.1)
    except serial.SerialException as e:
        err = str(e).lower()
        if "permission" in err or "access" in err or "denied" in err:
            print("\n" + "=" * 60)
            print("PermissionError: Port is held by another process.")
            print("=" * 60)
            if platform.system() == "Windows":
                print("Run as Administrator, or kill the process manually:")
                print("  1. tasklist | findstr /i pio")
                print("  2. tasklist | findstr /i python")
                print("  3. taskkill /F /PID <PID>")
                print("\nOr close PlatformIO Monitor, Serial Monitor, PuTTY, etc.")
            else:
                print("Find and kill the process:")
                print(f"  fuser -k {port}")
                print(f"  # OR: lsof -t {port} | xargs kill -9")
                print("\nEnsure user is in 'dialout' group: sudo usermod -aG dialout $USER")
            print("=" * 60)
        else:
            print(f"[FAIL] {e}")
        sys.exit(1)

    print("[OK] Port opened. Capturing raw bytes for %d seconds..." % args.duration)
    print("-" * 60)

    start = time.time()
    total_bytes = 0
    lines = []

    while time.time() - start < args.duration:
        n = ser.in_waiting
        if n:
            chunk = ser.read(n)
            total_bytes += len(chunk)
            try:
                text = chunk.decode("utf-8", errors="replace")
                print(text, end="", flush=True)
                for line in text.splitlines():
                    line = line.strip()
                    if line and not line.startswith(">>>"):
                        lines.append(line)
            except Exception:
                print(chunk.hex(), end=" ", flush=True)
        else:
            time.sleep(0.05)

    ser.close()
    print("\n" + "-" * 60)
    print(f"[DONE] Total bytes: {total_bytes} in {args.duration}s")

    if total_bytes == 0:
        print("\n[WARN] NO DATA RECEIVED. Check:")
        print("  - ESP32 powered and connected")
        print("  - Correct port (COM4 vs COM3)")
        print("  - Baud rate (115200 for First Breath, 921600 for OMEGA)")
        print("  - Press ESP32 RESET button")
    else:
        print("\n[OK] ESP32 IS TALKING. JSON lines captured:")
        for i, ln in enumerate(lines[:10]):
            print(f"  {i+1}. {ln[:100]}{'...' if len(ln) > 100 else ''}")
        if len(lines) > 10:
            print(f"  ... and {len(lines) - 10} more")

    sys.exit(0 if total_bytes > 0 else 1)


if __name__ == "__main__":
    main()
