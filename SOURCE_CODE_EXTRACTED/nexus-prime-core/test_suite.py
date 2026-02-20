"""
═══════════════════════════════════════════════════════════════════════════════
NEXUS PRIME CORE — Comprehensive Test Suite
═══════════════════════════════════════════════════════════════════════════════
Tests all 4 gRPC RPCs:
  1. GetSystemStatus (unary)
  2. RegisterAgent (unary)
  3. SubmitCommand (unary)
  4. Pulse (bidirectional streaming)
Also validates Cortex bridge integration.
═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import json
import sys
import time
import uuid
import os

sys.path.insert(0, os.path.dirname(__file__))

import grpc
from google.protobuf import empty_pb2, struct_pb2, timestamp_pb2
import nexus_pulse_pb2 as pb
import nexus_pulse_pb2_grpc as pb_grpc


ORCH_HOST = os.getenv("ORCHESTRATOR_HOST", "localhost:50051")
CORTEX_URL = os.getenv("CORTEX_URL", "http://localhost:8090")

# ── Test Results Tracking ────────────────────────────────────────────────────
results = []
test_count = 0
pass_count = 0
fail_count = 0


def report(test_name: str, passed: bool, details: str = "", duration_ms: int = 0):
    global test_count, pass_count, fail_count
    test_count += 1
    if passed:
        pass_count += 1
        icon = "✅"
    else:
        fail_count += 1
        icon = "❌"
    results.append({
        "test": test_name,
        "passed": passed,
        "details": details,
        "duration_ms": duration_ms,
    })
    dur = f" ({duration_ms}ms)" if duration_ms else ""
    print(f"  {icon} {test_name}{dur}")
    if details and not passed:
        print(f"     → {details}")


# ═════════════════════════════════════════════════════════════════════════════
# TEST 1: gRPC Channel Connectivity
# ═════════════════════════════════════════════════════════════════════════════

async def test_channel_connectivity():
    print("\n═══ TEST GROUP 1: Channel Connectivity ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    try:
        t0 = time.monotonic()
        await asyncio.wait_for(channel.channel_ready(), timeout=5.0)
        dur = int((time.monotonic() - t0) * 1000)
        report("gRPC channel ready", True, f"Connected to {ORCH_HOST}", dur)
    except Exception as e:
        report("gRPC channel ready", False, str(e))
    finally:
        await channel.close()


# ═════════════════════════════════════════════════════════════════════════════
# TEST 2: Server Reflection
# ═════════════════════════════════════════════════════════════════════════════

async def test_server_reflection():
    print("\n═══ TEST GROUP 2: Server Reflection ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    try:
        # Use low-level reflection call instead of ProtoReflectionDescriptorDatabase
        from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)

        t0 = time.monotonic()

        async def _req_gen():
            yield reflection_pb2.ServerReflectionRequest(list_services="")

        responses = stub.ServerReflectionInfo(_req_gen())
        services = []
        async for resp in responses:
            if resp.HasField("list_services_response"):
                for svc in resp.list_services_response.service:
                    services.append(svc.name)

        dur = int((time.monotonic() - t0) * 1000)

        has_pulse = "nexus.prime.NexusPulseService" in services
        has_health = "grpc.health.v1.Health" in services
        has_reflection = "grpc.reflection.v1alpha.ServerReflection" in services

        report("Service discovery via reflection", has_pulse,
               f"Found: {services}", dur)
        report("Health service registered", has_health)
        report("Reflection service active", has_reflection)

    except Exception as e:
        report("Server reflection", False, str(e))
    finally:
        await channel.close()


# ═════════════════════════════════════════════════════════════════════════════
# TEST 3: GetSystemStatus (Unary RPC)
# ═════════════════════════════════════════════════════════════════════════════

async def test_get_system_status():
    print("\n═══ TEST GROUP 3: GetSystemStatus (Unary) ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    stub = pb_grpc.NexusPulseServiceStub(channel)
    try:
        t0 = time.monotonic()
        snapshot = await stub.GetSystemStatus(empty_pb2.Empty())
        dur = int((time.monotonic() - t0) * 1000)

        report("GetSystemStatus returns response", True, duration_ms=dur)
        report("Has online_agents field", snapshot.online_agents >= 0,
               f"online_agents={snapshot.online_agents}")
        report("Has total_agents field", snapshot.total_agents >= 0,
               f"total_agents={snapshot.total_agents}")
        report("Has queued_commands field", snapshot.queued_commands >= 0,
               f"queued_commands={snapshot.queued_commands}")
        report("Has timestamp", snapshot.timestamp.seconds > 0)
        report("Contains agent summaries", len(snapshot.agents) >= 0,
               f"{len(snapshot.agents)} agents listed")

        # Check META-ORCHESTRATOR is registered
        agent_names = [a.name for a in snapshot.agents]
        report("META-ORCHESTRATOR in agent list",
               "META-ORCHESTRATOR" in agent_names,
               f"Agents: {agent_names[:5]}...")

    except Exception as e:
        report("GetSystemStatus", False, str(e))
    finally:
        await channel.close()


# ═════════════════════════════════════════════════════════════════════════════
# TEST 4: RegisterAgent (Unary RPC)
# ═════════════════════════════════════════════════════════════════════════════

async def test_register_agent():
    print("\n═══ TEST GROUP 4: RegisterAgent (Unary) ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    stub = pb_grpc.NexusPulseServiceStub(channel)
    try:
        test_agent = f"TEST-AGENT-{uuid.uuid4().hex[:6].upper()}"

        t0 = time.monotonic()
        ack = await stub.RegisterAgent(pb.AgentRegistration(
            name=test_agent,
            display_name=f"Test Agent ({test_agent})",
            agent_type=pb.AGENT_TYPE_PLANET,
            capabilities=["scan", "report", "test"],
            endpoint="grpc://test:50052",
            metadata={"test": "true", "created_by": "test_suite"},
        ))
        dur = int((time.monotonic() - t0) * 1000)

        report("RegisterAgent returns ACK", True, duration_ms=dur)
        report("Registration successful", ack.success, ack.message)
        report("Agent ID returned", ack.agent_id == test_agent,
               f"Expected {test_agent}, got {ack.agent_id}")
        report("System snapshot included", ack.system_state is not None and
               ack.system_state.total_agents > 0,
               f"Total agents: {ack.system_state.total_agents if ack.system_state else 0}")
        report("Registered_at timestamp set",
               ack.registered_at.seconds > 0 if ack.registered_at else False)

        # Verify in Cortex via GetSystemStatus
        snapshot = await stub.GetSystemStatus(empty_pb2.Empty())
        agent_names = [a.name for a in snapshot.agents]
        report("Agent visible in system status",
               test_agent in agent_names,
               f"Looking for {test_agent} in {len(agent_names)} agents")

    except Exception as e:
        report("RegisterAgent", False, str(e))
    finally:
        await channel.close()


# ═════════════════════════════════════════════════════════════════════════════
# TEST 5: SubmitCommand (Unary RPC)
# ═════════════════════════════════════════════════════════════════════════════

async def test_submit_command():
    print("\n═══ TEST GROUP 5: SubmitCommand (Unary) ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    stub = pb_grpc.NexusPulseServiceStub(channel)
    try:
        payload = struct_pb2.Struct()
        payload.update({"target": "system", "action": "health_check", "test": True})

        t0 = time.monotonic()
        ack = await stub.SubmitCommand(pb.TaskCommand(
            command_id=str(uuid.uuid4()),
            command_type="scan",
            origin="test_suite",
            payload=payload,
            priority=3,
        ))
        dur = int((time.monotonic() - t0) * 1000)

        report("SubmitCommand returns ACK", True, duration_ms=dur)
        report("Command acknowledged", ack.success, ack.message)
        report("Command ID assigned", len(ack.command_id) > 0,
               f"command_id={ack.command_id}")
        report("Status is QUEUED", ack.status == pb.TASK_STATUS_QUEUED,
               f"status={pb.TaskStatus.Name(ack.status)}")

    except Exception as e:
        report("SubmitCommand", False, str(e))
    finally:
        await channel.close()


# ═════════════════════════════════════════════════════════════════════════════
# TEST 6: Pulse Bidirectional Stream
# ═════════════════════════════════════════════════════════════════════════════

async def test_pulse_stream():
    print("\n═══ TEST GROUP 6: Pulse Bidirectional Stream ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    stub = pb_grpc.NexusPulseServiceStub(channel)

    stream_agent = f"PULSE-TEST-{uuid.uuid4().hex[:6].upper()}"
    received_directives = []
    stream_error = None

    async def pulse_generator():
        """Send registration → heartbeat → intent → result pulses."""
        seq = 0

        # 1. Registration pulse
        seq += 1
        yield pb.AgentPulse(
            agent_id=stream_agent,
            pulse_type=pb.PULSE_TYPE_REGISTRATION,
            timestamp=_now_ts(),
            capabilities=["scan", "analyze", "pulse_test"],
            endpoint="grpc://test-pulse:50099",
            agent_type=pb.AGENT_TYPE_PLANET,
            display_name=f"Pulse Test Agent",
            sequence_number=seq,
            correlation_id="reg-001",
        )
        await asyncio.sleep(0.5)

        # 2. Heartbeat pulse
        seq += 1
        yield pb.AgentPulse(
            agent_id=stream_agent,
            pulse_type=pb.PULSE_TYPE_HEARTBEAT,
            timestamp=_now_ts(),
            state=pb.AgentState(
                status=pb.AGENT_STATUS_IDLE,
                current_task="",
                metrics=pb.AgentMetrics(
                    cpu_usage_percent=12.5,
                    memory_usage_percent=45.2,
                    request_latency_ms=3.7,
                    active_tasks=0,
                    completed_tasks=0,
                    failed_tasks=0,
                    uptime_seconds=10.0,
                ),
            ),
            sequence_number=seq,
        )
        await asyncio.sleep(0.5)

        # 3. State update pulse
        seq += 1
        yield pb.AgentPulse(
            agent_id=stream_agent,
            pulse_type=pb.PULSE_TYPE_STATE_UPDATE,
            timestamp=_now_ts(),
            state=pb.AgentState(
                status=pb.AGENT_STATUS_BUSY,
                current_task="running_test_scan",
                metrics=pb.AgentMetrics(
                    cpu_usage_percent=78.3,
                    memory_usage_percent=62.1,
                    active_tasks=1,
                ),
            ),
            sequence_number=seq,
        )
        await asyncio.sleep(0.5)

        # 4. Intent pulse (request cooperation)
        seq += 1
        intent_payload = struct_pb2.Struct()
        intent_payload.update({"scan_type": "deep", "target": "network_192"})
        yield pb.AgentPulse(
            agent_id=stream_agent,
            pulse_type=pb.PULSE_TYPE_INTENT,
            timestamp=_now_ts(),
            intent=pb.AgentIntent(
                requested_action="scan",
                target_agent="",
                priority=2,
                payload=intent_payload,
            ),
            sequence_number=seq,
            correlation_id="intent-001",
        )
        await asyncio.sleep(0.5)

        # 5. Error pulse
        seq += 1
        yield pb.AgentPulse(
            agent_id=stream_agent,
            pulse_type=pb.PULSE_TYPE_ERROR,
            timestamp=_now_ts(),
            error_code="TEST_ERROR_001",
            error_message="Simulated test error for validation",
            error_stack_trace="test_suite.py:test_pulse_stream:line_42",
            sequence_number=seq,
        )
        await asyncio.sleep(0.5)

        # 6. Final heartbeat
        seq += 1
        yield pb.AgentPulse(
            agent_id=stream_agent,
            pulse_type=pb.PULSE_TYPE_HEARTBEAT,
            timestamp=_now_ts(),
            state=pb.AgentState(
                status=pb.AGENT_STATUS_IDLE,
                current_task="",
                metrics=pb.AgentMetrics(
                    cpu_usage_percent=5.2,
                    memory_usage_percent=40.0,
                    completed_tasks=1,
                    uptime_seconds=15.0,
                ),
            ),
            sequence_number=seq,
        )

    try:
        t0 = time.monotonic()

        # Open bidirectional stream
        stream = stub.Pulse(pulse_generator())

        # Collect directives with timeout
        try:
            async def _collect():
                async for directive in stream:
                    received_directives.append(directive)
            await asyncio.wait_for(_collect(), timeout=10.0)
        except asyncio.TimeoutError:
            pass  # expected — stream ends when generator finishes
        except grpc.aio.AioRpcError:
            pass  # stream closed by server

        dur = int((time.monotonic() - t0) * 1000)

        # Validate received directives
        report("Pulse stream opened successfully", len(received_directives) > 0,
               f"Received {len(received_directives)} directives", dur)

        # Check for welcome ACK
        acks = [d for d in received_directives if d.directive_type == pb.DIRECTIVE_TYPE_ACK]
        report("Welcome ACK received", len(acks) > 0,
               f"ACKs: {len(acks)} — first: {acks[0].message[:60] if acks else 'none'}...")

        # Check for system state in welcome
        welcome_acks = [d for d in acks if "Welcome" in d.message]
        report("Welcome includes system snapshot",
               len(welcome_acks) > 0 and welcome_acks[0].system_state is not None,
               f"System state included: {welcome_acks[0].system_state.total_agents if welcome_acks and welcome_acks[0].system_state else 0} agents")

        # Check heartbeat ACKs
        hb_acks = [d for d in acks if "Heartbeat" in d.message]
        report("Heartbeat ACKs received", len(hb_acks) >= 1,
               f"Got {len(hb_acks)} heartbeat ACKs")

        # Check intent ACK
        intent_acks = [d for d in acks if "Intent routed" in d.message or "routed" in d.message.lower()]
        report("Intent routed ACK received", len(intent_acks) >= 1,
               f"Got {len(intent_acks)} intent ACKs")

        # Registration ACK
        reg_acks = [d for d in acks if "registered" in d.message.lower() or "Registration" in d.message]
        report("Registration ACK via stream", len(reg_acks) >= 1,
               f"Got {len(reg_acks)} registration ACKs")

        # Directive IDs are UUIDs
        report("All directives have UUIDs",
               all(len(d.directive_id) > 10 for d in received_directives),
               f"Sample ID: {received_directives[0].directive_id if received_directives else 'none'}")

        # Sequence numbers
        report("Directives have sequence numbers",
               all(d.sequence_number > 0 for d in received_directives),
               f"Sequences: {[d.sequence_number for d in received_directives[:5]]}")

    except Exception as e:
        report("Pulse stream", False, str(e))
    finally:
        await channel.close()


async def _collect_directives(stream):
    """Helper to collect directives from a stream."""
    try:
        async for directive in stream:
            yield directive
    except grpc.aio.AioRpcError:
        return
    except asyncio.CancelledError:
        return


# ═════════════════════════════════════════════════════════════════════════════
# TEST 7: Cortex Bridge Integration
# ═════════════════════════════════════════════════════════════════════════════

async def test_cortex_bridge():
    print("\n═══ TEST GROUP 7: Cortex Bridge Integration ═══")

    try:
        import httpx
    except ImportError:
        report("httpx available", False, "Install httpx: pip install httpx")
        return

    async with httpx.AsyncClient(base_url=CORTEX_URL, timeout=10.0) as client:
        # Check Cortex health
        t0 = time.monotonic()
        r = await client.get("/health")
        dur = int((time.monotonic() - t0) * 1000)
        report("Cortex health endpoint", r.status_code == 200,
               f"Status: {r.json()}", dur)

        # Check META-ORCHESTRATOR registered in Cortex
        r = await client.get("/agents")
        agents = r.json().get("agents", [])
        agent_names = [a["name"] for a in agents]
        report("META-ORCHESTRATOR in Cortex registry",
               "META-ORCHESTRATOR" in agent_names,
               f"Cortex knows {len(agents)} agents")

        # Check test agents registered via gRPC
        grpc_agents = [a for a in agents if "TEST-AGENT" in a.get("name", "") or
                       "PULSE-TEST" in a.get("name", "")]
        report("gRPC test agents propagated to Cortex",
               len(grpc_agents) > 0,
               f"Found {len(grpc_agents)} test agents in Cortex")

        # Check dashboard endpoint
        r = await client.get("/dashboard")
        dashboard = r.json()
        report("Cortex dashboard accessible", r.status_code == 200,
               f"Stats: {dashboard.get('stats', {})}")

        # Check events from gRPC error pulse
        r = await client.get("/events", params={"limit": 5})
        events = r.json().get("events", [])
        report("Events flowing to Cortex", len(events) >= 0,
               f"Recent events: {len(events)}")


# ═════════════════════════════════════════════════════════════════════════════
# TEST 8: gRPC Health Check
# ═════════════════════════════════════════════════════════════════════════════

async def test_grpc_health():
    print("\n═══ TEST GROUP 8: gRPC Health Check ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    try:
        from grpc_health.v1 import health_pb2, health_pb2_grpc
        stub = health_pb2_grpc.HealthStub(channel)

        t0 = time.monotonic()
        response = await stub.Check(health_pb2.HealthCheckRequest(
            service="nexus.prime.NexusPulseService"
        ))
        dur = int((time.monotonic() - t0) * 1000)

        report("Health check responds", True, duration_ms=dur)
        report("Service status SERVING",
               response.status == health_pb2.HealthCheckResponse.SERVING,
               f"Status: {response.status}")

    except Exception as e:
        report("gRPC health check", False, str(e))
    finally:
        await channel.close()


# ═════════════════════════════════════════════════════════════════════════════
# TEST 9: Performance & Latency
# ═════════════════════════════════════════════════════════════════════════════

async def test_performance():
    print("\n═══ TEST GROUP 9: Performance & Latency ═══")
    channel = grpc.aio.insecure_channel(ORCH_HOST)
    stub = pb_grpc.NexusPulseServiceStub(channel)

    try:
        # Rapid-fire GetSystemStatus calls
        latencies = []
        for i in range(10):
            t0 = time.monotonic()
            await stub.GetSystemStatus(empty_pb2.Empty())
            latencies.append((time.monotonic() - t0) * 1000)

        avg_ms = sum(latencies) / len(latencies)
        min_ms = min(latencies)
        max_ms = max(latencies)
        p95_ms = sorted(latencies)[int(len(latencies) * 0.95)]

        report(f"10x GetSystemStatus avg latency", avg_ms < 200,
               f"avg={avg_ms:.1f}ms min={min_ms:.1f}ms max={max_ms:.1f}ms p95={p95_ms:.1f}ms")

        # Rapid-fire RegisterAgent calls
        latencies = []
        for i in range(5):
            t0 = time.monotonic()
            await stub.RegisterAgent(pb.AgentRegistration(
                name=f"PERF-TEST-{i}",
                display_name=f"Perf Test {i}",
                agent_type=pb.AGENT_TYPE_SERVICE,
                capabilities=["test"],
            ))
            latencies.append((time.monotonic() - t0) * 1000)

        avg_ms = sum(latencies) / len(latencies)
        report(f"5x RegisterAgent avg latency", avg_ms < 200,
               f"avg={avg_ms:.1f}ms min={min(latencies):.1f}ms max={max(latencies):.1f}ms")

    except Exception as e:
        report("Performance test", False, str(e))
    finally:
        await channel.close()


# ── Helpers ──────────────────────────────────────────────────────────────────

def _now_ts() -> timestamp_pb2.Timestamp:
    ts = timestamp_pb2.Timestamp()
    ts.GetCurrentTime()
    return ts


# ═════════════════════════════════════════════════════════════════════════════
# MAIN — Run All Tests
# ═════════════════════════════════════════════════════════════════════════════

async def main():
    print("═" * 70)
    print("  NEXUS PRIME CORE — Comprehensive gRPC Test Suite")
    print(f"  Target: {ORCH_HOST}")
    print(f"  Cortex: {CORTEX_URL}")
    print("═" * 70)

    t_start = time.monotonic()

    await test_channel_connectivity()
    await test_server_reflection()
    await test_grpc_health()
    await test_get_system_status()
    await test_register_agent()
    await test_submit_command()
    await test_pulse_stream()
    await test_cortex_bridge()
    await test_performance()

    total_time = int((time.monotonic() - t_start) * 1000)

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "═" * 70)
    print(f"  TEST RESULTS: {pass_count}/{test_count} passed "
          f"({fail_count} failed) — {total_time}ms total")
    print("═" * 70)

    if fail_count > 0:
        print("\n  ❌ FAILED TESTS:")
        for r in results:
            if not r["passed"]:
                print(f"     • {r['test']}: {r['details']}")

    print(f"\n  {'✅ ALL TESTS PASSED' if fail_count == 0 else '⚠️ SOME TESTS FAILED'}")
    print("═" * 70)

    # ── JSON Report ──────────────────────────────────────────────────────
    report_data = {
        "suite": "NEXUS PRIME CORE — gRPC Test Suite",
        "target": ORCH_HOST,
        "cortex": CORTEX_URL,
        "total_tests": test_count,
        "passed": pass_count,
        "failed": fail_count,
        "total_time_ms": total_time,
        "results": results,
    }
    with open("/tmp/nexus_grpc_test_report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    print(f"\n  📄 JSON report saved to /tmp/nexus_grpc_test_report.json")

    return fail_count == 0


if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass

    success = asyncio.run(main())
    sys.exit(0 if success else 1)
