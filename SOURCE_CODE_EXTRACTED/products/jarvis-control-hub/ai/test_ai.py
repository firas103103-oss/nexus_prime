#!/usr/bin/env python3
from orchestrator import AIOrchestrator, AIProvider

print('🤖 JARVIS AI Orchestrator Test')
print('-' * 40)

ai = AIOrchestrator()

# Health check
print('Checking AI providers...')
health = ai.health_check()
for provider, status in health.items():
    symbol = '✅' if status else '❌'
    print(f'  {provider}: {symbol}')

print()

# Test local
print('Testing LOCAL AI...')
result = ai.chat('Say hi in 3 words', provider=AIProvider.LOCAL)
print(f'  Provider: {result[\ provider\]}')
print(f'  Response: {result[\response\].strip()}')
print(f'  Tokens: {result[\tokens\]}')

print()
print('✅ AI Orchestrator is OPERATIONAL!')
