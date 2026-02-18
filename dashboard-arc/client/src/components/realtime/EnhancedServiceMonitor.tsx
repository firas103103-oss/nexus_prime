import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Activity, 
  Database, 
  Brain, 
  Mic, 
  MessageSquare, 
  BarChart3,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock
} from 'lucide-react';

interface ServiceHealth {
  name: string;
  displayName: string;
  status: 'healthy' | 'degraded' | 'down' | 'starting';
  uptime: number;
  responseTime: number;
  port: number;
  url: string;
  lastCheck: string;
  metadata?: {
    version?: string;
    memory?: number;
    cpu?: number;
    connections?: number;
  };
}

const serviceConfigs = [
  { name: 'nexus_ai', displayName: 'AI Chat Engine', port: 3000, icon: Brain },
  { name: 'nexus_dashboard', displayName: 'Dashboard', port: 5001, icon: BarChart3 },
  { name: 'nexus_voice', displayName: 'Voice Engine', port: 5050, icon: Mic },
  { name: 'nexus_flow', displayName: 'Workflow Engine', port: 5678, icon: MessageSquare },
  { name: 'nexus_boardroom', displayName: 'Boardroom', port: 8501, icon: Activity },
  { name: 'nexus_ollama', displayName: 'AI Models', port: 11434, icon: Brain },
  { name: 'nexus_db', displayName: 'Database', port: 5432, icon: Database },
];

export default function EnhancedServiceMonitor() {
  const [services, setServices] = useState<ServiceHealth[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const fetchServiceHealth = async () => {
    try {
      // Test each service
      const healthChecks = serviceConfigs.map(async (config) => {
        const startTime = Date.now();
        try {
          const response = await fetch(`http://localhost:${config.port}/`, { 
            method: 'GET',
            signal: AbortSignal.timeout(5000)
          });
          const responseTime = Date.now() - startTime;
          
          return {
            name: config.name,
            displayName: config.displayName,
            status: response.ok ? 'healthy' : 'degraded' as ServiceHealth['status'],
            uptime: Math.floor(Math.random() * 86400), // Mock uptime
            responseTime,
            port: config.port,
            url: `http://localhost:${config.port}`,
            lastCheck: new Date().toISOString(),
            metadata: {
              version: '2.1.0',
              memory: Math.floor(Math.random() * 100),
              cpu: Math.floor(Math.random() * 50),
              connections: Math.floor(Math.random() * 20),
            }
          };
        } catch (error) {
          return {
            name: config.name,
            displayName: config.displayName,
            status: 'down' as ServiceHealth['status'],
            uptime: 0,
            responseTime: 5000,
            port: config.port,
            url: `http://localhost:${config.port}`,
            lastCheck: new Date().toISOString(),
          };
        }
      });

      const results = await Promise.all(healthChecks);
      setServices(results);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Failed to fetch service health:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServiceHealth();
    const interval = setInterval(fetchServiceHealth, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: ServiceHealth['status']) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'degraded': return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      case 'down': return <XCircle className="h-4 w-4 text-red-500" />;
      case 'starting': return <Clock className="h-4 w-4 text-blue-500 animate-spin" />;
    }
  };

  const getStatusColor = (status: ServiceHealth['status']) => {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-50 border-green-200';
      case 'degraded': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'down': return 'text-red-600 bg-red-50 border-red-200';
      case 'starting': return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  const formatUptime = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
  };

  const healthyServices = services.filter(s => s.status === 'healthy').length;
  const totalServices = services.length;
  const overallHealthPercentage = totalServices ? (healthyServices / totalServices) * 100 : 0;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
        <div>
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Service Health Monitor
          </CardTitle>
          <p className="text-sm text-muted-foreground mt-1">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-2xl font-bold text-green-600">{healthyServices}/{totalServices}</div>
            <div className="text-xs text-muted-foreground">Services Online</div>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={fetchServiceHealth}
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="mb-4">
          <div className="flex justify-between text-sm mb-2">
            <span>Overall System Health</span>
            <span className="font-medium">{overallHealthPercentage.toFixed(0)}%</span>
          </div>
          <Progress value={overallHealthPercentage} className="h-2" />
        </div>

        <div className="grid gap-3">
          {serviceConfigs.map((config) => {
            const service = services.find(s => s.name === config.name);
            const Icon = config.icon;
            
            return (
              <div 
                key={config.name}
                className={`p-4 rounded-lg border transition-all duration-200 ${
                  service ? getStatusColor(service.status) : 'bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="flex items-center gap-2">
                      <Icon className="h-5 w-5 text-current" />
                      <div>
                        <h4 className="font-medium">{config.displayName}</h4>
                        <p className="text-xs opacity-75">Port {config.port}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4 text-sm">
                    {service && (
                      <>
                        <div className="text-center hidden sm:block">
                          <div className="font-medium">{service.responseTime}ms</div>
                          <div className="text-xs opacity-75">Response</div>
                        </div>
                        
                        <div className="text-center hidden md:block">
                          <div className="font-medium">{formatUptime(service.uptime)}</div>
                          <div className="text-xs opacity-75">Uptime</div>
                        </div>
                        
                        {service.metadata && (
                          <div className="text-center hidden lg:block">
                            <div className="font-medium">{service.metadata.memory}%</div>
                            <div className="text-xs opacity-75">Memory</div>
                          </div>
                        )}
                      </>
                    )}
                    
                    <div className="flex items-center gap-2">
                      {service ? getStatusIcon(service.status) : (
                        <div className="w-4 h-4 bg-gray-300 rounded-full animate-pulse" />
                      )}
                      <Badge variant="secondary" className="text-xs">
                        {service?.status || 'loading'}
                      </Badge>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}