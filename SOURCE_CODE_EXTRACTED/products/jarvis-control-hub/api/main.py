#!/usr/bin/env python3
'''
JARVIS CORE CONTROL API
The brain that controls everything
'''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
from datetime import datetime
from typing import Optional, Dict, List

app = FastAPI(
    title='JARVIS Core Engine',
    description='Central control API for the entire ecosystem',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Models
class ServiceControl(BaseModel):
    action: str  # start, stop, restart, status
    service: str

class CommandRequest(BaseModel):
    command: str
    description: Optional[str] = None

# Health Check
@app.get('/')
async def root():
    return {
        'status': 'operational',
        'engine': 'JARVIS Core',
        'owner': 'Firas',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }

@app.get('/health')
async def health():
    '''System health check'''
    try:
        # Check Docker
        docker_status = subprocess.run(
            ['docker', 'ps', '-a', '--format', '{{json .}}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        containers = []
        if docker_status.returncode == 0:
            for line in docker_status.stdout.strip().split('\n'):
                if line:
                    containers.append(json.loads(line))
        
        return {
            'status': 'healthy',
            'docker': {
                'available': docker_status.returncode == 0,
                'containers': len(containers),
                'running': len([c for c in containers if 'Up' in c.get('Status', '')])
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            'status': 'degraded',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }

@app.get('/services/list')
async def list_services():
    '''List all Docker containers'''
    try:
        result = subprocess.run(
            ['docker', 'ps', '-a', '--format', '{{json .}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                containers.append(json.loads(line))
        
        return {
            'success': True,
            'count': len(containers),
            'services': containers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/services/control')
async def control_service(req: ServiceControl):
    '''Start/stop/restart Docker containers'''
    try:
        if req.action == 'start':
            cmd = ['docker', 'start', req.service]
        elif req.action == 'stop':
            cmd = ['docker', 'stop', req.service]
        elif req.action == 'restart':
            cmd = ['docker', 'restart', req.service]
        elif req.action == 'status':
            cmd = ['docker', 'inspect', req.service]
        else:
            raise HTTPException(status_code=400, detail='Invalid action')
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        return {
            'success': result.returncode == 0,
            'action': req.action,
            'service': req.service,
            'output': result.stdout,
            'error': result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/exec')
async def execute_command(req: CommandRequest):
    '''Execute system command (use with caution)'''
    try:
        result = subprocess.run(
            req.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return {
            'success': result.returncode == 0,
            'command': req.command,
            'output': result.stdout,
            'error': result.stderr if result.returncode != 0 else None,
            'exit_code': result.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/system/info')
async def system_info():
    '''Get system information'''
    try:
        # Disk usage
        df = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        # Memory
        free = subprocess.run(['free', '-h'], capture_output=True, text=True)
        # Uptime
        uptime = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
        
        return {
            'success': True,
            'disk': df.stdout,
            'memory': free.stdout,
            'uptime': uptime.stdout.strip(),
            'timestamp': datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
