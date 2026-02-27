/**
 * 🧬 xBio Sentinel - Scent Command
 * مركز xBio المتقدم - الشم الرقمي والغريزة
 * OMEGA V2.1: SRI, MSI, SPI, Truth Score, State
 * Uses useBioSentinel + XBioGateway
 */

import { useState, useEffect } from 'react';
import { Wind, Activity, TrendingUp, AlertCircle, Brain, Thermometer, Droplets, Gauge, Shield, Zap } from 'lucide-react';
import { useBioSentinel } from '@/hooks/useBioSentinel';
import { XBioGateway } from '@/services/XBioGateway';

interface SmellProfile {
  id: string;
  name: string;
  nameAr: string;
  category: string;
  confidence: number;
  color: string;
  lastDetected: Date;
}

export default function XBioSentinel() {
  const { sensorData, omegaData, wsConnected, error: telemetryError } = useBioSentinel();

  const [trainingMode, setTrainingMode] = useState(false);
  const [instinctAlerts, setInstinctAlerts] = useState<string[]>([]);
  const [apiStatus, setApiStatus] = useState<{ health?: string; patents?: string[]; implemented?: string[] } | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  const [agents] = useState([
    { id: 'olfactory', name: 'Olfactory', nameAr: 'الشمي', role: 'Smell Detection & Classification', icon: '👃', color: '#14B8A6', tasks: 156 },
    { id: 'instinct', name: 'Instinct', nameAr: 'الغريزة', role: 'Digital Instinct', icon: '🧠', color: '#0D9488', tasks: 89 },
    { id: 'environ', name: 'Environ', nameAr: 'البيئة', role: 'Environmental Analysis', icon: '🌍', color: '#2DD4BF', tasks: 112 },
    { id: 'sensor', name: 'Sensor', nameAr: 'المستشعر', role: 'Hardware & Sensors', icon: '📡', color: '#5EEAD4', tasks: 67 }
  ]);

  const [smellProfiles, setSmellProfiles] = useState<SmellProfile[]>([
    { id: '1', name: 'Fresh Air', nameAr: 'هواء منعش', category: 'clean', confidence: 95, color: '#10B981', lastDetected: new Date() },
    { id: '2', name: 'Coffee', nameAr: 'قهوة', category: 'food', confidence: 88, color: '#F59E0B', lastDetected: new Date(Date.now() - 3600000) },
    { id: '3', name: 'Smoke', nameAr: 'دخان', category: 'alert', confidence: 0, color: '#EF4444', lastDetected: new Date(Date.now() - 86400000) }
  ]);

  // Fetch X-BIO API via XBioGateway
  useEffect(() => {
    const fetchApi = async () => {
      try {
        const [health, patents] = await Promise.all([
          XBioGateway.getHealth(),
          XBioGateway.getPatents(),
        ]);
        setApiStatus({
          health: health?.status || 'ok',
          patents: patents?.patents || [],
          implemented: patents?.implemented || [],
        });
        setApiError(null);
      } catch (e) {
        setApiError((e as Error).message || 'فشل الاتصال');
      }
    };
    fetchApi();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-8">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
              <span className="text-5xl">🧬</span>
              xBio Sentinel
            </h1>
            <p className="text-gray-400 text-lg">Maestro Scent - سينت | الشم الرقمي والغريزة</p>
            {apiStatus && (
              <div className="mt-2 text-sm">
                <span className="text-green-400">API: {apiStatus.health}</span>
                {apiStatus.patents?.length && (
                  <span className="text-gray-500 ml-2">| براءات: {apiStatus.patents.length} ({apiStatus.implemented?.length || 0} مُنفّذة)</span>
                )}
                {wsConnected && (
                  <span className="ml-2 text-cyan-400">| Real-time WS</span>
                )}
              </div>
            )}
            {apiError && <div className="mt-2 text-sm text-red-400">API: {apiError}</div>}
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => setTrainingMode(!trainingMode)}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${trainingMode
                ? 'bg-green-500 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
            >
              {trainingMode ? '🎓 Training Mode: ON' : '📖 Training Mode: OFF'}
            </button>
          </div>
        </div>
      </div>

      {/* OMEGA V2.1 — Sovereign Witness (when available) */}
      {omegaData && (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Shield className="w-6 h-6 text-amber-400" />
              OMEGA V2.1 — Sovereign Witness
            </h2>
            <div className="flex items-center gap-3">
              <span className={`px-4 py-2 rounded-lg font-bold text-sm ${omegaData.state === 'RESONANCE_DISTURBANCE'
                ? 'bg-red-500/20 text-red-400 border border-red-500/50'
                : 'bg-green-500/20 text-green-400 border border-green-500/50'
                }`}>
                {omegaData.state === 'RESONANCE_DISTURBANCE' ? '⚠️ RESONANCE_DISTURBANCE' : '✓ VOID_STABLE'}
              </span>
              {omegaData.alert && (
                <span className="px-4 py-2 rounded-lg font-bold text-sm bg-red-500/30 text-red-300 border border-red-500 animate-pulse">
                  <AlertCircle className="w-4 h-4 inline mr-1" />
                  ALERT
                </span>
              )}
              <span className="text-xs text-gray-500">{omegaData.deviceId}</span>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-gradient-to-br from-cyan-500/20 to-cyan-600/20 rounded-lg p-6 border border-cyan-500/30">
              <div className="flex items-center gap-3 mb-2">
                <Zap className="w-8 h-8 text-cyan-400" />
                <div>
                  <div className="text-xs text-gray-400">SRI</div>
                  <div className="text-2xl font-bold">{omegaData.sri.toFixed(3)}</div>
                </div>
              </div>
              <div className="text-xs text-gray-500">Sovereign Resonance Index</div>
            </div>
            <div className="bg-gradient-to-br from-violet-500/20 to-violet-600/20 rounded-lg p-6 border border-violet-500/30">
              <div className="flex items-center gap-3 mb-2">
                <Activity className="w-8 h-8 text-violet-400" />
                <div>
                  <div className="text-xs text-gray-400">MSI</div>
                  <div className="text-2xl font-bold">{omegaData.msi.toFixed(2)}</div>
                </div>
              </div>
              <div className="text-xs text-gray-500">Metabolic Stress Index</div>
            </div>
            <div className="bg-gradient-to-br from-fuchsia-500/20 to-fuchsia-600/20 rounded-lg p-6 border border-fuchsia-500/30">
              <div className="flex items-center gap-3 mb-2">
                <Wind className="w-8 h-8 text-fuchsia-400" />
                <div>
                  <div className="text-xs text-gray-400">SPI</div>
                  <div className="text-2xl font-bold">{omegaData.spi.toFixed(2)}</div>
                </div>
              </div>
              <div className="text-xs text-gray-500">Sovereign Pheromone Index</div>
            </div>
            <div className="bg-gradient-to-br from-amber-500/20 to-amber-600/20 rounded-lg p-6 border border-amber-500/30">
              <div className="flex items-center gap-3 mb-2">
                <TrendingUp className="w-8 h-8 text-amber-400" />
                <div>
                  <div className="text-xs text-gray-400">Truth Score</div>
                  <div className="text-2xl font-bold">{omegaData.truthScore.toFixed(1)}</div>
                </div>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-amber-500 to-amber-600"
                  style={{ width: `${Math.min(100, omegaData.truthScore)}%` }}
                />
              </div>
            </div>
          </div>
          {telemetryError && <div className="mt-2 text-sm text-amber-400">{telemetryError}</div>}
        </div>
      )}

      {/* Live Sensor Readings (legacy / fallback) */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <Activity className="w-6 h-6 text-teal-400" />
          {omegaData ? 'Legacy Sensors' : 'Live Sensor Readings'} — ESP32-S3 N16R8 + BME688
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="bg-gradient-to-br from-red-500/20 to-red-600/20 rounded-lg p-6 border border-red-500/30">
            <div className="flex items-center gap-3 mb-3">
              <Thermometer className="w-8 h-8 text-red-400" />
              <div>
                <div className="text-xs text-gray-400">Temperature</div>
                <div className="text-2xl font-bold">{sensorData.temperature.toFixed(1)}°C</div>
              </div>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div className="h-2 rounded-full bg-gradient-to-r from-red-500 to-red-600" style={{ width: '70%' }} />
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-lg p-6 border border-blue-500/30">
            <div className="flex items-center gap-3 mb-3">
              <Droplets className="w-8 h-8 text-blue-400" />
              <div>
                <div className="text-xs text-gray-400">Humidity</div>
                <div className="text-2xl font-bold">{sensorData.humidity.toFixed(0)}%</div>
              </div>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-blue-600" style={{ width: `${sensorData.humidity}%` }} />
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 rounded-lg p-6 border border-purple-500/30">
            <div className="flex items-center gap-3 mb-3">
              <Gauge className="w-8 h-8 text-purple-400" />
              <div>
                <div className="text-xs text-gray-400">Pressure</div>
                <div className="text-2xl font-bold">{sensorData.pressure.toFixed(0)}</div>
              </div>
            </div>
            <div className="text-xs text-gray-500">hPa</div>
          </div>

          <div className="bg-gradient-to-br from-teal-500/20 to-teal-600/20 rounded-lg p-6 border border-teal-500/30">
            <div className="flex items-center gap-3 mb-3">
              <Wind className="w-8 h-8 text-teal-400" />
              <div>
                <div className="text-xs text-gray-400">Gas Resistance</div>
                <div className="text-2xl font-bold">{(sensorData.gasResistance / 1000).toFixed(0)}K</div>
              </div>
            </div>
            <div className="text-xs text-gray-500">Ohms</div>
          </div>

          <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 rounded-lg p-6 border border-green-500/30">
            <div className="flex items-center gap-3 mb-3">
              <TrendingUp className="w-8 h-8 text-green-400" />
              <div>
                <div className="text-xs text-gray-400">Air Quality</div>
                <div className="text-2xl font-bold">{sensorData.airQuality.toFixed(0)}%</div>
              </div>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div className="h-2 rounded-full bg-gradient-to-r from-green-500 to-green-600" style={{ width: `${sensorData.airQuality}%` }} />
            </div>
          </div>
        </div>
      </div>

      {/* Smell Profiles */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-gray-800/50 rounded-lg p-6 border border-gray-700">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span className="text-2xl">👃</span>
            Detected Smell Profiles
          </h3>
          <div className="space-y-3">
            {smellProfiles.map((profile) => (
              <div
                key={profile.id}
                className="p-4 rounded-lg border"
                style={{
                  backgroundColor: `${profile.color}10`,
                  borderColor: `${profile.color}40`
                }}
              >
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <div className="font-semibold flex items-center gap-2">
                      {profile.name}
                      <span className="text-sm text-gray-400">({profile.nameAr})</span>
                    </div>
                    <div className="text-xs text-gray-500 capitalize">{profile.category}</div>
                  </div>
                  <div
                    className="px-3 py-1 rounded-full text-xs font-bold"
                    style={{
                      backgroundColor: `${profile.color}20`,
                      color: profile.color
                    }}
                  >
                    {profile.confidence}%
                  </div>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div
                    className="h-2 rounded-full"
                    style={{
                      width: `${profile.confidence}%`,
                      backgroundColor: profile.color
                    }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-2">
                  Last: {profile.lastDetected.toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Digital Instinct */}
        <div className="bg-gray-800/50 rounded-lg p-6 border border-gray-700">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Brain className="w-6 h-6 text-purple-400" />
            Digital Instinct - الغريزة الرقمية
          </h3>
          <div className="space-y-3">
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="w-5 h-5 text-blue-400" />
                <span className="font-semibold text-blue-400">Pattern Detected</span>
              </div>
              <p className="text-sm text-gray-300">
                Unusual air quality pattern detected at this time of day
              </p>
            </div>

            <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <span className="font-semibold text-green-400">Learning Progress</span>
              </div>
              <p className="text-sm text-gray-300">
                Successfully learned 3 new smell patterns this week
              </p>
            </div>

            <div className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Brain className="w-5 h-5 text-purple-400" />
                <span className="font-semibold text-purple-400">Prediction</span>
              </div>
              <p className="text-sm text-gray-300">
                Environment quality will improve in next 2 hours
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* xBio Team */}
      <div>
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <span className="text-2xl">👥</span>
          xBio Team
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="bg-gray-800/50 rounded-lg p-4 border border-gray-700"
              style={{ borderLeftColor: agent.color, borderLeftWidth: '3px' }}
            >
              <div className="flex items-center gap-3 mb-3">
                <span className="text-3xl">{agent.icon}</span>
                <div>
                  <h3 className="font-bold">{agent.name}</h3>
                  <p className="text-xs text-gray-400">{agent.nameAr}</p>
                </div>
              </div>
              <p className="text-sm text-gray-400 mb-3">{agent.role}</p>
              <div className="flex items-center justify-between">
                <span className="px-2 py-1 rounded text-xs font-bold bg-teal-500/20 text-teal-400">ACTIVE</span>
                <span className="text-sm text-gray-400">{agent.tasks} tasks</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
