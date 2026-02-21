#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
Reflex Agent Runner — Neural Spine Agent Process
═══════════════════════════════════════════════════════════════════════════════

Runs N Active Inference agents, each connected to the Rust spine via FFI
(ctypes → libspine_core.so). Each agent:

  1. Reads its PERCEPT buffer from shared memory (via FFI)
  2. Runs Active Inference cognitive cycle
  3. Writes ACTION buffer back to shared memory (via FFI)
  4. Publishes agent state to Redis for monitoring

ARCHITECTURE:
  - Single Python process, asyncio event loop
  - Each agent is an async coroutine (not a process)
  - FFI calls are fast (~1μs each), so no thread pool needed
  - Cognitive cycle is CPU-bound (~160μs), runs synchronously per agent
  - All 32 agents complete a full cycle in ~5.1ms

CPU PINNING:
  Designed to run on cores 4-11 (cpuset in Docker)
  The spine server runs on cores 0-2, Redis on core 3

═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import ctypes
import json
import os
import signal
import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np

# Import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.active_inference import ActiveInferenceAgent, create_default_model
from monitoring.phi_monitor import PhiStarMonitor

# ═══════════════════════════════════════════════════════════════════════════════
# FFI Bindings to libspine_core.so
# ═══════════════════════════════════════════════════════════════════════════════

class SpineFFI:
    """
    ctypes bindings to the Rust spine-core shared library.
    Provides lock-free access to shared memory agent buffers.
    """

    # Buffer type constants (must match Rust lib.rs)
    BUF_PERCEPT = 0
    BUF_WORKSPACE = 1
    BUF_BROADCAST = 2
    BUF_ACTION = 3
    BUF_META = 4

    BUFFER_SIZE = 1024

    def __init__(self, lib_path: Optional[str] = None):
        if lib_path is None:
            # Default paths to search
            search_paths = [
                "/usr/local/lib/libspine_core.so",
                "/app/lib/libspine_core.so",
                str(Path(__file__).parent.parent / "target" / "release" / "libspine_core.so"),
            ]
            for p in search_paths:
                if os.path.exists(p):
                    lib_path = p
                    break

        if lib_path is None or not os.path.exists(lib_path):
            print(f"⚠ libspine_core.so not found, running in SIMULATION mode")
            self._lib = None
            self._shm_ptr = None
            self._simulated_buffers = {}
            return

        self._lib = ctypes.CDLL(lib_path)
        self._setup_signatures()
        self._shm_ptr = None

    def _setup_signatures(self):
        """Set up ctypes function signatures — must match Rust FFI exactly"""
        lib = self._lib

        # spine_init(shm_name: *const c_char) -> i32
        lib.spine_init.argtypes = [ctypes.c_char_p]
        lib.spine_init.restype = ctypes.c_int32

        # spine_attach(shm_name: *const c_char) -> i32
        lib.spine_attach.argtypes = [ctypes.c_char_p]
        lib.spine_attach.restype = ctypes.c_int32

        # spine_write_buffer(agent_id: u32, buffer_type: u32, data: *const u8, len: u32) -> i32
        lib.spine_write_buffer.argtypes = [
            ctypes.c_uint32, ctypes.c_uint32,
            ctypes.c_char_p, ctypes.c_uint32
        ]
        lib.spine_write_buffer.restype = ctypes.c_int32

        # spine_read_buffer(agent_id: u32, buffer_type: u32, dest: *mut u8, len: u32) -> i32
        lib.spine_read_buffer.argtypes = [
            ctypes.c_uint32, ctypes.c_uint32,
            ctypes.c_char_p, ctypes.c_uint32
        ]
        lib.spine_read_buffer.restype = ctypes.c_int32

        # spine_activate_agent(agent_id: u32) -> i32
        lib.spine_activate_agent.argtypes = [ctypes.c_uint32]
        lib.spine_activate_agent.restype = ctypes.c_int32

        # spine_push_interrupt(source: u16, target: u16, itype: u8, priority: u8, payload: *const u8, len: u32) -> i32
        lib.spine_push_interrupt.argtypes = [
            ctypes.c_uint16, ctypes.c_uint16,
            ctypes.c_uint8, ctypes.c_uint8,
            ctypes.c_char_p, ctypes.c_uint32
        ]
        lib.spine_push_interrupt.restype = ctypes.c_int32

        # spine_active_count() -> i32
        lib.spine_active_count.argtypes = []
        lib.spine_active_count.restype = ctypes.c_int32

        # spine_ring_len() -> i32
        lib.spine_ring_len.argtypes = []
        lib.spine_ring_len.restype = ctypes.c_int32

    def init(self, shm_name: str = "/nexus_spine", use_hugepages: bool = False):
        """Initialize shared memory (only spine-server should call this)"""
        if self._lib is None:
            return
        name_bytes = shm_name.encode('utf-8')
        result = self._lib.spine_init(name_bytes)
        if result != 0:
            print(f"  spine_init failed: {result}")

    def attach(self, shm_name: str = "/nexus_spine"):
        """Attach to existing shared memory (agents call this)"""
        if self._lib is None:
            return
        name_bytes = shm_name.encode('utf-8')
        result = self._lib.spine_attach(name_bytes)
        if result != 0:
            print(f"  spine_attach failed: {result}")

    def activate_agent(self, agent_id: int):
        """Mark an agent as active in the shared memory region"""
        if self._lib is None:
            return
        self._lib.spine_activate_agent(agent_id)

    def write_buffer(self, agent_id: int, buf_type: int, data: bytes):
        """Write data to an agent's buffer"""
        if self._lib is None:
            key = (agent_id, buf_type)
            self._simulated_buffers[key] = data
            return
        self._lib.spine_write_buffer(agent_id, buf_type, data, len(data))

    def read_buffer(self, agent_id: int, buf_type: int) -> bytes:
        """Read data from an agent's buffer"""
        if self._lib is None:
            key = (agent_id, buf_type)
            return self._simulated_buffers.get(key, b'\x00' * self.BUFFER_SIZE)
        out = ctypes.create_string_buffer(self.BUFFER_SIZE)
        retries = self._lib.spine_read_buffer(agent_id, buf_type, out, self.BUFFER_SIZE)
        return out.raw

    def push_interrupt(self, src: int, tgt: int, itype: int, priority: int,
                       payload: bytes = b'') -> bool:
        """Push an interrupt to the ring buffer"""
        if self._lib is None:
            return True
        result = self._lib.spine_push_interrupt(
            src, tgt, itype, priority,
            payload, len(payload)
        )
        return result == 0

    def active_count(self) -> int:
        """Get number of active agents"""
        if self._lib is None:
            return 0
        return self._lib.spine_active_count()

    def ring_len(self) -> int:
        """Get number of pending interrupts"""
        if self._lib is None:
            return 0
        return self._lib.spine_ring_len()


# ═══════════════════════════════════════════════════════════════════════════════
# Agent Runner
# ═══════════════════════════════════════════════════════════════════════════════

class ReflexAgentRunner:
    """
    Manages N Active Inference agents, running their cognitive cycles
    and connecting them to the spine shared memory and Redis.
    """

    def __init__(self, num_agents: int = 32, cycle_hz: float = 20.0):
        self.num_agents = num_agents
        self.cycle_period = 1.0 / cycle_hz
        self.running = False

        # FFI connection to spine
        self.spine = SpineFFI()

        # Active Inference agents
        self.agents: list[ActiveInferenceAgent] = []

        # Phi* monitor
        self.phi_monitor = PhiStarMonitor(num_agents=num_agents)

        # Metrics
        self.total_cycles = 0
        self.total_cycle_ns = 0
        self.phi_eval_count = 0

        # Redis (optional)
        self._redis = None

    async def _init_redis(self):
        """Connect to Redis for status publishing"""
        try:
            import redis.asyncio as aioredis
            self._redis = aioredis.Redis(
                host=os.environ.get('REDIS_HOST', 'nexus_redis'),
                port=int(os.environ.get('REDIS_PORT', 6379)),
                decode_responses=True
            )
            await self._redis.ping()
            print(f"  ✅ Connected to Redis")
        except Exception as e:
            print(f"  ⚠ Redis unavailable: {e} (running standalone)")
            self._redis = None

    def _init_agents(self):
        """Initialize all Active Inference agents"""
        print(f"\n  Initializing {self.num_agents} agents...")
        for i in range(self.num_agents):
            # Each agent gets a unique model seeded by its ID
            # In production, models would be loaded from HR Registry
            model = create_default_model(
                num_states=64,
                num_obs=32,
                num_actions=8,
            )
            # Vary the model slightly per agent
            rng = np.random.default_rng(i * 1000 + 42)
            model.C = rng.standard_normal(32) * 0.5  # Different preferences

            agent = ActiveInferenceAgent(model, agent_id=i)
            self.agents.append(agent)

            # Activate in spine
            self.spine.activate_agent(i)

        print(f"  ✅ {self.num_agents} agents initialized")

    def _percept_to_observation(self, percept_data: bytes, num_obs: int) -> np.ndarray:
        """
        Convert raw percept bytes from spine buffer to observation vector.
        Uses first `num_obs` bytes as softmax input.
        """
        obs = np.zeros(num_obs)
        n = min(len(percept_data), num_obs)
        for i in range(n):
            obs[i] = percept_data[i] / 255.0

        # Softmax normalization
        obs_exp = np.exp(obs - obs.max())
        obs = obs_exp / obs_exp.sum()
        return obs

    def _action_to_bytes(self, action: int, free_energy: float) -> bytes:
        """Encode action and free energy into bytes for ACTION buffer"""
        # Format: [action:u8][free_energy:f64][timestamp:u64]
        import struct
        return struct.pack('<Bdq', action, free_energy, int(time.time_ns()))

    async def _run_cycle(self):
        """
        Run one cognitive cycle for all agents.
        This is the hot loop — performance critical.
        """
        start_ns = time.perf_counter_ns()
        workspace_values = np.zeros(self.num_agents)

        for i, agent in enumerate(self.agents):
            # 1. Read percept from spine
            percept = self.spine.read_buffer(i, SpineFFI.BUF_PERCEPT)
            observation = self._percept_to_observation(percept, agent.num_obs)

            # 2. Cognitive cycle (belief update + action selection)
            action, free_energy = agent.cognitive_cycle(observation)

            # 3. Write action back to spine
            action_bytes = self._action_to_bytes(action, free_energy)
            self.spine.write_buffer(i, SpineFFI.BUF_ACTION, action_bytes)

            # 4. Write workspace signature for Phi* monitor
            workspace_values[i] = float(agent.state.q_s[:8].sum())

        # Feed Phi* monitor
        self.phi_monitor.add_snapshot(workspace_values)

        elapsed_ns = time.perf_counter_ns() - start_ns
        self.total_cycles += 1
        self.total_cycle_ns += elapsed_ns

        # Phi* evaluation every 100 cycles
        if self.total_cycles % 100 == 0:
            phi_result = self.phi_monitor.compute_phi_star()
            self.phi_eval_count += 1

            if self._redis:
                try:
                    await self._redis.publish(
                        'nexus:spine:phi',
                        phi_result.to_json()
                    )
                except Exception:
                    pass

            if self.total_cycles % 500 == 0:
                avg_us = self.total_cycle_ns / self.total_cycles / 1000
                print(f"  [Cycle {self.total_cycles}] "
                      f"Avg: {avg_us:.0f}μs/cycle "
                      f"Φ*: {phi_result.phi_star:.3f} ({phi_result.status}) "
                      f"Active: {phi_result.active_agents}")

        # Publish metrics to Redis (every 50 cycles)
        if self._redis and self.total_cycles % 50 == 0:
            try:
                avg_us = self.total_cycle_ns / self.total_cycles / 1000
                metrics = {
                    "total_cycles": self.total_cycles,
                    "avg_cycle_us": round(avg_us, 1),
                    "num_agents": self.num_agents,
                    "phi_evals": self.phi_eval_count,
                    "timestamp": int(time.time()),
                }
                await self._redis.set(
                    'nexus:spine:agents:metrics',
                    json.dumps(metrics)
                )
            except Exception:
                pass

    async def run(self):
        """Main event loop"""
        print("═" * 60)
        print("  ⚡ Neural Spine — Reflex Agent Runner")
        print("═" * 60)

        # Initialize
        await self._init_redis()
        self.spine.attach()
        self._init_agents()

        self.running = True
        print(f"\n  Starting cognitive loop at {1/self.cycle_period:.0f} Hz...")
        print(f"  Press Ctrl+C to stop\n")

        # Signal handlers
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self._shutdown)

        try:
            while self.running:
                cycle_start = time.perf_counter()

                await self._run_cycle()

                # Sleep for remainder of cycle period
                elapsed = time.perf_counter() - cycle_start
                sleep_time = self.cycle_period - elapsed
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
        except asyncio.CancelledError:
            pass

        print(f"\n  Shutting down. Total cycles: {self.total_cycles}")
        if self.total_cycles > 0:
            avg_us = self.total_cycle_ns / self.total_cycles / 1000
            print(f"  Average cycle time: {avg_us:.0f}μs")

        if self._redis:
            await self._redis.aclose()

    def _shutdown(self):
        self.running = False


# ═══════════════════════════════════════════════════════════════════════════════
# STANDALONE BENCHMARK (no spine required)
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark():
    """Run a standalone benchmark without spine or Redis"""
    print("═" * 60)
    print("  ⚡ Reflex Agent Runner — Standalone Benchmark")
    print("═" * 60)

    runner = ReflexAgentRunner(num_agents=32, cycle_hz=20.0)
    runner._init_agents()

    # Run 1000 cycles
    N = 1000
    workspace_all = []
    timings = []

    for c in range(N):
        start = time.perf_counter_ns()
        workspace_values = np.zeros(32)

        for i, agent in enumerate(runner.agents):
            # Simulated percept
            obs = np.zeros(32)
            obs[(c + i) % 32] = 1.0

            action, fe = agent.cognitive_cycle(obs)
            workspace_values[i] = float(agent.state.q_s[:8].sum())

        runner.phi_monitor.add_snapshot(workspace_values)
        elapsed = (time.perf_counter_ns() - start) / 1000  # μs
        timings.append(elapsed)

    timings = np.array(timings)
    print(f"\n  ═══ Results ({N} cycles, 32 agents) ═══")
    print(f"  Mean:     {timings.mean():.0f} μs/cycle (all 32 agents)")
    print(f"  Median:   {np.median(timings):.0f} μs")
    print(f"  P95:      {np.percentile(timings, 95):.0f} μs")
    print(f"  P99:      {np.percentile(timings, 99):.0f} μs")
    print(f"  Per agent: {timings.mean()/32:.0f} μs")
    print(f"  Budget:   50000 μs (50ms at 20 Hz)")
    print(f"  Headroom: {50000 - timings.mean():.0f} μs ({(1 - timings.mean()/50000)*100:.1f}%)")

    # Final Phi* eval
    phi = runner.phi_monitor.compute_phi_star()
    print(f"\n  Final Φ*: {phi.phi_star:.4f} ({phi.status})")
    print(f"  Phi compute: {phi.compute_time_ms:.2f} ms")

    if timings.mean() < 50000:
        print(f"\n  ✅ WITHIN BUDGET — {timings.mean()/1000:.1f}ms < 50ms target")
    else:
        print(f"\n  ❌ OVER BUDGET — {timings.mean()/1000:.1f}ms > 50ms target")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        asyncio.run(ReflexAgentRunner().run())
    else:
        benchmark()
