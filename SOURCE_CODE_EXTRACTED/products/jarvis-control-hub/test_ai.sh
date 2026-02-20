#!/bin/bash
cd /root/jarvis_core
source venv/bin/activate
python3 << 'PYEND'
from ai.orchestrator import AIOrchestrator, AIProvider
ai = AIOrchestrator()
print('Health:', ai.health_check())
result = ai.chat('Hi', provider=AIProvider.LOCAL)
print('Local AI Response:', result.get('response', '')[:50])
print('AI Orchestrator WORKS!')
PYEND
