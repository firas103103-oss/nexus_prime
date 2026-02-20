"""
═══════════════════════════════════════════════════════════════════════════════
NEXUS PRIME — Meta-Orchestrator gRPC Server
═══════════════════════════════════════════════════════════════════════════════
The central brain of the Multi-Agent Swarm Intelligence architecture.
Sits ABOVE the existing Cortex (FastAPI), wrapping it as a downstream service.

Agents connect via bidirectional gRPC Pulse streams. The orchestrator bridges:
  gRPC agents ←→ Cortex REST API ←→ existing REST agents

Port: 50051  |  Protocol: gRPC (HTTP/2)  |  Async: uvloop + grpc.aio
═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import json
import logging
import os
import random
import signal
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Set

import grpc
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health_pb2, health_pb2_grpc
from grpc_health.v1.health import HealthServicer
import httpx
import redis.asyncio as aioredis
from google.protobuf import timestamp_pb2, struct_pb2, empty_pb2
import json

# ── Proto imports (compiled from nexus_pulse.proto) ──────────────────────────
import nexus_pulse_pb2 as pb
import nexus_pulse_pb2_grpc as pb_grpc

# ── Configuration ────────────────────────────────────────────────────────────
CORTEX_URL   = os.getenv("CORTEX_URL", "http://nexus_cortex:8090")
REDIS_URL    = os.getenv("REDIS_URL", "redis://nexus_redis:6379/0")
GRPC_PORT    = int(os.getenv("GRPC_PORT", "50051"))
MAX_WORKERS  = int(os.getenv("MAX_WORKERS", "10"))

# Staleness: if no pulse in N seconds, mark agent offline
STALENESS_THRESHOLD_SEC = int(os.getenv("STALENESS_THRESHOLD", "60"))
STALENESS_CHECK_INTERVAL = int(os.getenv("STALENESS_CHECK_INTERVAL", "15"))

# Heartbeat ACK
HEARTBEAT_ACK_ENABLED = os.getenv("HEARTBEAT_ACK", "true").lower() == "true"

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(name)-20s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("nexus.orchestrator")
log_pulse = logging.getLogger("nexus.pulse")
log_bridge = logging.getLogger("nexus.cortex_bridge")
log_redis = logging.getLogger("nexus.redis_bridge")


# ═════════════════════════════════════════════════════════════════════════════
# CORTEX BRIDGE — HTTP proxy to existing FastAPI Cortex
# ═════════════════════════════════════════════════════════════════════════════

class CortexBridge:
    """Async HTTP bridge to the existing Cortex REST API (port 8090)."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._client: Optional[httpx.AsyncClient] = None

    async def start(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(10.0, connect=5.0),
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=20),
        )
        log_bridge.info(f"Cortex bridge connected → {self.base_url}")

    async def stop(self):
        if self._client:
            await self._client.aclose()
            log_bridge.info("Cortex bridge closed")

    @property
    def client(self) -> httpx.AsyncClient:
        assert self._client is not None, "CortexBridge not started"
        return self._client

    async def health(self) -> dict:
        """GET /health"""
        try:
            r = await self.client.get("/health")
            return r.json()
        except Exception as e:
            log_bridge.error(f"Cortex health check failed: {e}")
            return {"cortex": "unreachable", "error": str(e)}

    async def register_agent(self, name: str, display_name: str,
                              agent_type: str, capabilities: list,
                              endpoint: str) -> dict:
        """POST /agent/register"""
        body = {
            "name": name,
            "display_name": display_name or name,
            "agent_type": agent_type,
            "capabilities": capabilities,
            "endpoint": endpoint,
        }
        try:
            r = await self.client.post("/agent/register", json=body)
            r.raise_for_status()
            log_bridge.info(f"Registered agent via Cortex: {name}")
            return r.json()
        except Exception as e:
            log_bridge.error(f"Agent registration failed for {name}: {e}")
            return {"error": str(e)}

    async def heartbeat(self, agent_name: str, current_task: str = None,
                         metrics: dict = None) -> dict:
        """POST /agent/{name}/heartbeat"""
        body = {
            "current_task": current_task,
            "metrics": metrics or {},
        }
        try:
            r = await self.client.post(f"/agent/{agent_name}/heartbeat", json=body)
            return r.json()
        except Exception as e:
            log_bridge.warning(f"Heartbeat relay failed for {agent_name}: {e}")
            return {"error": str(e)}

    async def submit_command(self, command_type: str, origin: str,
                              target_agent: str = None, payload: dict = None,
                              priority: int = 5) -> dict:
        """POST /command"""
        body = {
            "command_type": command_type,
            "origin": origin,
            "target_agent": target_agent,
            "payload": payload or {},
            "priority": priority,
        }
        try:
            r = await self.client.post("/command", json=body)
            r.raise_for_status()
            data = r.json()
            log_bridge.info(f"Command submitted: {data.get('command_id')} → {target_agent or 'auto-route'}")
            return data
        except Exception as e:
            log_bridge.error(f"Command submission failed: {e}")
            return {"error": str(e)}

    async def update_command(self, command_id: str, status: str,
                              result: dict = None,
                              error_msg: str = None) -> dict:
        """PATCH /command/{id}"""
        body = {"status": status}
        if result:
            body["result"] = result
        if error_msg:
            body["error_msg"] = error_msg
        try:
            r = await self.client.patch(f"/command/{command_id}", json=body)
            return r.json()
        except Exception as e:
            log_bridge.warning(f"Command update failed for {command_id}: {e}")
            return {"error": str(e)}

    async def post_event(self, agent_name: str, event_type: str,
                          severity: str = "info", title: str = None,
                          body: dict = None, command_id: str = None) -> dict:
        """POST /event"""
        event = {
            "agent_name": agent_name,
            "event_type": event_type,
            "severity": severity,
            "title": title,
            "body": body or {},
        }
        if command_id:
            event["command_id"] = command_id
        try:
            r = await self.client.post("/event", json=event)
            return r.json()
        except Exception as e:
            log_bridge.warning(f"Event post failed: {e}")
            return {"error": str(e)}

    async def get_dashboard(self) -> dict:
        """GET /dashboard"""
        try:
            r = await self.client.get("/dashboard")
            return r.json()
        except Exception as e:
            log_bridge.error(f"Dashboard fetch failed: {e}")
            return {"error": str(e)}

    async def get_agents(self) -> list:
        """GET /agents"""
        try:
            r = await self.client.get("/agents")
            data = r.json()
            return data.get("agents", [])
        except Exception as e:
            log_bridge.error(f"Agents fetch failed: {e}")
            return []


# ═════════════════════════════════════════════════════════════════════════════
# CONNECTED AGENT TRACKER
# ═════════════════════════════════════════════════════════════════════════════

class ConnectedAgent:
    """Tracks a single gRPC-connected agent's state."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.connected_at = time.monotonic()
        self.last_pulse_at = time.monotonic()
        self.directive_queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        self.sequence_out: int = 0
        self.pulse_count: int = 0
        self.status = pb.AGENT_STATUS_IDLE

    def touch(self):
        self.last_pulse_at = time.monotonic()
        self.pulse_count += 1

    @property
    def idle_seconds(self) -> float:
        return time.monotonic() - self.last_pulse_at

    def next_sequence(self) -> int:
        self.sequence_out += 1
        return self.sequence_out


# ═════════════════════════════════════════════════════════════════════════════
# gRPC SERVICE IMPLEMENTATION — NexusPulseServicer
# ═════════════════════════════════════════════════════════════════════════════

class NexusPulseServicer(pb_grpc.NexusPulseServiceServicer):
    """
    Production-ready Meta-Orchestrator.
    Bridges gRPC Pulse streams ←→ Cortex REST API.
    """

    def __init__(self, cortex: CortexBridge, redis_client: aioredis.Redis):
        self.cortex = cortex
        self.redis = redis_client
        self.connected_agents: Dict[str, ConnectedAgent] = {}
        self._shutting_down = False
        self._stats = {
            "total_pulses": 0,
            "total_directives": 0,
            "total_registrations": 0,
            "total_commands": 0,
            "server_start": time.time(),
        }
        log.info("NexusPulseServicer initialized")

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _now_ts() -> timestamp_pb2.Timestamp:
        ts = timestamp_pb2.Timestamp()
        ts.FromDatetime(datetime.now(timezone.utc))
        return ts

    @staticmethod
    def _struct_from_dict(d: dict) -> struct_pb2.Struct:
        s = struct_pb2.Struct()
        if d:
            s.update(d)
        return s

    @staticmethod
    def _struct_to_dict(s: struct_pb2.Struct) -> dict:
        from google.protobuf.json_format import MessageToDict
        return MessageToDict(s) if s.fields else {}

    @staticmethod
    def _agent_type_to_str(at: int) -> str:
        return {
            pb.AGENT_TYPE_PLANET: "planet",
            pb.AGENT_TYPE_SERVICE: "service",
            pb.AGENT_TYPE_HUMAN: "human",
            pb.AGENT_TYPE_SWARM: "swarm",
        }.get(at, "planet")

    @staticmethod
    def _str_to_agent_status(s: str) -> int:
        return {
            "online": pb.AGENT_STATUS_IDLE,
            "idle": pb.AGENT_STATUS_IDLE,
            "busy": pb.AGENT_STATUS_BUSY,
            "error": pb.AGENT_STATUS_ERROR,
            "offline": pb.AGENT_STATUS_OFFLINE,
        }.get(s, pb.AGENT_STATUS_UNSPECIFIED)

    def _make_ack_directive(self, pulse_id: str, message: str,
                             correlation_id: str = "") -> pb.OrchestratorDirective:
        """Create an ACK directive for a received pulse."""
        agent_conn = None
        # find agent for sequence
        return pb.OrchestratorDirective(
            directive_id=str(uuid.uuid4()),
            directive_type=pb.DIRECTIVE_TYPE_ACK,
            timestamp=self._now_ts(),
            ack_for_pulse_id=pulse_id,
            message=message,
            correlation_id=correlation_id,
        )

    # ── RPC: Bidirectional Pulse Stream ──────────────────────────────────────

    async def Pulse(self, request_iterator, context):
        """
        Core bidirectional stream. Agent sends pulses, receives directives.
        This is THE heartbeat of the swarm intelligence.
        """
        agent_id = None
        agent_conn = None

        async def _send_directives():
            """Background coroutine: dequeue directives and yield to agent."""
            nonlocal agent_conn
            try:
                while not self._shutting_down:
                    try:
                        directive = await asyncio.wait_for(
                            agent_conn.directive_queue.get(), timeout=1.0
                        )
                        directive.sequence_number = agent_conn.next_sequence()
                        self._stats["total_directives"] += 1
                        await context.write(directive)
                    except asyncio.TimeoutError:
                        continue
                    except asyncio.CancelledError:
                        break
            except Exception as e:
                log.warning(f"Directive sender for {agent_id} ended: {e}")

        sender_task = None

        try:
            async for pulse in request_iterator:
                # First pulse identifies the agent
                if agent_id is None:
                    agent_id = pulse.agent_id
                    if not agent_id:
                        await context.abort(
                            grpc.StatusCode.INVALID_ARGUMENT,
                            "First pulse must contain agent_id"
                        )
                        return

                    # Register in connected agents
                    agent_conn = ConnectedAgent(agent_id)
                    self.connected_agents[agent_id] = agent_conn
                    log_pulse.info(
                        f"⚡ Agent connected: {agent_id} "
                        f"(total: {len(self.connected_agents)})"
                    )

                    # Start directive sender coroutine
                    sender_task = asyncio.create_task(_send_directives())

                    # Send welcome ACK
                    welcome = pb.OrchestratorDirective(
                        directive_id=str(uuid.uuid4()),
                        directive_type=pb.DIRECTIVE_TYPE_ACK,
                        timestamp=self._now_ts(),
                        message=f"Welcome to NEXUS PRIME, {agent_id}. Pulse stream active.",
                        system_state=await self._build_system_snapshot(),
                    )
                    await agent_conn.directive_queue.put(welcome)

                # Process pulse
                agent_conn.touch()
                self._stats["total_pulses"] += 1

                await self._process_pulse(agent_id, pulse, agent_conn)

        except asyncio.CancelledError:
            log_pulse.info(f"Pulse stream cancelled for {agent_id}")
        except Exception as e:
            log_pulse.error(f"Pulse stream error for {agent_id}: {e}")
        finally:
            # Cleanup
            if sender_task:
                sender_task.cancel()
                try:
                    await sender_task
                except asyncio.CancelledError:
                    pass

            if agent_id and agent_id in self.connected_agents:
                del self.connected_agents[agent_id]
                log_pulse.info(
                    f"🔌 Agent disconnected: {agent_id} "
                    f"(remaining: {len(self.connected_agents)})"
                )
                # Mark offline in Cortex
                await self.cortex.post_event(
                    agent_name=agent_id,
                    event_type="info",
                    severity="medium",
                    title=f"Agent {agent_id} disconnected from gRPC Pulse",
                )

    async def _process_pulse(self, agent_id: str, pulse: pb.AgentPulse,
                              conn: ConnectedAgent):
        """Route incoming pulse to appropriate handler."""
        pt = pulse.pulse_type

        if pt == pb.PULSE_TYPE_HEARTBEAT:
            metrics = {}
            if pulse.state and pulse.state.metrics:
                m = pulse.state.metrics
                metrics = {
                    "cpu": m.cpu_usage_percent,
                    "memory": m.memory_usage_percent,
                    "latency_ms": m.request_latency_ms,
                    "active_tasks": m.active_tasks,
                }
            current_task = pulse.state.current_task if pulse.state else None
            await self.cortex.heartbeat(agent_id, current_task, metrics)

            if HEARTBEAT_ACK_ENABLED:
                ack = self._make_ack_directive(
                    str(pulse.sequence_number),
                    f"Heartbeat #{conn.pulse_count} received",
                    pulse.correlation_id,
                )
                await conn.directive_queue.put(ack)

        elif pt == pb.PULSE_TYPE_REGISTRATION:
            await self.cortex.register_agent(
                name=agent_id,
                display_name=pulse.display_name or agent_id,
                agent_type=self._agent_type_to_str(pulse.agent_type),
                capabilities=list(pulse.capabilities),
                endpoint=pulse.endpoint,
            )
            self._stats["total_registrations"] += 1
            ack = self._make_ack_directive(
                str(pulse.sequence_number),
                f"Agent {agent_id} registered via Pulse stream",
                pulse.correlation_id,
            )
            await conn.directive_queue.put(ack)

        elif pt == pb.PULSE_TYPE_TASK_RESULT:
            if pulse.result and pulse.result.command_id:
                status_map = {
                    pb.TASK_STATUS_SUCCESS: "done",
                    pb.TASK_STATUS_FAILED: "failed",
                    pb.TASK_STATUS_PARTIAL: "running",
                    pb.TASK_STATUS_RUNNING: "running",
                }
                cortex_status = status_map.get(pulse.result.status, "done")
                output = self._struct_to_dict(pulse.result.output)
                await self.cortex.update_command(
                    command_id=pulse.result.command_id,
                    status=cortex_status,
                    result=output,
                    error_msg=pulse.result.error_message or None,
                )
                log_pulse.info(
                    f"Task result from {agent_id}: "
                    f"{pulse.result.command_id} → {cortex_status} "
                    f"({pulse.result.execution_time_ms}ms)"
                )

        elif pt == pb.PULSE_TYPE_ERROR:
            await self.cortex.post_event(
                agent_name=agent_id,
                event_type="error",
                severity="high",
                title=f"Error from {agent_id}: {pulse.error_code}",
                body={
                    "code": pulse.error_code,
                    "message": pulse.error_message,
                    "stack_trace": pulse.error_stack_trace,
                },
            )
            log_pulse.error(f"Error from {agent_id}: {pulse.error_message}")

        elif pt == pb.PULSE_TYPE_INTENT:
            if pulse.intent:
                payload = self._struct_to_dict(pulse.intent.payload)
                result = await self.cortex.submit_command(
                    command_type=pulse.intent.requested_action,
                    origin=agent_id,
                    target_agent=pulse.intent.target_agent or None,
                    payload=payload,
                    priority=pulse.intent.priority or 5,
                )
                ack = self._make_ack_directive(
                    str(pulse.sequence_number),
                    f"Intent routed: {result.get('command_id', 'unknown')}",
                    pulse.correlation_id,
                )
                await conn.directive_queue.put(ack)

        elif pt == pb.PULSE_TYPE_STATE_UPDATE:
            if pulse.state:
                conn.status = pulse.state.status
                metrics = {}
                if pulse.state.metrics:
                    m = pulse.state.metrics
                    metrics = {
                        "cpu": m.cpu_usage_percent,
                        "memory": m.memory_usage_percent,
                    }
                await self.cortex.heartbeat(agent_id, pulse.state.current_task, metrics)

    # ── RPC: RegisterAgent (Unary) ───────────────────────────────────────────

    async def RegisterAgent(self, request, context):
        """One-shot agent registration. Wraps Cortex POST /agent/register."""
        result = await self.cortex.register_agent(
            name=request.name,
            display_name=request.display_name or request.name,
            agent_type=self._agent_type_to_str(request.agent_type),
            capabilities=list(request.capabilities),
            endpoint=request.endpoint,
        )
        self._stats["total_registrations"] += 1

        if "error" in result:
            return pb.RegistrationAck(
                success=False,
                agent_id=request.name,
                message=f"Registration failed: {result['error']}",
            )

        log.info(f"Agent registered (unary): {request.name}")
        return pb.RegistrationAck(
            success=True,
            agent_id=request.name,
            message=f"Agent {request.name} registered successfully",
            registered_at=self._now_ts(),
            system_state=await self._build_system_snapshot(),
        )

    # ── RPC: SubmitCommand (Unary) ───────────────────────────────────────────

    async def SubmitCommand(self, request, context):
        """Submit a task command for routing. Wraps Cortex POST /command."""
        payload = self._struct_to_dict(request.payload)
        result = await self.cortex.submit_command(
            command_type=request.command_type,
            origin=request.origin or "grpc_client",
            target_agent=None,  # let routing rules decide
            payload=payload,
            priority=request.priority or 5,
        )
        self._stats["total_commands"] += 1

        if "error" in result:
            return pb.CommandAck(
                success=False,
                message=f"Command failed: {result['error']}",
            )

        cmd_id = result.get("command_id", "")
        target = result.get("target_agent", "auto-routed")

        # If target agent is gRPC-connected, push directive directly
        if target and target in self.connected_agents:
            directive = pb.OrchestratorDirective(
                directive_id=str(uuid.uuid4()),
                directive_type=pb.DIRECTIVE_TYPE_EXECUTE_TASK,
                timestamp=self._now_ts(),
                command=pb.TaskCommand(
                    command_id=cmd_id,
                    command_type=request.command_type,
                    origin=request.origin,
                    payload=request.payload,
                    priority=request.priority,
                ),
                routing=pb.RoutingInfo(target_agent=target),
            )
            await self.connected_agents[target].directive_queue.put(directive)
            log.info(f"Command {cmd_id} pushed directly to gRPC agent {target}")

        return pb.CommandAck(
            success=True,
            command_id=cmd_id,
            target_agent=target,
            status=pb.TASK_STATUS_QUEUED,
            message="Command queued successfully",
        )

    # ── RPC: GetSystemStatus (Unary) ─────────────────────────────────────────

    async def GetSystemStatus(self, request, context):
        """Returns current NEXUS PRIME cluster state."""
        return await self._build_system_snapshot()

    async def _build_system_snapshot(self) -> pb.SystemSnapshot:
        """Build system snapshot from Cortex dashboard + local gRPC state."""
        dashboard = await self.cortex.get_dashboard()
        stats = dashboard.get("stats", {})
        cortex_agents = dashboard.get("agents", [])

        agent_summaries = []
        for a in cortex_agents:
            ts = timestamp_pb2.Timestamp()
            if a.get("last_seen"):
                try:
                    dt = datetime.fromisoformat(a["last_seen"].replace("Z", "+00:00"))
                    ts.FromDatetime(dt)
                except Exception:
                    pass

            caps = a.get("capabilities", [])
            if isinstance(caps, str):
                try:
                    caps = json.loads(caps)
                except Exception:
                    caps = []

            agent_summaries.append(pb.AgentSummary(
                name=a.get("name", ""),
                display_name=a.get("display_name", a.get("name", "")),
                status=self._str_to_agent_status(a.get("status", "offline")),
                agent_type=pb.AGENT_TYPE_PLANET if a.get("agent_type") == "planet" else pb.AGENT_TYPE_SERVICE,
                last_seen=ts,
                current_task=a.get("current_task", ""),
                capabilities=caps,
            ))

        return pb.SystemSnapshot(
            online_agents=stats.get("online_count", len(self.connected_agents)),
            total_agents=len(cortex_agents) if cortex_agents else len(self.connected_agents),
            queued_commands=stats.get("queued_commands", 0),
            running_commands=stats.get("running_commands", 0),
            timestamp=self._now_ts(),
            agents=agent_summaries,
        )


# ═════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════
# REDIS BRIDGE — Subscribe to Redis Streams with Consumer Groups
# ═════════════════════════════════════════════════════════════════════════════

class RedisBridge:
    """
    Production-grade Redis Streams consumer with Consumer Groups.
    Prevents duplicate command processing when scaling orchestrator to 3+ replicas.
    
    Features:
      ✅ Consumer Groups - only one consumer processes each message
      ✅ ACK mechanism - ensures delivery semantics
      ✅ Dead Letter Queue - moves failed messages after 3 retries
      ✅ Stream trimming - prevents memory overflow
      ✅ Backward compatible - also subscribes to legacy Pub/Sub channels
    """

    def __init__(self, redis_client: aioredis.Redis,
                 servicer: NexusPulseServicer):
        self.redis = redis_client
        self.servicer = servicer
        self._running = False
        
        # Stream configuration
        self.stream_name = "nexus:commands:stream"
        self.group_name = "orchestrator_group"
        self.consumer_name = f"orch_pod_{os.getpid()}"
        self.dlq_stream = "nexus:commands:dlq"
        
        # Retry tracking
        self.retry_counts = {}  # msg_id -> count
        self.max_retries = 3

    async def start(self):
        self._running = True
        
        # Create consumer group (idempotent - won't fail if exists)
        try:
            await self.redis.xgroup_create(
                self.stream_name, 
                self.group_name, 
                id='0',
                mkstream=True
            )
            log_redis.info(f"✅ Consumer group '{self.group_name}' created")
        except aioredis.ResponseError as e:
            if "BUSYGROUP" in str(e):
                log_redis.info(f"Consumer group '{self.group_name}' already exists")
            else:
                raise
        
        # Start stream consumer
        asyncio.create_task(self._stream_consumer_loop())
        
        # Start legacy Pub/Sub listener (backward compatibility)
        asyncio.create_task(self._legacy_pubsub_loop())
        
        log_redis.info(
            f"Redis Streams bridge started — "
            f"Stream: {self.stream_name} | "
            f"Group: {self.group_name} | "
            f"Consumer: {self.consumer_name}"
        )

    async def stop(self):
        self._running = False

    async def _stream_consumer_loop(self):
        """Consume messages from Redis Streams with XREADGROUP."""
        retry_delay = 1
        
        while self._running:
            try:
                # Read new messages from stream (blocking call with 2s timeout)
                messages = await self.redis.xreadgroup(
                    self.group_name,
                    self.consumer_name,
                    {self.stream_name: '>'},  # '>' means new undelivered messages
                    count=10,  # Process up to 10 messages per batch
                    block=2000  # 2-second block timeout
                )
                
                retry_delay = 1  # Reset on success
                
                # Process messages
                for stream, msgs in messages:
                    for msg_id, data in msgs:
                        await self._process_stream_message(msg_id, data)
                
                # Periodic stream trimming to prevent memory overflow
                if random.random() < 0.1:  # 10% chance each loop
                    await self._trim_stream()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                log_redis.error(f"Stream consumer error: {e}, retrying in {retry_delay}s")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 30)

    async def _process_stream_message(self, msg_id, data: dict):
        """Process a single stream message."""
        try:
            # Decode byte strings
            decoded_data = {}
            for k, v in data.items():
                key = k.decode() if isinstance(k, bytes) else k
                value = v.decode() if isinstance(v, bytes) else v
                decoded_data[key] = value
            
            # Parse JSON payload
            message_type = decoded_data.get("type", "")
            target = decoded_data.get("target", "")
            
            if message_type == "command_issued" and target:
                # Check if agent is connected via gRPC
                if target in self.servicer.connected_agents:
                    # Parse command details
                    command_id = decoded_data.get("command_id", "")
                    command_type = decoded_data.get("command_type", "")
                    priority = int(decoded_data.get("priority", "5"))
                    
                    # Create gRPC directive
                    directive = pb.OrchestratorDirective(
                        directive_id=str(uuid.uuid4()),
                        directive_type=pb.DIRECTIVE_TYPE_EXECUTE_TASK,
                        timestamp=self.servicer._now_ts(),
                        command=pb.TaskCommand(
                            command_id=command_id,
                            command_type=command_type,
                            origin="cortex_redis_streams",
                            priority=priority,
                        ),
                        routing=pb.RoutingInfo(target_agent=target),
                        message=f"Task from Redis Streams: {command_type}",
                    )
                    
                    # Route to agent
                    await self.servicer.connected_agents[target].directive_queue.put(directive)
                    log_redis.info(
                        f"✅ Redis Streams → gRPC: {command_id} → {target} "
                        f"(msg_id: {msg_id.decode() if isinstance(msg_id, bytes) else msg_id})"
                    )
                    
                    # ACK message - successfully processed
                    await self.redis.xack(self.stream_name, self.group_name, msg_id)
                    
                    # Clear retry count
                    if msg_id in self.retry_counts:
                        del self.retry_counts[msg_id]
                else:
                    # Agent not connected via gRPC - will be handled by REST fallback
                    log_redis.debug(f"Agent {target} not connected via gRPC, skipping")
                    await self.redis.xack(self.stream_name, self.group_name, msg_id)
            else:
                # Unknown message type or missing target - ACK to avoid reprocessing
                log_redis.debug(f"Unknown message type: {message_type}, ACKing")
                await self.redis.xack(self.stream_name, self.group_name, msg_id)
                
        except Exception as e:
            log_redis.error(f"Failed to process message {msg_id}: {e}")
            
            # Track retry count
            if msg_id not in self.retry_counts:
                self.retry_counts[msg_id] = 0
            self.retry_counts[msg_id] += 1
            
            # Move to DLQ after max retries
            if self.retry_counts[msg_id] >= self.max_retries:
                log_redis.warning(
                    f"⚠️  Message {msg_id} failed {self.max_retries} times, "
                    f"moving to DLQ: {self.dlq_stream}"
                )
                try:
                    # Copy to DLQ
                    await self.redis.xadd(self.dlq_stream, data)
                    # ACK original message
                    await self.redis.xack(self.stream_name, self.group_name, msg_id)
                    # Clear retry count
                    del self.retry_counts[msg_id]
                except Exception as dlq_error:
                    log_redis.error(f"Failed to move message to DLQ: {dlq_error}")

    async def _trim_stream(self):
        """Trim stream to prevent unbounded growth."""
        try:
            # Keep last 10,000 messages (approximate)
            await self.redis.xtrim(
                self.stream_name, 
                maxlen=10000, 
                approximate=True
            )
            log_redis.debug(f"Stream trimmed: {self.stream_name}")
        except Exception as e:
            log_redis.warning(f"Failed to trim stream: {e}")

    async def _legacy_pubsub_loop(self):
        """
        Legacy Pub/Sub listener for backward compatibility.
        Runs in parallel with Streams consumer.
        """
        retry_delay = 1
        while self._running:
            try:
                pubsub = self.redis.pubsub()
                await pubsub.subscribe("nexus:events", "nexus:agents")
                retry_delay = 1

                async for msg in pubsub.listen():
                    if not self._running:
                        break
                    if msg["type"] != "message":
                        continue

                    channel = msg["channel"]
                    if isinstance(channel, bytes):
                        channel = channel.decode()

                    try:
                        data = json.loads(msg["data"])
                    except (json.JSONDecodeError, TypeError):
                        continue

                    # Only handle non-command channels (commands now via Streams)
                    if channel == "nexus:events":
                        log_redis.debug(f"Event: {data}")
                    elif channel == "nexus:agents":
                        log_redis.debug(f"Agent event: {data}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                log_redis.error(f"Legacy Pub/Sub error: {e}, retrying in {retry_delay}s")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 30)



# ═════════════════════════════════════════════════════════════════════════════
# STALENESS REAPER — Detects dead agents
# ═════════════════════════════════════════════════════════════════════════════

class StalenessReaper:
    """
    Background task that monitors connected agents for pulse staleness.
    If an agent hasn't sent a pulse within STALENESS_THRESHOLD_SEC,
    marks it offline via Cortex — filling the production gap.
    """

    def __init__(self, servicer: NexusPulseServicer, cortex: CortexBridge):
        self.servicer = servicer
        self.cortex = cortex
        self._running = False

    async def start(self):
        self._running = True
        asyncio.create_task(self._reap_loop())
        log.info(f"Staleness reaper active (threshold: {STALENESS_THRESHOLD_SEC}s)")

    async def stop(self):
        self._running = False

    async def _reap_loop(self):
        while self._running:
            await asyncio.sleep(STALENESS_CHECK_INTERVAL)
            stale_agents = []

            for agent_id, conn in list(self.servicer.connected_agents.items()):
                if conn.idle_seconds > STALENESS_THRESHOLD_SEC:
                    stale_agents.append(agent_id)

            for agent_id in stale_agents:
                log.warning(
                    f"⚠️ Agent {agent_id} stale "
                    f"({self.servicer.connected_agents[agent_id].idle_seconds:.0f}s silent) "
                    f"— marking offline"
                )
                await self.cortex.post_event(
                    agent_name=agent_id,
                    event_type="alert",
                    severity="high",
                    title=f"Agent {agent_id} marked offline (no pulse for {STALENESS_THRESHOLD_SEC}s)",
                )
                # Remove from connected pool
                if agent_id in self.servicer.connected_agents:
                    del self.servicer.connected_agents[agent_id]


# ═════════════════════════════════════════════════════════════════════════════
# SERVER BOOTSTRAP
# ═════════════════════════════════════════════════════════════════════════════

async def serve():
    """Initialize and run the Meta-Orchestrator gRPC server."""

    # ── Banner ───────────────────────────────────────────────────────────
    log.info("═" * 70)
    log.info("  NEXUS PRIME — Meta-Orchestrator v1.0.0")
    log.info("  Protocol: gRPC (HTTP/2) | Port: %d", GRPC_PORT)
    log.info("  Cortex Bridge: %s", CORTEX_URL)
    log.info("  Redis Bridge: %s", REDIS_URL)
    log.info("═" * 70)

    # ── Initialize clients ───────────────────────────────────────────────
    cortex = CortexBridge(CORTEX_URL)
    await cortex.start()

    # Check Cortex health
    health = await cortex.health()
    if health.get("cortex") == "unreachable":
        log.warning("⚠️ Cortex not reachable — will retry on demand")
    else:
        log.info(f"✅ Cortex connected: {health}")

    # Redis
    redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
    try:
        await redis_client.ping()
        log.info("✅ Redis connected")
    except Exception as e:
        log.warning(f"⚠️ Redis not reachable: {e} — will retry")

    # ── Create servicer ──────────────────────────────────────────────────
    servicer = NexusPulseServicer(cortex, redis_client)

    # ── Create gRPC server ───────────────────────────────────────────────
    server = grpc.aio.server(
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),    # 50MB
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),
            ("grpc.keepalive_time_ms", 30000),                      # 30s keepalive ping
            ("grpc.keepalive_timeout_ms", 10000),                   # 10s timeout
            ("grpc.keepalive_permit_without_calls", True),
            ("grpc.http2.max_pings_without_data", 0),
            ("grpc.http2.min_time_between_pings_ms", 10000),
            ("grpc.http2.min_ping_interval_without_data_ms", 5000),
        ],
    )

    # Register services
    pb_grpc.add_NexusPulseServiceServicer_to_server(servicer, server)

    # Health checking
    health_servicer = HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    # Set service status (sync call — varies by grpcio version)
    _set_result = health_servicer.set(
        "nexus.prime.NexusPulseService",
        health_pb2.HealthCheckResponse.SERVING,
    )
    if asyncio.iscoroutine(_set_result):
        await _set_result

    # Server reflection (for grpcurl debugging)
    SERVICE_NAMES = (
        pb.DESCRIPTOR.services_by_name["NexusPulseService"].full_name,
        reflection.SERVICE_NAME,
        health_pb2.DESCRIPTOR.services_by_name["Health"].full_name,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Bind
    listen_addr = f"0.0.0.0:{GRPC_PORT}"
    server.add_insecure_port(listen_addr)

    # ── Start server ─────────────────────────────────────────────────────
    await server.start()
    log.info(f"🚀 Meta-Orchestrator listening on {listen_addr}")

    # ── Start background services ────────────────────────────────────────
    redis_bridge = RedisBridge(redis_client, servicer)
    await redis_bridge.start()

    reaper = StalenessReaper(servicer, cortex)
    await reaper.start()

    # ── Register self in Cortex ──────────────────────────────────────────
    await cortex.register_agent(
        name="META-ORCHESTRATOR",
        display_name="Meta-Orchestrator (gRPC)",
        agent_type="service",
        capabilities=["orchestrate", "route", "monitor", "pulse_stream"],
        endpoint=f"grpc://0.0.0.0:{GRPC_PORT}",
    )
    log.info("✅ Meta-Orchestrator registered in Cortex")

    # ── Graceful shutdown ────────────────────────────────────────────────
    shutdown_event = asyncio.Event()

    def _signal_handler():
        log.info("Shutdown signal received")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _signal_handler)

    await shutdown_event.wait()

    log.info("Shutting down gracefully...")
    servicer._shutting_down = True
    await redis_bridge.stop()
    await reaper.stop()
    await server.stop(grace=5)
    await cortex.stop()
    await redis_client.aclose()
    log.info("Meta-Orchestrator stopped. Farewell.")


# ═════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
        log.info("uvloop installed — maximum async throughput")
    except ImportError:
        log.info("uvloop not available — using default asyncio loop")

    asyncio.run(serve())
