"""
═══════════════════════════════════════════════════════════════════════════════
NEXUS PRIME — Generic Agent Client (gRPC Pulse Template)
═══════════════════════════════════════════════════════════════════════════════
Template for any agent to connect to the Meta-Orchestrator via gRPC.
Demonstrates: registration, heartbeat loop, task result, intent submission.

Usage:
    AGENT_ID=MY-AGENT ORCHESTRATOR_HOST=localhost:50051 python agent_client.py

Adapt this for SHADOW-7, CLONE-HUB, X-BIO, or any future planet agent.
═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import logging
import os
import signal
import sys
import time
import uuid
from typing import Optional

import grpc
from google.protobuf import timestamp_pb2, struct_pb2

# Proto imports — ensure compiled stubs are on PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "orchestrator"))
import nexus_pulse_pb2 as pb
import nexus_pulse_pb2_grpc as pb_grpc

# ── Configuration ────────────────────────────────────────────────────────────
AGENT_ID       = os.getenv("AGENT_ID", "GENERIC-AGENT")
AGENT_TYPE     = os.getenv("AGENT_TYPE", "planet")
DISPLAY_NAME   = os.getenv("DISPLAY_NAME", AGENT_ID)
CAPABILITIES   = os.getenv("CAPABILITIES", "scan,report").split(",")
ENDPOINT       = os.getenv("ENDPOINT", "")
ORCH_HOST      = os.getenv("ORCHESTRATOR_HOST", "localhost:50051")
HEARTBEAT_SEC  = int(os.getenv("HEARTBEAT_INTERVAL", "10"))

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s │ %(levelname)-7s │ {AGENT_ID:20s} │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(AGENT_ID)


class NexusAgentClient:
    """
    gRPC Pulse client for NEXUS PRIME agents.
    Opens a bidirectional stream with the Meta-Orchestrator.
    """

    def __init__(self):
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[pb_grpc.NexusPulseServiceStub] = None
        self._running = True
        self._sequence = 0
        self._tasks_completed = 0
        self._tasks_failed = 0
        self._start_time = time.monotonic()

    async def connect(self):
        """Establish gRPC channel to Meta-Orchestrator."""
        self.channel = grpc.aio.insecure_channel(
            ORCH_HOST,
            options=[
                ("grpc.keepalive_time_ms", 30000),
                ("grpc.keepalive_timeout_ms", 10000),
                ("grpc.keepalive_permit_without_calls", True),
                ("grpc.max_send_message_length", 50 * 1024 * 1024),
                ("grpc.max_receive_message_length", 50 * 1024 * 1024),
            ],
        )
        self.stub = pb_grpc.NexusPulseServiceStub(self.channel)
        log.info(f"Connected to Meta-Orchestrator at {ORCH_HOST}")

    async def disconnect(self):
        """Clean shutdown."""
        self._running = False
        if self.channel:
            await self.channel.close()
            log.info("Disconnected from Meta-Orchestrator")

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

    # ── Pulse Stream ─────────────────────────────────────────────────────────

    async def run_pulse_stream(self):
        """Core bidirectional Pulse stream."""

        async def _pulse_generator():
            """Yields AgentPulse messages to the orchestrator."""
            # 1. Send registration pulse first
            reg_pulse = pb.AgentPulse(
                agent_id=AGENT_ID,
                pulse_type=pb.PULSE_TYPE_REGISTRATION,
                timestamp=self._now_ts(),
                capabilities=CAPABILITIES,
                endpoint=ENDPOINT,
                agent_type=self._agent_type_enum(AGENT_TYPE),
                display_name=DISPLAY_NAME,
                sequence_number=self._next_seq(),
                correlation_id=str(uuid.uuid4()),
            )
            log.info("📡 Sending registration pulse...")
            yield reg_pulse

            # 2. Heartbeat loop
            while self._running:
                await asyncio.sleep(HEARTBEAT_SEC)
                if not self._running:
                    break

                uptime = time.monotonic() - self._start_time
                heartbeat = pb.AgentPulse(
                    agent_id=AGENT_ID,
                    pulse_type=pb.PULSE_TYPE_HEARTBEAT,
                    timestamp=self._now_ts(),
                    state=pb.AgentState(
                        status=pb.AGENT_STATUS_IDLE,
                        current_task="",
                        metrics=pb.AgentMetrics(
                            cpu_usage_percent=0.0,
                            memory_usage_percent=0.0,
                            request_latency_ms=0.0,
                            active_tasks=0,
                            completed_tasks=self._tasks_completed,
                            failed_tasks=self._tasks_failed,
                            uptime_seconds=uptime,
                        ),
                    ),
                    sequence_number=self._next_seq(),
                )
                yield heartbeat
                log.debug(f"💓 Heartbeat #{self._sequence} sent (uptime: {uptime:.0f}s)")

        # Open bidirectional stream
        stream = self.stub.Pulse(_pulse_generator())

        # Receive directives from orchestrator
        try:
            async for directive in stream:
                await self._handle_directive(directive)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.CANCELLED:
                log.info("Pulse stream cancelled (shutdown)")
            else:
                log.error(f"Pulse stream error: {e.code()} — {e.details()}")
        except asyncio.CancelledError:
            log.info("Pulse stream cancelled")

    async def _handle_directive(self, directive: pb.OrchestratorDirective):
        """Process incoming directives from the Meta-Orchestrator."""
        dt = directive.directive_type

        if dt == pb.DIRECTIVE_TYPE_ACK:
            log.info(f"✅ ACK: {directive.message}")

        elif dt == pb.DIRECTIVE_TYPE_EXECUTE_TASK:
            cmd = directive.command
            log.info(
                f"📋 Task received: {cmd.command_type} "
                f"(id: {cmd.command_id}, priority: {cmd.priority})"
            )
            # ─── IMPLEMENT YOUR TASK LOGIC HERE ───
            # Example: simulate task execution
            await self._execute_task(cmd)

        elif dt == pb.DIRECTIVE_TYPE_RECONFIGURE:
            log.info(f"⚙️ Reconfiguration directive: {directive.message}")

        elif dt == pb.DIRECTIVE_TYPE_SHUTDOWN:
            log.warning("🛑 Shutdown directive received — stopping agent")
            self._running = False

        elif dt == pb.DIRECTIVE_TYPE_BROADCAST:
            log.info(f"📢 Broadcast: {directive.message}")

        else:
            log.warning(f"Unknown directive type: {dt}")

    async def _execute_task(self, cmd: pb.TaskCommand):
        """
        Template task executor. Override this for real agent logic.
        Reports result back via a TASK_RESULT pulse (through the stream).
        """
        log.info(f"⏳ Executing task: {cmd.command_type}...")

        # Simulate work
        start = time.monotonic()
        await asyncio.sleep(1)
        elapsed_ms = int((time.monotonic() - start) * 1000)

        self._tasks_completed += 1
        log.info(f"✅ Task completed in {elapsed_ms}ms: {cmd.command_type}")

        # Note: In a real implementation, you'd send a TASK_RESULT pulse
        # back through the stream generator. For simplicity, this template
        # logs the result. See the stream generator for how to inject pulses.

    # ── Unary RPCs (Alternative to Pulse stream) ─────────────────────────────

    async def register_unary(self):
        """One-shot registration via unary RPC."""
        req = pb.AgentRegistration(
            name=AGENT_ID,
            display_name=DISPLAY_NAME,
            agent_type=self._agent_type_enum(AGENT_TYPE),
            capabilities=CAPABILITIES,
            endpoint=ENDPOINT,
        )
        try:
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
        except grpc.aio.AioRpcError as e:
            log.error(f"Registration failed: {e.code()} — {e.details()}")
            return None

    async def get_status(self):
        """Query system status via unary RPC."""
        from google.protobuf.empty_pb2 import Empty
        try:
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
        except grpc.aio.AioRpcError as e:
            log.error(f"Status query failed: {e.code()} — {e.details()}")
            return None

    async def submit_command(self, command_type: str, payload: dict = None,
                              priority: int = 5):
        """Submit a command via unary RPC."""
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
        try:
            ack = await self.stub.SubmitCommand(cmd)
            log.info(
                f"Command {'✅' if ack.success else '❌'}: "
                f"{ack.command_id} → {ack.target_agent} ({ack.message})"
            )
            return ack
        except grpc.aio.AioRpcError as e:
            log.error(f"Command submission failed: {e.code()} — {e.details()}")
            return None


# ═════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═════════════════════════════════════════════════════════════════════════════

async def main():
    client = NexusAgentClient()
    await client.connect()

    # Handle shutdown signals
    def _shutdown():
        log.info("Shutdown signal — stopping agent...")
        client._running = False

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _shutdown)

    try:
        # Option 1: Run full bidirectional Pulse stream (recommended)
        log.info(f"🚀 Starting Pulse stream for {AGENT_ID}...")
        await client.run_pulse_stream()
    except KeyboardInterrupt:
        pass
    finally:
        await client.disconnect()


if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass

    asyncio.run(main())
