#!/usr/bin/env python3
'''
JARVIS AI ORCHESTRATOR
Routes requests between local (Ollama) and cloud (GPT, Gemini) AI
'''
import os
import requests
import json
from typing import Optional, Dict, Any
from enum import Enum

class AIProvider(str, Enum):
    LOCAL = 'local'      # Ollama (LLaMA)
    GPT = 'gpt'          # OpenAI
    GEMINI = 'gemini'    # Google Gemini
    AUTO = 'auto'        # Smart routing

class AIOrchestrator:
    def __init__(self):
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.openai_key = os.getenv('OPENAI_API_KEY', '')
        self.gemini_key = os.getenv('GEMINI_API_KEY', '')
        
    def chat(self, prompt: str, provider: AIProvider = AIProvider.AUTO, **kwargs) -> Dict[str, Any]:
        '''Main chat interface'''
        if provider == AIProvider.AUTO:
            provider = self._smart_route(prompt)
        
        try:
            if provider == AIProvider.LOCAL:
                return self._chat_local(prompt, **kwargs)
            elif provider == AIProvider.GPT:
                return self._chat_gpt(prompt, **kwargs)
            elif provider == AIProvider.GEMINI:
                return self._chat_gemini(prompt, **kwargs)
        except Exception as e:
            # Fallback to local if cloud fails
            if provider != AIProvider.LOCAL:
                print(f'Cloud AI failed, falling back to local: {e}')
                return self._chat_local(prompt, **kwargs)
            raise
    
    def _smart_route(self, prompt: str) -> AIProvider:
        '''Decide which AI to use'''
        prompt_lower = prompt.lower()
        
        # Use local for simple/fast tasks
        if len(prompt) < 100 or any(word in prompt_lower for word in ['hello', 'hi', 'test', 'quick']):
            return AIProvider.LOCAL
        
        # Use GPT for complex coding/analysis
        if any(word in prompt_lower for word in ['code', 'debug', 'analyze', 'complex']):
            return AIProvider.GPT
        
        # Default to local (faster, free)
        return AIProvider.LOCAL
    
    def _chat_local(self, prompt: str, model: str = 'llama3.2:1b', **kwargs) -> Dict[str, Any]:
        '''Chat with local Ollama'''
        response = requests.post(
            f'{self.ollama_url}/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'provider': 'local',
                'model': model,
                'response': data.get('response', ''),
                'tokens': data.get('eval_count', 0)
            }
        else:
            raise Exception(f'Ollama error: {response.status_code}')
    
    def _chat_gpt(self, prompt: str, model: str = 'gpt-4', **kwargs) -> Dict[str, Any]:
        '''Chat with OpenAI GPT'''
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {self.openai_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': model,
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': kwargs.get('max_tokens', 500)
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'provider': 'gpt',
                'model': model,
                'response': data['choices'][0]['message']['content'],
                'tokens': data['usage']['total_tokens']
            }
        else:
            raise Exception(f'OpenAI error: {response.status_code}')
    
    def _chat_gemini(self, prompt: str, **kwargs) -> Dict[str, Any]:
        '''Chat with Gemini via LiteLLM (Data Sovereignty)'''
        litellm_url = os.getenv('LITELLM_PROXY_URL', 'http://nexus_litellm:4000')
        master_key = os.getenv('LITELLM_MASTER_KEY', 'sk-nexus-sovereign-mrf103')
        
        response = requests.post(
            f'{litellm_url}/v1/chat/completions',
            headers={'Authorization': f'Bearer {master_key}'},
            json={
                'model': 'gemini-pro',
                'messages': [{'role': 'user', 'content': prompt}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'provider': 'litellm',
                'model': 'gemini-pro',
                'response': data['choices'][0]['message']['content'],
                'tokens': data.get('usage', {}).get('total_tokens', 0)
            }
        else:
            raise Exception(f'Gemini error: {response.status_code}')
    
    def health_check(self) -> Dict[str, bool]:
        '''Check status of all AI providers'''
        status = {}
        
        # Check local
        try:
            resp = requests.get(f'{self.ollama_url}/api/tags', timeout=3)
            status['local'] = resp.status_code == 200
        except:
            status['local'] = False
        
        # Check GPT (basic validation)
        status['gpt'] = bool(self.openai_key)
        
        # Check Gemini (basic validation)
        status['gemini'] = bool(self.gemini_key)
        
