/**
 * useBioSentinel — Parse, sanitize, stream WebSocket data from X-Bio IoT
 * Integrates with SovereignMasterContext for GalaxyDashboard
 */
import { useState, useEffect, useCallback, useRef } from "react";
import { z } from "zod";
import { XBioGateway } from "@/services/XBioGateway";

const SensorReadingSchema = z.object({
  temperature: z.number().min(-50).max(100).optional(),
  humidity: z.number().min(0).max(100).optional(),
  pressure: z.number().min(0).max(2000).optional(),
  gasResistance: z.number().min(0).optional(),
  iaq: z.number().min(0).max(500).optional(),
});

const OmegaMetaSchema = z.object({
  sri: z.number(),
  msi: z.number(),
  spi: z.number(),
  truth: z.number(),
  s: z.string().optional(),
  alert: z.boolean().optional(),
});

const WsMessageSchema = z.object({
  type: z.string(),
  deviceId: z.string().optional(),
  data: z
    .object({
      metadata: z.record(z.unknown()).optional(),
      temperature: z.number().optional(),
      humidity: z.number().optional(),
      pressure: z.number().optional(),
      gasResistance: z.number().optional(),
      iaq: z.number().optional(),
    })
    .optional(),
});

export interface SensorData {
  temperature: number;
  humidity: number;
  pressure: number;
  gasResistance: number;
  airQuality: number;
  timestamp: Date;
}

export interface OmegaData {
  sri: number;
  msi: number;
  spi: number;
  truthScore: number;
  state: string;
  alert: boolean;
  deviceId: string;
  timestamp: string;
}

const DEFAULT_SENSOR: SensorData = {
  temperature: 24.5,
  humidity: 45,
  pressure: 1013,
  gasResistance: 150000,
  airQuality: 92,
  timestamp: new Date(),
};

const IOT_WS_PORT = import.meta.env.VITE_IOT_WS_PORT || "8081";

export function useBioSentinel() {
  const [sensorData, setSensorData] = useState<SensorData>(DEFAULT_SENSOR);
  const [omegaData, setOmegaData] = useState<OmegaData | null>(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleMessage = useCallback((ev: MessageEvent) => {
    try {
      const raw = JSON.parse(ev.data as string);
      const parsed = WsMessageSchema.safeParse(raw);
      if (!parsed.success) return;

      const msg = parsed.data;
      if (msg.type !== "sensor_reading") return;

      const data = msg.data;
      const meta = data?.metadata;

      if (meta) {
        const metaParsed = OmegaMetaSchema.safeParse(meta);
        if (metaParsed.success) {
          const m = metaParsed.data;
          setOmegaData({
            sri: m.sri,
            msi: m.msi,
            spi: m.spi,
            truthScore: m.truth,
            state: m.s ?? "VOID_STABLE",
            alert: m.alert ?? false,
            deviceId: msg.deviceId ?? "",
            timestamp: new Date().toISOString(),
          });
          setError(null);
        }
      }

      if (data) {
        const sensorParsed = SensorReadingSchema.safeParse(data);
        if (sensorParsed.success) {
          const s = sensorParsed.data;
          setSensorData((prev) => ({
            ...prev,
            temperature: s.temperature ?? prev.temperature,
            humidity: s.humidity ?? prev.humidity,
            pressure: s.pressure ?? prev.pressure,
            gasResistance: s.gasResistance ?? prev.gasResistance,
            airQuality: s.iaq ?? prev.airQuality,
            timestamp: new Date(),
          }));
        }
      }
    } catch {
      // ignore parse errors
    }
  }, []);

  const reconnect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;
    const host = window.location.hostname;
    const wsUrl = `ws://${host}:${IOT_WS_PORT}`;
    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;
      ws.onopen = () => setWsConnected(true);
      ws.onclose = () => {
        setWsConnected(false);
        reconnectRef.current = setTimeout(reconnect, 3000);
      };
      ws.onmessage = handleMessage;
      ws.onerror = () => { };
    } catch {
      setWsConnected(false);
    }
  }, [handleMessage]);

  useEffect(() => {
    reconnect();
    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [reconnect]);

  // Fallback: poll telemetry when WS disconnected
  useEffect(() => {
    if (wsConnected) return;
    const poll = async () => {
      try {
        const res = await XBioGateway.getLatestTelemetry(5);
        const rows = res.data ?? [];
        const omegaRow = rows.find(
          (r) =>
            r.sri != null && r.msi != null && r.spi != null && r.truth_score != null
        );
        if (omegaRow) {
          setOmegaData({
            sri: Number(omegaRow.sri),
            msi: Number(omegaRow.msi),
            spi: Number(omegaRow.spi),
            truthScore: Number(omegaRow.truth_score),
            state: String(omegaRow.state ?? "VOID_STABLE"),
            alert: Boolean(omegaRow.alert),
            deviceId: String(omegaRow.device_id ?? ""),
            timestamp: String(omegaRow.created_at ?? ""),
          });
          setError(null);
        }
        if (rows.length > 0) {
          const r = rows[0];
          setSensorData({
            temperature: Number(r.temperature) ?? 24,
            humidity: Number(r.humidity) ?? 45,
            pressure: Number(r.pressure) ?? 1013,
            gasResistance: Number(r.gas_resistance) ?? 150000,
            airQuality: Number(r.iaq) ?? 90,
            timestamp: new Date(r.created_at ?? Date.now()),
          });
        }
      } catch (e) {
        setError((e as Error).message ?? "Telemetry unavailable");
      }
    };
    poll();
    const interval = setInterval(poll, 3000);
    return () => clearInterval(interval);
  }, [wsConnected]);

  return {
    sensorData,
    omegaData,
    wsConnected,
    error,
    reconnect,
  };
}
