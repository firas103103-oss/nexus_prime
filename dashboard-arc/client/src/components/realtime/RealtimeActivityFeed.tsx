import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Activity, User, Server, AlertCircle, CheckCircle, Zap } from 'lucide-react';

interface ActivityEvent {
  id: string;
  timestamp: string;
  type: 'user' | 'system' | 'error' | 'success' | 'warning';
  title: string;
  description: string;
  metadata?: {
    user?: string;
    service?: string;
    duration?: number;
    ip?: string;
  };
}

export default function RealtimeActivityFeed() {
  const [activities, setActivities] = useState<ActivityEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Simulate real-time activity feed
    const generateActivity = (): ActivityEvent => {
      const types: ActivityEvent['type'][] = ['user', 'system', 'error', 'success', 'warning'];
      const type = types[Math.floor(Math.random() * types.length)];
      
      const activities: Record<ActivityEvent['type'], { title: string; description: string }[]> = {
        user: [
          { title: 'User Login', description: 'New user session started' },
          { title: 'Dashboard Access', description: 'User accessed admin dashboard' },
          { title: 'API Request', description: 'User made API call to /agents' },
        ],
        system: [
          { title: 'Service Health Check', description: 'All services responding normally' },
          { title: 'Database Backup', description: 'Automated backup completed' },
          { title: 'Cache Refresh', description: 'Redis cache updated successfully' },
        ],
        error: [
          { title: 'Connection Timeout', description: 'Database connection timeout occurred' },
          { title: 'Rate Limit Exceeded', description: 'API rate limit hit for IP 192.168.1.100' },
          { title: 'Authentication Failed', description: 'Invalid credentials provided' },
        ],
        success: [
          { title: 'Deployment Complete', description: 'New version deployed successfully' },
          { title: 'Backup Created', description: 'System backup completed in 2.3s' },
          { title: 'AI Model Updated', description: 'Ollama model refreshed' },
        ],
        warning: [
          { title: 'High Memory Usage', description: 'Memory usage reached 85%' },
          { title: 'SSL Certificate', description: 'Certificate expires in 30 days' },
          { title: 'Disk Space Low', description: 'Available disk space below 15%' },
        ],
      };

      const typeActivities = activities[type];
      const activity = typeActivities[Math.floor(Math.random() * typeActivities.length)];

      return {
        id: Math.random().toString(36).substr(2, 9),
        timestamp: new Date().toISOString(),
        type,
        title: activity.title,
        description: activity.description,
        metadata: {
          user: `user${Math.floor(Math.random() * 100)}`,
          service: `nexus_${['ai', 'dashboard', 'db', 'flow', 'voice'][Math.floor(Math.random() * 5)]}`,
          duration: Math.floor(Math.random() * 5000),
          ip: `192.168.1.${Math.floor(Math.random() * 255)}`,
        }
      };
    };

    // Initial activities
    const initialActivities = Array.from({ length: 10 }, generateActivity);
    setActivities(initialActivities);
    setIsConnected(true);

    // Simulate real-time updates
    const interval = setInterval(() => {
      const newActivity = generateActivity();
      setActivities(prev => [newActivity, ...prev.slice(0, 49)]); // Keep last 50
    }, 3000 + Math.random() * 4000); // Random interval 3-7 seconds

    return () => clearInterval(interval);
  }, []);

  const getIcon = (type: ActivityEvent['type']) => {
    switch (type) {
      case 'user': return <User className="h-4 w-4 text-blue-500" />;
      case 'system': return <Server className="h-4 w-4 text-gray-500" />;
      case 'error': return <AlertCircle className="h-4 w-4 text-red-500" />;
      case 'success': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'warning': return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      default: return <Activity className="h-4 w-4 text-gray-400" />;
    }
  };

  const getBadgeVariant = (type: ActivityEvent['type']) => {
    switch (type) {
      case 'error': return 'destructive';
      case 'success': return 'default';
      case 'warning': return 'secondary';
      default: return 'outline';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    
    if (diff < 60000) return `${Math.floor(diff / 1000)}s ago`;
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    return date.toLocaleTimeString();
  };

  return (
    <Card className="h-[600px]">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Activity className="h-5 w-5" />
          Live Activity Feed
        </CardTitle>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
          <span className="text-xs text-muted-foreground">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[500px] w-full">
          <div className="space-y-3">
            {activities.map((activity) => (
              <div 
                key={activity.id}
                className="flex items-start space-x-3 p-3 rounded-lg border bg-card/50 hover:bg-card transition-colors"
              >
                <div className="mt-0.5">
                  {getIcon(activity.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-medium text-foreground">
                      {activity.title}
                    </p>
                    <div className="flex items-center gap-2">
                      <Badge variant={getBadgeVariant(activity.type)} className="text-xs">
                        {activity.type}
                      </Badge>
                      <span className="text-xs text-muted-foreground whitespace-nowrap">
                        {formatTimestamp(activity.timestamp)}
                      </span>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    {activity.description}
                  </p>
                  {activity.metadata && (
                    <div className="flex gap-3 mt-2 text-xs text-muted-foreground">
                      {activity.metadata.service && (
                        <span>Service: {activity.metadata.service}</span>
                      )}
                      {activity.metadata.duration && (
                        <span>Duration: {activity.metadata.duration}ms</span>
                      )}
                      {activity.metadata.ip && (
                        <span>IP: {activity.metadata.ip}</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}