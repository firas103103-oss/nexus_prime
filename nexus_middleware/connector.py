"""
═══════════════════════════════════════════════════════════════════════════════
THE UNIFIED NEXUS CONNECTOR
═══════════════════════════════════════════════════════════════════════════════
العصب الرئيسي للتواصل مع غرفة الاجتماعات والوكلاء
This is the neural pathway connecting Dashboard, CLI, and the Boardroom
═══════════════════════════════════════════════════════════════════════════════
"""

import httpx
import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

class NexusMasterConnector:
    """
    The Master Connector - يربط كل أجزاء الإمبراطورية ببعضها
    
    Usage:
        connector = NexusMasterConnector()
        result = await connector.collective_chat("AI-ARCH", "Optimize the central core")
    """
    
    def __init__(self, base_url: str = None):
        # Auto-detect the best endpoint
        self.base_url = base_url or os.getenv(
            "NEXUS_API_URL", 
            "https://nerve.mrf103.com"
        )
        # Multiple fallback URLs
        self.internal_urls = [
            "http://nexus_nerve:8200",      # Docker internal
            "http://localhost:8200",         # Local development
            "http://127.0.0.1:8200"          # Direct localhost
        ]
        self.timeout = httpx.Timeout(60.0, connect=10.0)
        self.master_key = os.getenv("NEXUS_MASTER_KEY", "sk-nexus-sovereign-mrf103")
        
    def _get_headers(self) -> Dict[str, str]:
        """Headers for authenticated requests"""
        return {
            "Authorization": f"Bearer {self.master_key}",
            "Content-Type": "application/json",
            "X-Nexus-Source": "MasterConnector"
        }
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Unified request handler with fallback"""
        # Try external URL first, then internal fallbacks
        urls_to_try = [self.base_url] + self.internal_urls
        last_error = None
        
        for url in urls_to_try:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    full_url = f"{url}{endpoint}"
                    response = await client.request(
                        method,
                        full_url,
                        headers=self._get_headers(),
                        **kwargs
                    )
                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code < 500:
                        return {"error": response.text, "status": response.status_code}
                    # 5xx errors - try next URL
                    last_error = f"HTTP {response.status_code}"
            except httpx.ConnectError as e:
                last_error = f"Connection failed: {str(e)[:50]}"
                continue
            except httpx.TimeoutException:
                last_error = "Request timeout"
                continue
            except Exception as e:
                last_error = str(e)[:100]
                continue
        
        return {"error": f"All endpoints unreachable. Last: {last_error}", "status": 503}

    # ═══════════════════════════════════════════════════════════════════════════
    # BOARDROOM OPERATIONS - غرفة الاجتماعات
    # ═══════════════════════════════════════════════════════════════════════════

    async def summon_to_boardroom(self, agent_id: str) -> Dict[str, Any]:
        """
        استدعاء وكيل معين لغرفة الاجتماعات بكل صلاحياته
        Summon an agent to the boardroom with full capabilities
        """
        return await self._request("GET", f"/api/boardroom/summon/{agent_id}")

    async def collective_chat(self, agent_id: str, message: str, 
                             context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        تحدث مع الوكيل ضمن سياق الوعي الجمعي
        Chat with agent within collective consciousness context
        """
        payload = {
            "agent_id": agent_id,
            "message": message
        }
        return await self._request("POST", "/api/boardroom/chat", json=payload)

    async def get_boardroom_roster(self) -> Dict[str, Any]:
        """
        قائمة جميع الوكلاء المتاحين للاستدعاء
        List all agents available for summoning
        """
        return await self._request("GET", "/api/boardroom/roster")

    async def multi_agent_council(self, agent_ids: List[str], 
                                  topic: str) -> Dict[str, Any]:
        """
        استدعاء مجلس من عدة وكلاء لمناقشة موضوع معين
        Summon multiple agents for a council discussion
        """
        payload = {
            "agents": agent_ids,
            "topic": topic,
            "mode": "council",
            "timestamp": datetime.utcnow().isoformat()
        }
        return await self._request("POST", "/api/boardroom/council", json=payload)
    
    async def broadcast_directive(self, message: str, 
                                  priority: str = "normal") -> Dict[str, Any]:
        """
        بث توجيه لجميع الوكلاء
        Broadcast a directive to all agents
        """
        payload = {
            "message": message,
            "priority": priority,  # normal, high, critical
            "source": "ARCHITECT",
            "timestamp": datetime.utcnow().isoformat()
        }
        return await self._request("POST", "/api/command", json=payload)

    # ═══════════════════════════════════════════════════════════════════════════
    # SYSTEM PULSE - نبض النظام
    # ═══════════════════════════════════════════════════════════════════════════

    async def get_system_pulse(self) -> Dict[str, Any]:
        """
        قراءة نبض الإمبراطورية لحظياً
        Read the empire's pulse in real-time
        """
        return await self._request("GET", "/api/pulse")

    async def get_system_overview(self) -> Dict[str, Any]:
        """Get comprehensive system overview"""
        return await self._request("GET", "/api/overview")

    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed status of a specific agent (genome)"""
        return await self._request("GET", f"/api/genome/{agent_id}")

    async def get_all_agents(self) -> Dict[str, Any]:
        """Get list of all registered agents"""
        return await self._request("GET", "/api/agents")

    # ═══════════════════════════════════════════════════════════════════════════
    # HR REGISTRY OPERATIONS - سجلات الموظفين
    # ═══════════════════════════════════════════════════════════════════════════

    async def get_agent_profile(self, agent_id: str) -> Dict[str, Any]:
        """Get full profile for an agent via boardroom summon"""
        return await self._request("GET", f"/api/boardroom/summon/{agent_id}")

    async def get_agent_genome(self, agent_id: str) -> Dict[str, Any]:
        """Get agent's genome (evolution stats)"""
        return await self._request("GET", f"/api/genome/{agent_id}")

    async def evolve_agent(self, agent_id: str, event_type: str = "task_complete") -> Dict[str, Any]:
        """Trigger agent evolution event"""
        payload = {"event_type": event_type}
        return await self._request("POST", f"/api/genome/{agent_id}/evolve", json=payload)

    # ═══════════════════════════════════════════════════════════════════════════
    # ORACLE OPERATIONS - ذاكرة الـ RAG
    # ═══════════════════════════════════════════════════════════════════════════

    async def query_oracle(self, query: str, 
                          context_limit: int = 5) -> Dict[str, Any]:
        """
        استعلام من الـ Oracle (RAG Memory) via external endpoint
        Query the Oracle for accumulated wisdom
        """
        payload = {
            "query": query,
            "limit": context_limit
        }
        # Oracle is on a different port
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post("http://localhost:8100/api/query", json=payload)
                return resp.json()
        except:
            return {"error": "Oracle service unavailable"}

    # ═══════════════════════════════════════════════════════════════════════════
    # AUTOPILOT & BOMB OPERATIONS - القنابل الذرية
    # ═══════════════════════════════════════════════════════════════════════════

    async def deploy_bombs(self, manuscript_title: str = "Sovereign Directive") -> Dict[str, Any]:
        """
        تفعيل جميع القنابل الخمس - تشغيل الطيار الآلي
        Deploy all 5 atomic bombs - AUTOPILOT MODE
        """
        return await self._request("POST", "/api/autopilot/trigger", 
                                   params={"manuscript_title": manuscript_title})

    async def trigger_autopilot(self, manuscript_title: str = "Untitled") -> Dict[str, Any]:
        """Trigger the Shadow Autopilot Pipeline"""
        return await self._request("POST", "/api/autopilot/trigger",
                                   params={"manuscript_title": manuscript_title})

    async def send_command(self, command: str) -> Dict[str, Any]:
        """Send a natural language command to the system"""
        return await self._request("POST", "/api/command", json={"text": command})


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON INSTANCE FOR QUICK ACCESS
# ═══════════════════════════════════════════════════════════════════════════════

_connector_instance = None

def get_connector() -> NexusMasterConnector:
    """Get singleton connector instance"""
    global _connector_instance
    if _connector_instance is None:
        _connector_instance = NexusMasterConnector()
    return _connector_instance
