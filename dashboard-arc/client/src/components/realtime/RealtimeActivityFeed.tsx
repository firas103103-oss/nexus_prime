import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
// @ts-ignore
import { Activity, User, Server, AlertCircle, CheckCircle, Zap, RefreshCw } from 'lucide-react';

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
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchActivities = useCallback(async () => {
    try {
      const response = await fetch('/api/enhanced/activity-feed');
      if (!response.ok) throw new Error('Failed to fetch activities');
      const data = await response.json();
      
      // Transform API data to component format
      const newActivities: ActivityEvent[] = data.map((item: any) => ({
        id: item.id || Math.random().toString(36).substr(2, 9),
        timestamp: item.timestamp,
        type: item.type || 'system',
        title: item.title,
        description: item.description,
        metadata: item.metadata
      }));
      
      setActivities(prev => {
        // Merge new activities, avoiding duplicates
        const existingIds = new Set(prev.map(a => a.id));
        const uniqueNew = newActivities.filter((a: ActivityEvent) => !existingIds.has(a.id));
        return [...uniqueNew, ...prev].slice(0, 50); // Keep last 50
      });
      
      setIsConnected(true);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Connection error');
      setIsConnected(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    // Initial fetch
    fetchActivities();
    
    // Poll for updates every 5 seconds
    const interval = setInterval(fetchActivities, 5000);
    
    return () => clearInterval(interval);
  }, [fetchActivities]);

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