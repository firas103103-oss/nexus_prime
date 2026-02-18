import { Router } from 'express';
import type { Request, Response } from 'express';

const router = Router();

// Live system stats for enhanced dashboard
router.get('/live-stats', async (req: Request, res: Response) => {
  try {
    // Mock live system statistics
    const stats = {
      timestamp: new Date().toISOString(),
      services: {
        total: 7,
        healthy: 6,
        degraded: 1,
        down: 0
      },
      performance: {
        cpu: Math.floor(Math.random() * 30) + 15, // 15-45%
        memory: Math.floor(Math.random() * 20) + 40, // 40-60%
        disk: Math.floor(Math.random() * 10) + 65, // 65-75%
        network: Math.floor(Math.random() * 15) + 80 // 80-95%
      },
      users: {
        active: Math.floor(Math.random() * 20) + 5, // 5-25
        total: 156 + Math.floor(Math.random() * 50) // 156-206
      },
      requests: {
        total: 45678 + Math.floor(Math.random() * 10000),
        successful: 44892 + Math.floor(Math.random() * 9500),
        errors: 786 + Math.floor(Math.random() * 500),
        rpm: 200 + Math.floor(Math.random() * 100) // requests per minute
      }
    };

    res.json(stats);
  } catch (error) {
    console.error('Error fetching live stats:', error);
    res.status(500).json({ error: 'Failed to fetch live stats' });
  }
});

// Service health endpoint
router.get('/service-health', async (req: Request, res: Response) => {
  try {
    const services = [
      {
        name: 'nexus_ai',
        displayName: 'AI Chat Engine',
        status: 'healthy',
        port: 3000,
        responseTime: Math.floor(Math.random() * 100) + 50,
        uptime: Math.floor(Math.random() * 86400),
        metadata: {
          version: '2.1.0',
          memory: Math.floor(Math.random() * 30) + 20,
          cpu: Math.floor(Math.random() * 20) + 10,
          connections: Math.floor(Math.random() * 15) + 5
        }
      },
      {
        name: 'nexus_dashboard',
        displayName: 'Control Dashboard',
        status: 'degraded',
        port: 5001,
        responseTime: Math.floor(Math.random() * 200) + 100,
        uptime: Math.floor(Math.random() * 86400),
        metadata: {
          version: '2.1.0',
          memory: Math.floor(Math.random() * 40) + 30,
          cpu: Math.floor(Math.random() * 25) + 15,
          connections: Math.floor(Math.random() * 10) + 2
        }
      },
      {
        name: 'nexus_voice',
        displayName: 'Voice Engine',
        status: 'healthy',
        port: 5050,
        responseTime: Math.floor(Math.random() * 80) + 30,
        uptime: Math.floor(Math.random() * 86400),
        metadata: {
          version: '1.0.0',
          memory: Math.floor(Math.random() * 25) + 15,
          cpu: Math.floor(Math.random() * 15) + 5,
          connections: Math.floor(Math.random() * 8) + 1
        }
      },
      {
        name: 'nexus_flow',
        displayName: 'Workflow Engine (n8n)',
        status: 'healthy',
        port: 5678,
        responseTime: Math.floor(Math.random() * 150) + 75,
        uptime: Math.floor(Math.random() * 86400),
        metadata: {
          version: '1.23.1',
          memory: Math.floor(Math.random() * 35) + 25,
          cpu: Math.floor(Math.random() * 20) + 10,
          connections: Math.floor(Math.random() * 12) + 3
        }
      },
      {
        name: 'nexus_boardroom',
        displayName: 'Cognitive Boardroom',
        status: 'healthy',
        port: 8501,
        responseTime: Math.floor(Math.random() * 120) + 60,
        uptime: Math.floor(Math.random() * 86400),
        metadata: {
          version: '4.0.0',
          memory: Math.floor(Math.random() * 45) + 35,
          cpu: Math.floor(Math.random() * 30) + 20,
          connections: Math.floor(Math.random() * 18) + 2
        }
      },
      {
        name: 'nexus_ollama',
        displayName: 'AI Model Server',
        status: 'healthy',
        port: 11434,
        responseTime: Math.floor(Math.random() * 300) + 150,
        uptime: Math.floor(Math.random() * 86400),
        metadata: {
          version: '0.1.26',
          memory: Math.floor(Math.random() * 60) + 40,
          cpu: Math.floor(Math.random() * 40) + 30,
          connections: Math.floor(Math.random() * 25) + 5
        }
      },
      {
        name: 'nexus_db',
        displayName: 'PostgreSQL Database',
        status: 'healthy',
        port: 5432,
        responseTime: Math.floor(Math.random() * 50) + 10,
        uptime: Math.floor(Math.random() * 86400),
        metadata: {
          version: '15.1.0',
          memory: Math.floor(Math.random() * 30) + 20,
          cpu: Math.floor(Math.random() * 15) + 5,
          connections: Math.floor(Math.random() * 20) + 10
        }
      }
    ];

    res.json(services);
  } catch (error) {
    console.error('Error fetching service health:', error);
    res.status(500).json({ error: 'Failed to fetch service health' });
  }
});

// Activity feed endpoint
router.get('/activity-feed', async (req: Request, res: Response) => {
  try {
    const activities = [
      {
        id: '1',
        timestamp: new Date(Date.now() - 30000).toISOString(),
        type: 'success',
        title: 'AI Model Updated',
        description: 'Ollama model llama3.2:3b refreshed successfully',
        metadata: {
          service: 'nexus_ollama',
          duration: 2300
        }
      },
      {
        id: '2',
        timestamp: new Date(Date.now() - 120000).toISOString(),
        type: 'user',
        title: 'Dashboard Access',
        description: 'Administrator accessed control panel',
        metadata: {
          user: 'admin',
          ip: '46.224.225.96'
        }
      },
      {
        id: '3',
        timestamp: new Date(Date.now() - 300000).toISOString(),
        type: 'system',
        title: 'Health Check Complete',
        description: 'All services responding within normal parameters',
        metadata: {
          service: 'monitoring'
        }
      },
      {
        id: '4',
        timestamp: new Date(Date.now() - 600000).toISOString(),
        type: 'warning',
        title: 'SSL Certificate Notice',
        description: 'Certificate *.mrf103.com expires in 88 days',
        metadata: {
          service: 'nginx'
        }
      }
    ];

    res.json(activities);
  } catch (error) {
    console.error('Error fetching activity feed:', error);
    res.status(500).json({ error: 'Failed to fetch activity feed' });
  }
});

export { router as enhancedDashboardRoutes };