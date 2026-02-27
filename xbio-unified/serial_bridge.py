#!/usr/bin/env python3
"""
X-BIO Unified Serial Bridge V2 — Production
Operation Unified Bridge: Serial → HTTP + MQTT with Rotating Logs.
Supports: OMEGA (v/gadget,tag,sri,msi,spi,truth), First Breath (node_id,temp,gas,anomaly), Standard Ingest.
Usage:
  python serial_bridge.py --port /dev/ttyUSB0 --url https://xbio.mrf103.com
  python serial_bridge.py --port /dev/ttyUSB0 --mqtt --mqtt-broker localhost:1883
  python serial_bridge.py --port /dev/ttyUSB0 --both
"""
import argparse
import json
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

try:
    import serial
    import requests
except ImportError:
    print("Install: pip install pyserial requests")
    sys.exit(1)

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "bridge.log")
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5MB
LOG_BACKUP_COUNT = 5


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure RotatingFileHandler for production logging."""
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger("xbio_bridge")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    fh = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(ch)
    return logger


def _is_omega(data: dict) -> bool:
    """Detect OMEGA format (v, gadget, or tag with OMEGA)."""
    v = data.get("v") or data.get("gadget") or ""
    return str(v).upper().startswith("OMEGA")


def build_ingest_payload(data: dict, device_id: str) -> dict | None:
    """Build /api/ingest payload from various JSON formats."""
    if _is_omega(data):
        return {
            "device_id": data.get("device_id", device_id),
            "v": data.get("v") or data.get("gadget"),
            "s": data.get("s") or data.get("tag"),
            "sri": data.get("sri"),
            "msi": data.get("msi"),
            "spi": data.get("spi"),
            "truth": data.get("truth"),
            "alert": data.get("alert"),
            "ts": data.get("ts", int(time.time())),
        }
    if "node_id" in data and "temp" in data and "gas" in data:
        return {
            "device_id": data.get("node_id", device_id),
            "temp": data.get("temp"),
            "humidity": None,
            "pressure": None,
            "gas": data.get("gas"),
            "iaq": None,
            "voc": None,
            "ts": data.get("ts", int(time.time() * 1000)),
        }
    if "device_id" in data or "temp" in data:
        return {
            "device_id": data.get("device_id", device_id),
            "temp": data.get("temp"),
            "humidity": data.get("humidity"),
            "pressure": data.get("pressure"),
            "gas": data.get("gas"),
            "iaq": data.get("iaq"),
            "voc": data.get("voc"),
            "ts": data.get("ts", int(time.time() * 1000)),
        }
    return None


def to_mqtt_payload(data: dict, device_id: str) -> dict | None:
    """Map to iot_service SensorReading schema for xbio/{device_id}/data."""
    ts = int(time.time() * 1000)
    if _is_omega(data):
        truth = float(data.get("truth", 0) or 0)
        s = data.get("s") or data.get("tag") or "VOID_STABLE"
        return {
            "sensors": {
                "temperature": 22.0,
                "humidity": 50.0,
                "pressure": 1013.0,
                "gas_resistance": int(truth * 1000) if truth else 100000,
                "iaq": truth,
                "iaq_accuracy": 3,
                "co2_equivalent": 0,
                "voc_equivalent": 0,
            },
            "status": {
                "s": s,
                "sri": data.get("sri"),
                "msi": data.get("msi"),
                "spi": data.get("spi"),
                "truth": truth,
                "alert": data.get("alert"),
            },
            "ts": data.get("ts", ts),
        }
    if "node_id" in data and "temp" in data and "gas" in data:
        temp = float(data.get("temp", 22))
        gas = int(data.get("gas", 100000))
        anomaly = bool(data.get("anomaly", False))
        return {
            "sensors": {
                "temperature": temp,
                "humidity": 0,
                "pressure": 1013.0,
                "gas_resistance": gas,
                "iaq": 50.0 if anomaly else 100.0,
                "iaq_accuracy": 2,
                "co2_equivalent": 0,
                "voc_equivalent": 0,
            },
            "status": {"anomaly": anomaly},
            "ts": data.get("ts", ts),
        }
    if "device_id" in data or "temp" in data:
        return {
            "sensors": {
                "temperature": float(data.get("temp", 0) or 0),
                "humidity": float(data.get("humidity", 0) or 0),
                "pressure": float(data.get("pressure", 0) or 1013),
                "gas_resistance": int(data.get("gas", 0) or 100000),
                "iaq": float(data.get("iaq", 0) or 0),
                "iaq_accuracy": 0,
                "co2_equivalent": 0,
                "voc_equivalent": 0,
            },
            "ts": data.get("ts", ts),
        }
    return None


def get_device_id(data: dict, fallback: str) -> str:
    return data.get("device_id") or data.get("node_id") or fallback


def main():
    p = argparse.ArgumentParser(description="X-BIO Unified Serial Bridge V2")
    p.add_argument("--port", default="/dev/ttyUSB0", help="Serial port")
    p.add_argument("--url", default="https://xbio.mrf103.com", help="Ingest API base URL")
    p.add_argument("--baud", type=int, default=115200, help="Baud rate (115200 First Breath, 921600 OMEGA)")
    p.add_argument("--device-id", default="XBIO_S3_01", help="Device ID fallback (XBIO_S3_01 for First Breath)")
    p.add_argument("--dry-run", action="store_true", help="Print payloads, do not send")
    p.add_argument("--mqtt", action="store_true", help="Publish to MQTT (xbio/{id}/data)")
    p.add_argument("--mqtt-broker", default="localhost:1883", help="MQTT broker host:port")
    p.add_argument("--both", action="store_true", help="HTTP POST + MQTT")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = p.parse_args()

    log = setup_logging(args.verbose)
    use_http = not args.mqtt or args.both
    use_mqtt = args.mqtt or args.both

    mqtt_client = None
    if use_mqtt:
        try:
            import paho.mqtt.client as mqtt
            host, _, port_str = args.mqtt_broker.partition(":")
            port = int(port_str or 1883)
            mqtt_client = mqtt.Client(client_id=f"xbio-bridge-{int(time.time())}")
            mqtt_client.connect(host, port, 60)
            mqtt_client.loop_start()
            log.info("MQTT connected to %s:%d", host, port)
        except ImportError:
            log.error("Install: pip install paho-mqtt")
            sys.exit(1)
        except Exception as e:
            log.error("MQTT connect failed: %s", e)
            sys.exit(1)

    ingest_url = f"{args.url.rstrip('/')}/api/ingest"

    RECONNECT_DELAY = 5
    ser = None

    while ser is None:
        try:
            ser = serial.Serial(args.port, args.baud, timeout=0)
            ser.dtr = False
            ser.rts = False
            time.sleep(0.1)
            ser.dtr = True
            ser.rts = True
            time.sleep(0.1)
            ser.dtr = False
            ser.rts = False
            time.sleep(0.3)
            break
        except PermissionError as e:
            log.error("Port %s LOCKED (PermissionError). Run: python fix_serial_lock.py --port %s", args.port, args.port)
            log.error("Or kill the process: taskkill /F /IM pio.exe  (Windows) | fuser -k %s  (Linux)", args.port)
            log.warning("Retrying in %ds...", RECONNECT_DELAY)
            time.sleep(RECONNECT_DELAY)
        except Exception as e:
            log.error("Failed to open %s: %s. Retrying in %ds...", args.port, e, RECONNECT_DELAY)
            time.sleep(RECONNECT_DELAY)

    log.info("Bridge V2 started | port=%s baud=%d", args.port, args.baud)
    if use_http:
        log.info("Ingest URL: %s", ingest_url)
    if use_mqtt:
        log.info("MQTT broker: %s topic: xbio/{device_id}/data", args.mqtt_broker)
    if args.dry_run:
        log.info("DRY RUN — no POST/MQTT")
    log.info("Log file: %s (max %dMB, %d backups)", LOG_FILE, LOG_MAX_BYTES // (1024 * 1024), LOG_BACKUP_COUNT)

    buf = ""
    while True:
        try:
            n = ser.in_waiting
            if n:
                chunk = ser.read(n)
            else:
                time.sleep(0.05)
                continue
            if chunk:
                buf += chunk.decode("utf-8", errors="ignore")
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line or line.startswith(">>>"):
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    log.debug("Invalid JSON: %s", line[:80])
                    continue

                device_id = get_device_id(data, args.device_id)
                payload = build_ingest_payload(data, device_id)
                mqtt_payload = to_mqtt_payload(data, device_id)

                if args.dry_run:
                    if payload:
                        log.info("HTTP: %s", json.dumps(payload, separators=(",", ":")))
                    if mqtt_payload:
                        log.info("MQTT: %s", json.dumps(mqtt_payload, separators=(",", ":")))
                    continue

                if use_http and payload:
                    try:
                        r = requests.post(ingest_url, json=payload, timeout=5)
                        status = "OK" if r.status_code == 200 else f"ERR {r.status_code}"
                        label = payload.get("s") or payload.get("state") or str(payload.get("truth", ""))
                        log.info("[%s] %s truth=%s | %s", status, label, payload.get("truth", ""), json.dumps(payload, separators=(",", ":"))[:120])
                    except requests.RequestException as e:
                        log.error("POST failed: %s", e)

                if use_mqtt and mqtt_client and mqtt_payload:
                    try:
                        topic = f"xbio/{device_id}/data"
                        mqtt_client.publish(topic, json.dumps(mqtt_payload), qos=0)
                        log.debug("MQTT published: %s", topic)
                    except Exception as e:
                        log.error("MQTT publish failed: %s", e)

        except KeyboardInterrupt:
            log.info("Stopped by user")
            break
        except serial.SerialException as e:
            log.error("Serial disconnected: %s. Reconnecting in %ds...", e, RECONNECT_DELAY)
            try:
                ser.close()
            except Exception:
                pass
            ser = None
            while ser is None:
                try:
                    ser = serial.Serial(args.port, args.baud, timeout=0)
                    ser.dtr, ser.rts = False, False
                    time.sleep(0.1)
                    ser.dtr, ser.rts = True, True
                    time.sleep(0.1)
                    ser.dtr, ser.rts = False, False
                    time.sleep(0.3)
                    log.info("[OK] Serial reconnected")
                    break
                except Exception as ex:
                    log.warning("Reconnect failed: %s. Retry in %ds...", ex, RECONNECT_DELAY)
                    time.sleep(RECONNECT_DELAY)
        except Exception as e:
            log.exception("Error: %s", e)
            time.sleep(1)

    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    if ser:
        try:
            ser.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
