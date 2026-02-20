"""
═══════════════════════════════════════════════════════════════════════════════
NEXUS PRIME — Generic Agent Client v2.0 (Production-Grade gRPC Pulse)
═══════════════════════════════════════════════════════════════════════════════
Enhanced agent client with:
  ✅ Exponential backoff reconnection
  ✅ Real system metrics (psutil)
  ✅ Production error handling
  ✅ Graceful shutdown with stream cleanup
  ✅ Correlation IDs for request tracing

Usage:
    AGENT_ID=SHADOW-7 ORCHESTRATOR_HOST=nexus-orchestrator:50051 python agent_client_v2.py

Adapt this for SHADOW-7, CLONE-HUB, X-BIO, or any future planet agent.
═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import logging
import os
import random
import signal
import sys
import time
import uuid
from typing import Optional, AsyncGenerator

import grpc
from google.protobuf import timestamp_pb2, struct_pb2
from google.protobuf.empty_pb2 import Empty

# Proto imports — ensure compiled stubs are on PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../..", "orchestrator"))
import nexus_pulse_pb2 as pb
import nexus_pulse_pb2_grpc as pb_grpc

# Optional: System metrics (install with: pip install psutil)
try:
    import psutil
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    print("⚠️  psutil not available. Install with: pip install psutil")

# ── Configuration ────────────────────────────────────────────────────────────
AGENT_ID       = os.getenv("AGENT_ID", "GENERIC-AGENT")
AGENT_TYPE     = os.getenv("AGENT_TYPE", "planet")
DISPLAY_NAME   = os.getenv("DISPLAY_NAME", AGENT_ID)
CAPABILITIES   = os.getenv("CAPABILITIES", "scan,report,analyze,execute").split(",")
ENDPOINT       = os.getenv("ENDPOINT", "")
ORCH_HOST      = os.getenv("ORCHESTRATOR_HOST", "localhost:50051")
HEARTBEAT_SEC  = int(os.getenv("HEARTBEAT_INTERVAL", "10"))
MAX_RETRIES    = int(os.getenv("MAX_RETRIES", "10"))
INITIAL_BACKOFF = float(os.getenv("INITIAL_BACKOFF", "1.0"))
MAX_BACKOFF    = float(os.getenv("MAX_BACKOFF", "60.0"))

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s │ %(levelname)-7s │ {AGENT_ID:20s} │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(AGENT_ID)


# ═════════════════════════════════════════════════════════════════════════════
# SYSTEM METRICS (Production-grade observability)
# ═════════════════════════════════════════════════════════════════════════════

def get_system_metrics() -> pb.AgentMetrics:
    """Collect real system metrics using psutil."""
    if not METRICS_AVAILABLE:
        return pb.AgentMetrics(
            cpu_usage_percent=0.0,
            memory_usage_percent=0.0,
            request_latency_ms=0.0,
            active_tasks=0,
            completed_tasks=0,
            failed_tasks=0,
            uptime_seconds=0.0,
        )
    
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        
        return pb.AgentMetrics(
            cpu_usage_percent=cpu_percent,
            memory_usage_percent=memory_info.percent,
            request_latency_ms=0.0,  # Can be calculated from task execution
            active_tasks=0,
            completed_tasks=0,
            failed_tasks=0,
            uptime_seconds=0.0,
        )
    except Exception as e:
        log.warning(f"Failed to collect system metrics: {e}")
        return pb.AgentMetrics()


# ═════════════════════════════════════════════════════════════════════════════
# EXPONENTIAL BACKOFF RECONNECTION (Production-grade resilience)
# ═════════════════════════════════════════════════════════════════════════════

async def exponential_backoff_reconnect(
    func,
    max_retries: int = MAX_RETRIES,
    initial_delay: float = INITIAL_BACKOFF,
    max_delay: float = MAX_BACKOFF,
    jitter: bool = True
):
    """
    Retry a coroutine with exponential backoff.
    
    Args:
        func: Async function to retry (must be a coroutine)
        max_retries: Maximum number of retry attempts
        initial_delay: Starting delay in seconds
        max_delay: Maximum delay cap in seconds
        jitter: Add random jitter to prevent thundering herd
    
    Returns:
        Result of successful function call
    
    Raises:
        Exception: After max_retries exhausted
    """
    retry_delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return await func()
        except grpc.aio.AioRpcError as e:
            if attempt == max_retries - 1:
                log.error(
                    f"❌ Max retries ({max_retries}) exhausted. "
                    f"Last error: {e.code()} - {e.details()}"
                )
                raise
            
            # Calculate backoff with jitter
            if jitter:
                jitter_value = random.uniform(0, 1)
                actual_delay = min(retry_delay * 2 + jitter_value, max_delay)
            else:
                actual_delay = min(retry_delay * 2, max_delay)
            
            log.warning(
                f"⚠️  Attempt {attempt + 1}/{max_retries} failed: "
                f"{e.code()} - {e.details()}. "
                f"Retrying in {actual_delay:.2f}s..."
            )
            
            await asyncio.sleep(actual_delay)
            retry_delay = actual_delay
        except Exception as e:
            if attempt == max_retries - 1:
                log.error(f"❌ Max retries exhausted. Last error: {e}")
                raise
            
            # Calculate backoff
            if jitter:
                actual_delay = min(retry_delay * 2 + random.uniform(0, 1), max_delay)
            else:
                actual_delay = min(retry_delay * 2, max_delay)
            
            log.warning(
                f"⚠️  Attempt {attempt + 1}/{max_retries} failed: {e}. "
                f"Retrying in {actual_delay:.2f}s..."
            )
            
            await asyncio.sleep(actual_delay)
            retry_delay = actual_delay


# ═════════════════════════════════════════════════════════════════════════════
# AGENT CLIENT CLASS
# ═════════════════════════════════════════════════════════════════════════════

class NexusAgentClient:
    """
    Production-grade gRPC Pulse client for NEXUS PRIME agents.
    Features: exponential backoff, real metrics, graceful shutdown.
    """

    def __init__(self):
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[pb_grpc.NexusPulseServiceStub] = None
        self._running = True
        self._sequence = 0
        self._tasks_completed = 0
        self._tasks_failed = 0
        self._active_tasks = 0
        self._start_time = time.monotonic()
        self._pulse_queue: Optional[asyncio.Queue] = None
        self._stream_task: Optional[asyncio.Task] = None

    async def connect(self):
        """Establish gRPC channel to Meta-Orchestrator with retry."""
        async def _connect():
            self.channel = grpc.aio.insecure_channel(
                ORCH_HOST,
                options=[
                    ("grpc.keepalive_time_ms", 30000),
                    ("grpc.keepalive_timeout_ms", 10000),
                    ("grpc.keepalive_permit_without_calls", True),
                    ("grpc.max_send_message_length", 50 * 1024 * 1024),
                    ("grpc.max_receive_message_length", 50 * 1024 * 1024),
                    ("grpc.enable_retries", 1),
                    ("grpc.initial_reconnect_backoff_ms", 1000),
                    ("grpc.max_reconnect_backoff_ms", 60000),
                ],
            )
            self.stub = pb_grpc.NexusPulseServiceStub(self.channel)
            
            # Test connection with health check
            await self.channel.channel_ready()
            log.info(f"✅ Connected to Meta-Orchestrator at {ORCH_HOST}")
        
        await exponential_backoff_reconnect(_connect)

    async def disconnect(self):
        """Clean shutdown with stream cleanup."""
        log.info("🛑 Initiating graceful shutdown...")
        self._running = False
        
        # Cancel pulse stream if running
        if self._stream_task and not self._stream_task.done():
            self._stream_task.cancel()
            try:
                await self._stream_task
            except asyncio.CancelledError:
                pass
        
        # Close channel
        if self.channel:
            await self.channel.close()
            log.info("✅ Disconnected from Meta-Orchestrator")

    def _next_seq(self) -> int:
        self._sequence += 1
        return self._sequence

    @staticmethod
    def _now_ts() -> timestamp_pb2.Timestamp:
        ts = timestamp_pb2.Timestamp()
        ts.GetCurrentTime()
        return ts

    @staticmethod
    def _agent_type_enum(t: str) -> int:
        return {
            "planet": pb.AGENT_TYPE_PLANET,
            "service": pb.AGENT_TYPE_SERVICE,
            "human": pb.AGENT_TYPE_HUMAN,
            "swarm": pb.AGENT_TYPE_SWARM,
        }.get(t, pb.AGENT_TYPE_PLANET)

    # ── Production-Grade Pulse Stream ────────────────────────────────────────

    async def run_pulse_stream(self):
        """
        Core bidirectional Pulse stream with queue-based message injection.
        Allows sending pulses from anywhere (task results, intents, etc.).
        """
        self._pulse_queue = asyncio.Queue()
        
        async def _pulse_generator() -> AsyncGenerator[pb.AgentPulse, None]:
            """Yields AgentPulse messages to the orchestrator."""
            # 1. Send registration pulse first
            correlation_id = str(uuid.uuid4())
            reg_pulse = pb.AgentPulse(
                agent_id=AGENT_ID,
                pulse_type=pb.PULSE_TYPE_REGISTRATION,
                timestamp=self._now_ts(),
                capabilities=CAPABILITIES,
                endpoint=ENDPOINT,
                agent_type=self._agent_type_enum(AGENT_TYPE),
                display_name=DISPLAY_NAME,
                sequence_number=self._next_seq(),
                correlation_id=correlation_id,
            )
            log.info(f"📡 Sending registration pulse (correlation_id: {correlation_id})")
            yield reg_pulse

            # 2. Process queue (heartbeats, task results, intents)
            while self._running:
                try:
                    pulse = await asyncio.wait_for(
                        self._pulse_queue.get(), 
                        timeout=HEARTBEAT_SEC / 2
                    )
                    pulse.sequence_number = self._next_seq()
                    pulse.timestamp.CopyFrom(self._now_ts())
                    yield pulse
                    log.debug(f"📤 Sent pulse #{self._sequence}: {pb.PulseType.Name(pulse.pulse_type)}")
                except asyncio.TimeoutError:
                    # Send heartbeat if no messages in queue
                    if self._running:
                        heartbeat = self._create_heartbeat()
                        yield heartbeat

        # Open bidirectional stream with retry
        async def _run_stream():
            stream = self.stub.Pulse(_pulse_generator())
            
            # Receive directives from orchestrator
            try:
                async for directive in stream:
                    await self._handle_directive(directive)
            except grpc.aio.AioRpcError as e:
                if e.code() == grpc.StatusCode.CANCELLED:
                    log.info("Pulse stream cancelled (shutdown)")
                else:
                    log.error(f"❌ Pulse stream error: {e.code()} — {e.details()}")
                    raise
            except asyncio.CancelledError:
                log.info("Pulse stream cancelled")
                raise

        # Run with exponential backoff on connection failure
        await exponential_backoff_reconnect(_run_stream)

    def _create_heartbeat(self) -> pb.AgentPulse:
        """Create heartbeat pulse with real system metrics."""
        uptime = time.monotonic() - self._start_time
        
        # Get real system metrics
        base_metrics = get_system_metrics()
        
        # Merge with agent-specific tracking
        metrics = pb.AgentMetrics(
            cpu_usage_percent=base_metrics.cpu_usage_percent,
            memory_usage_percent=base_metrics.memory_usage_percent,
            request_latency_ms=0.0,
            active_tasks=self._active_tasks,
            completed_tasks=self._tasks_completed,
            failed_tasks=self._tasks_failed,
            uptime_seconds=uptime,
        )
        
        return pb.AgentPulse(
            agent_id=AGENT_ID,
            pulse_type=pb.PULSE_TYPE_HEARTBEAT,
            timestamp=self._now_ts(),
            state=pb.AgentState(
                status=pb.AGENT_STATUS_IDLE if self._active_tasks == 0 else pb.AGENT_STATUS_BUSY,
                current_task="" if self._active_tasks == 0 else f"{self._active_tasks} tasks",
                metrics=metrics,
            ),
            sequence_number=0,  # Will be set by generator
            correlation_id="",  # Will be set if needed
        )

    async def send_pulse(self, pulse: pb.AgentPulse):
        """
        Send a pulse through the stream (task results, intents, etc.).
        Safe to call from any coroutine.
        """
        if self._pulse_queue:
            await self._pulse_queue.put(pulse)
        else:
            log.warning("⚠️  Pulse queue not initialized. Cannot send pulse.")

    async def _handle_directive(self, directive: pb.OrchestratorDirective):
        """Process incoming directives from the Meta-Orchestrator."""
        dt = directive.directive_type
        correlation_id = directive.correlation_id or "N/A"

        if dt == pb.DIRECTIVE_TYPE_ACK:
            log.info(f"✅ ACK (correlation: {correlation_id}): {directive.message}")

        elif dt == pb.DIRECTIVE_TYPE_EXECUTE_TASK:
            cmd = directive.command
            log.info(
                f"📋 Task received (correlation: {correlation_id}): "
                f"{cmd.command_type} (id: {cmd.command_id}, priority: {cmd.priority})"
            )
            # Execute task in background
            asyncio.create_task(self._execute_task(cmd))

        elif dt == pb.DIRECTIVE_TYPE_RECONFIGURE:
            log.info(f"⚙️  Reconfiguration (correlation: {correlation_id}): {directive.message}")
            # Implement reconfiguration logic here

        elif dt == pb.DIRECTIVE_TYPE_SHUTDOWN:
            log.warning(f"🛑 Shutdown directive received (correlation: {correlation_id})")
            self._running = False

        elif dt == pb.DIRECTIVE_TYPE_BROADCAST:
            log.info(f"📢 Broadcast (correlation: {correlation_id}): {directive.message}")

        else:
            log.warning(f"⚠️  Unknown directive type: {dt}")

    async def _execute_task(self, cmd: pb.TaskCommand):
        """
        Template task executor with proper metrics tracking.
        Override this for real agent logic.
        """
        task_id = cmd.command_id
        task_type = cmd.command_type
        correlation_id = str(uuid.uuid4())
        
        self._active_tasks += 1
        log.info(f"⏳ Executing task: {task_type} (id: {task_id}, correlation: {correlation_id})")

        try:
            # Simulate work
            start = time.monotonic()
            await asyncio.sleep(random.uniform(0.5, 2.0))
            elapsed_ms = int((time.monotonic() - start) * 1000)

            self._tasks_completed += 1
            log.info(f"✅ Task completed in {elapsed_ms}ms: {task_type}")

            # Send task result pulse
            result_data = struct_pb2.Struct()
            result_data.update({
                "status": "success",
                "execution_time_ms": elapsed_ms,
                "result": f"Task {task_type} completed successfully",
            })

            result_pulse = pb.AgentPulse(
                agent_id=AGENT_ID,
                pulse_type=pb.PULSE_TYPE_TASK_RESULT,
                timestamp=self._now_ts(),
                task_result=pb.TaskResult(
                    command_id=task_id,
                    status=pb.TASK_STATUS_SUCCESS,
                    result_data=result_data,
                    execution_time_ms=elapsed_ms,
                    error_message="",
                ),
                correlation_id=correlation_id,
            )
            await self.send_pulse(result_pulse)

        except Exception as e:
            self._tasks_failed += 1
            log.error(f"❌ Task failed: {task_type} - {e}")

            # Send failure result
            result_pulse = pb.AgentPulse(
                agent_id=AGENT_ID,
                pulse_type=pb.PULSE_TYPE_TASK_RESULT,
                timestamp=self._now_ts(),
                task_result=pb.TaskResult(
                    command_id=task_id,
                    status=pb.TASK_STATUS_FAILED,
                    result_data=struct_pb2.Struct(),
                    execution_time_ms=0,
                    error_message=str(e),
                ),
                correlation_id=correlation_id,
            )
            await self.send_pulse(result_pulse)

        finally:
            self._active_tasks -= 1

    # ── Unary RPCs (Alternative to Pulse stream) ─────────────────────────────

    async def register_unary(self):
        """One-shot registration via unary RPC with retry."""
        async def _register():
            req = pb.AgentRegistration(
                name=AGENT_ID,
                display_name=DISPLAY_NAME,
                agent_type=self._agent_type_enum(AGENT_TYPE),
                capabilities=CAPABILITIES,
                endpoint=ENDPOINT,
            )
            ack = await self.stub.RegisterAgent(req)
            log.info(
                f"Registration {'✅ OK' if ack.success else '❌ FAILED'}: "
                f"{ack.message}"
            )
            if ack.system_state:
                log.info(
                    f"System: {ack.system_state.online_agents} online / "
                    f"{ack.system_state.total_agents} total agents"
                )
            return ack
        
        return await exponential_backoff_reconnect(_register)

    async def get_status(self):
        """Query system status via unary RPC with retry."""
        async def _get_status():
            snapshot = await self.stub.GetSystemStatus(Empty())
            log.info(
                f"System Status: "
                f"{snapshot.online_agents} online / "
                f"{snapshot.total_agents} total | "
                f"Queued: {snapshot.queued_commands} | "
                f"Running: {snapshot.running_commands}"
            )
            for a in snapshot.agents[:5]:
                log.info(f"  → {a.name}: {pb.AgentStatus.Name(a.status)}")
            return snapshot
        
        return await exponential_backoff_reconnect(_get_status)

    async def submit_command(self, command_type: str, payload: dict = None,
                              priority: int = 5):
        """Submit a command via unary RPC with retry."""
        async def _submit():
            payload_struct = struct_pb2.Struct()
            if payload:
                payload_struct.update(payload)

            cmd = pb.TaskCommand(
                command_id=str(uuid.uuid4()),
                command_type=command_type,
                origin=AGENT_ID,
                payload=payload_struct,
                priority=priority,
            )
            ack = await self.stub.SubmitCommand(cmd)
            log.info(
                f"Command {'✅' if ack.success else '❌'}: "
                f"{ack.command_id} → {ack.target_agent} ({ack.message})"
            )
            return ack
        
        return await exponential_backoff_reconnect(_submit)


# ═════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═════════════════════════════════════════════════════════════════════════════

async def main():
    client = NexusAgentClient()
    
    # Handle shutdown signals
    def _shutdown():
        log.info("🛑 Shutdown signal received...")
        client._running = False

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _shutdown)

    try:
        # Connect with exponential backoff
        await client.connect()
        
        # Run full bidirectional Pulse stream (recommended)
        log.info(f"🚀 Starting Pulse stream for {AGENT_ID}...")
        client._stream_task = asyncio.create_task(client.run_pulse_stream())
        await client._stream_task
        
    except KeyboardInterrupt:
        log.info("⌨️  Keyboard interrupt")
    except Exception as e:
        log.error(f"❌ Fatal error: {e}", exc_info=True)
    finally:
        await client.disconnect()


if __name__ == "__main__":
    # Use uvloop for maximum performance (optional)
    try:
        import uvloop
        uvloop.install()
        log.info("🚀 uvloop installed for optimal async performance")
    except ImportError:
        pass

    asyncio.run(main())
