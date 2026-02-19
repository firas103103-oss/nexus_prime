import React from 'react';
// @ts-ignore - react-helmet-async types
import { Helmet } from 'react-helmet-async';
import LiveSystemStats from '../components/realtime/LiveSystemStats';
import RealtimeActivityFeed from '../components/realtime/RealtimeActivityFeed';
import EnhancedServiceMonitor from '../components/realtime/EnhancedServiceMonitor';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
// @ts-ignore - lucide-react types
import { 
  Crown, 
  Zap, 
  Shield, 
  Globe2, 
  Server, 
  TrendingUp,
  Users,
  Cpu,
  Database
} from 'lucide-react';

export default function EnhancedDashboard() {
  return (
    <>
      <Helmet>
        <title>NEXUS PRIME - Command Center</title>
        <meta name="description" content="Advanced AI Empire Control Dashboard" />
      </Helmet>
      
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        {/* Header */}
        <div className="border-b border-white/10 bg-black/20 backdrop-blur-sm">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center gap-3">
                  <Crown className="h-8 w-8 text-yellow-400" />
                  <div>
                    <h1 className="text-2xl font-bold text-white">NEXUS PRIME</h1>
                    <p className="text-sm text-blue-200">Empire Command Center</p>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-4">
                <Badge variant="secondary" className="bg-green-500/20 text-green-300 border-green-500/30">
                  <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse" />
                  System Operational
                </Badge>
                
                <div className="text-sm text-slate-300 text-right">
                  <div className="font-medium">Supreme Commander</div>
                  <div className="text-xs text-slate-400">Mr. Firas</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Dashboard */}
        <div className="container mx-auto px-6 py-8 space-y-8">
          
          {/* Quick Stats Row */}
          <LiveSystemStats />
          
          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Left Column - Service Monitor */}
            <div className="lg:col-span-2">
              <EnhancedServiceMonitor />
            </div>
            
            {/* Right Column - Activity Feed */}
            <div className="lg:col-span-1">
              <RealtimeActivityFeed />
            </div>
          </div>

          {/* Empire Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* AI Operations */}
            <Card className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 border-purple-500/20">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-purple-200">AI Operations</CardTitle>
                <Zap className="h-4 w-4 text-purple-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-100">24/7</div>
                <p className="text-xs text-purple-300">Active AI Agents</p>
                <div className="mt-3 flex gap-2">
                  <Badge variant="outline" className="text-purple-300 border-purple-500/30">
                    🤖 Cognitive Boardroom
                  </Badge>
                </div>
              </CardContent>
            </Card>

            {/* Security Status */}
            <Card className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-500/20">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-green-200">Security</CardTitle>
                <Shield className="h-4 w-4 text-green-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-100">SECURE</div>
                <p className="text-xs text-green-300">All systems protected</p>
                <div className="mt-3 flex gap-2">
                  <Badge variant="outline" className="text-green-300 border-green-500/30">
                    🛡️ XBio Sentinel
                  </Badge>
                </div>
              </CardContent>
            </Card>

            {/* Global Reach */}
            <Card className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border-blue-500/20">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-blue-200">Global Reach</CardTitle>
                <Globe2 className="h-4 w-4 text-blue-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-100">LIVE</div>
                <p className="text-xs text-blue-300">mrf103.com empire</p>
                <div className="mt-3 flex gap-2">
                  <Badge variant="outline" className="text-blue-300 border-blue-500/30">
                    🌐 14 Domains
                  </Badge>
                </div>
              </CardContent>
            </Card>

            {/* Performance */}
            <Card className="bg-gradient-to-br from-orange-500/10 to-red-500/10 border-orange-500/20">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-orange-200">Performance</CardTitle>
                <TrendingUp className="h-4 w-4 text-orange-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-100">OPTIMAL</div>
                <p className="text-xs text-orange-300">System efficiency</p>
                <div className="mt-3 flex gap-2">
                  <Badge variant="outline" className="text-orange-300 border-orange-500/30">
                    ⚡ 99.9% Uptime
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <Card className="bg-black/20 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Server className="h-5 w-5" />
                Quick Actions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                <Button variant="outline" className="h-20 flex-col gap-2 bg-white/5 border-white/10 hover:bg-white/10 text-white">
                  <Database className="h-6 w-6" />
                  <span className="text-xs">Database</span>
                </Button>
                
                <Button variant="outline" className="h-20 flex-col gap-2 bg-white/5 border-white/10 hover:bg-white/10 text-white">
                  <Zap className="h-6 w-6" />
                  <span className="text-xs">AI Chat</span>
                </Button>
                
                <Button variant="outline" className="h-20 flex-col gap-2 bg-white/5 border-white/10 hover:bg-white/10 text-white">
                  <Users className="h-6 w-6" />
                  <span className="text-xs">Boardroom</span>
                </Button>
                
                <Button variant="outline" className="h-20 flex-col gap-2 bg-white/5 border-white/10 hover:bg-white/10 text-white">
                  <Globe2 className="h-6 w-6" />
                  <span className="text-xs">Websites</span>
                </Button>
                
                <Button variant="outline" className="h-20 flex-col gap-2 bg-white/5 border-white/10 hover:bg-white/10 text-white">
                  <Cpu className="h-6 w-6" />
                  <span className="text-xs">Monitoring</span>
                </Button>
                
                <Button variant="outline" className="h-20 flex-col gap-2 bg-white/5 border-white/10 hover:bg-white/10 text-white">
                  <Shield className="h-6 w-6" />
                  <span className="text-xs">Security</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <div className="border-t border-white/10 bg-black/20 backdrop-blur-sm mt-12">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between text-sm text-slate-400">
              <div>© 2026 MRF103 Empire. Supreme AI Architecture.</div>
              <div className="flex items-center gap-4">
                <span>Version 2.1.0</span>
                <span>•</span>
                <span>Hetzner Cloud</span>
                <span>•</span>
                <span>46.224.225.96</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}