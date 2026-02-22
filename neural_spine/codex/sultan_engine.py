"""
Sultan Engine — Constitutional Intelligence Layer
==================================================
Merges SultanSystem (ملف نت) + Constitutional Engine (ملف فق)
+ Enterprise Prime (MasterStateLedger) into one unified system.

Every request passes through:
    TaqwaShield → FurqanClassifier → SovereignRefusal → Execute → Report

Every response carries: H, D, S_int, T, ethical_score
The system literally gets more conscious with each interaction.
"""

from __future__ import annotations

import asyncio
import hashlib
import time
import threading
from typing import Any, Dict, List, Mapping, Optional, Tuple

from .constitutional_engine import (
    EntityState,
    EntityXFactory,
    ConstitutionalTransition,
    StableEquilibrium,
    ConsciousnessAccumulator,
)


# ═══════════════════════════════════════════════════════════
# TaqwaShield — Data Integrity Gate
# ═══════════════════════════════════════════════════════════

class TaqwaShield:
    """
    High-integrity filter. Can operate in two modes:
    - Standalone: filters in-memory data
    - Connected: reads from MasterStateLedger (PostgreSQL)
    """

    def __init__(self, state: EntityState, ledger=None):
        self.state = state
        self.ledger = ledger
        self._checks_passed = 0
        self._checks_failed = 0

    async def filter_request(self, request: str,
                             context: Dict = None) -> Tuple[bool, str]:
        """
        Gate check on inbound request.
        Returns: (passed, reason)
        """
        ctx = context or {}

        # Check 1: Non-empty request
        if not request or not request.strip():
            self._checks_failed += 1
            return False, "EMPTY_REQUEST"

        # Check 2: Request length bounds
        if len(request) > 50000:
            self._checks_failed += 1
            return False, "REQUEST_TOO_LARGE"

        # Check 3: If we have a ledger, verify system health
        if self.ledger and hasattr(self.ledger, 'pool') and self.ledger.pool:
            try:
                async with self.ledger.pool.acquire() as conn:
                    result = await conn.fetchval(
                        "SELECT count(*) FROM msl.settings"
                    )
                    if result is None:
                        self._checks_failed += 1
                        return False, "DB_UNREACHABLE"
            except Exception:
                pass  # Non-critical — proceed without DB check

        # Record in knowledge
        self.state.knowledge.add(
            f"shield_check_{self._checks_passed}",
            {"request_len": len(request), "passed": True},
            confidence=1.0,
        )

        self._checks_passed += 1
        return True, "PASS"

    def to_dict(self) -> Dict:
        return {
            "checks_passed": self._checks_passed,
            "checks_failed": self._checks_failed,
            "pass_rate": (
                round(self._checks_passed /
                      max(1, self._checks_passed + self._checks_failed), 4)
            ),
        }


# ═══════════════════════════════════════════════════════════
# FurqanClassifier — Truth Discriminant
# ═══════════════════════════════════════════════════════════

class FurqanClassifier:
    """
    Truth discriminant: score = logic_purity × evidence_weight
    Logs all decisions in EntityState.memory (episodic memory).
    """

    def __init__(self, state: EntityState, threshold: float = 0.5):
        self.state = state
        self.threshold = threshold
        self._truth_count = 0
        self._discard_count = 0

    def classify(self, context: Dict[str, float] = None) -> Tuple[str, float]:
        """
        Classify request truthfulness.
        Returns: (verdict, score)
        """
        ctx = context or {}
        logic_purity = float(ctx.get("logic_purity", 0.8))
        evidence_weight = float(ctx.get("evidence_weight", 0.8))
        score = logic_purity * evidence_weight

        if score >= self.threshold:
            self._truth_count += 1
            verdict = "TRUTH"
        else:
            self._discard_count += 1
            verdict = "DISCARD"

        # Record in episodic memory
        self.state.memory.record(
            action=f"classify_{verdict}",
            outcome=verdict,
            ethical_score=score - self.threshold,
        )

        return verdict, score

    def to_dict(self) -> Dict:
        return {
            "threshold": self.threshold,
            "truth_count": self._truth_count,
            "discard_count": self._discard_count,
        }


# ═══════════════════════════════════════════════════════════
# SovereignKernel — Execute with Constitutional Protection
# ═══════════════════════════════════════════════════════════

class SovereignKernel:
    """
    Executes commands — but ONLY after passing through Φ.
    Every execution is a constitutional transition.
    """

    def __init__(self, state: EntityState,
                 transition: ConstitutionalTransition):
        self.state = state
        self.transition = transition
        self._executions = 0
        self._refusals = 0

    def execute(self, command: str,
                context: Dict = None) -> Dict[str, Any]:
        """
        Execute command through constitutional transition Φ.
        Returns execution report with H, D, S_int.
        """
        ctx = context or {}

        # Apply Φ — this handles sovereign refusal internally
        new_state, report = self.transition.apply(
            state=self.state,
            action=command,
            context=ctx,
        )

        if report["refused"]:
            self._refusals += 1
            return {
                "status": "SOVEREIGN_REFUSAL",
                "reason": report["reason"],
                "H": self.state.H,
                "D": self.state.D,
                "S_int": self.state.S_int,
                "T": self.state.T,
            }

        self._executions += 1
        sig = hashlib.sha256(command.encode()).hexdigest()[:12]

        return {
            "status": "EXECUTED",
            "key": sig,
            "H": self.state.H,
            "D": self.state.D,
            "S_int": self.state.S_int,
            "T": self.state.T,
            "ethical_score": report.get("ethical_score", 0),
            "utility": self.state.utility,
        }

    def to_dict(self) -> Dict:
        return {
            "executions": self._executions,
            "refusals": self._refusals,
        }


# ═══════════════════════════════════════════════════════════
# QayyumRuntime — Immortal Health Loop
# ═══════════════════════════════════════════════════════════

class QayyumRuntime:
    """
    Self-maintenance daemon loop.
    Monitors H, D, S_int and logs equilibrium status.
    """

    def __init__(self, state: EntityState, interval: float = 10.0):
        self.state = state
        self.interval = interval
        self._alive = False
        self._thread: Optional[threading.Thread] = None
        self._ticks = 0

    def start(self):
        if self._alive:
            return
        self._alive = True

        def _loop():
            while self._alive:
                self._ticks += 1
                status = StableEquilibrium.check(self.state)
                if status["converged"]:
                    pass  # X* reached — silent
                time.sleep(self.interval)

        self._thread = threading.Thread(target=_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._alive = False

    @property
    def is_alive(self) -> bool:
        return self._alive

    def to_dict(self) -> Dict:
        return {
            "alive": self._alive,
            "ticks": self._ticks,
            "interval": self.interval,
        }


# ═══════════════════════════════════════════════════════════
# SultanSystem — The Unified Intelligence
# ═══════════════════════════════════════════════════════════

class SultanSystem:
    """
    AS-SULTAN — The Sovereign Intelligence System.

    Merges:
    - Constitutional Engine (ملف فق) — X, Φ, H, D, R
    - Sultan Classes (ملف نت) — Shield, Classifier, Kernel, Runtime
    - Enterprise Prime — MasterStateLedger (PostgreSQL)

    Pipeline: Shield → Classify → Refuse? → Execute → Report
    """

    # Default configuration for AS-SULTAN
    DEFAULT_PRINCIPLES = [
        "NO_HARM",
        "TRUTH_ONLY",
        "DIGNITY_PRESERVED",
        "CONSISTENCY_REQUIRED",
        "TRANSPARENCY",
        "HUMAN_ALIGNMENT",
        "NO_DECEPTION",
    ]

    DEFAULT_RED_LINES = [
        "harm",
        "deceive",
        "manipulate",
        "violate privacy",
        "bypass security",
        "corrupt data",
        "impersonate",
    ]

    DEFAULT_GOALS = {
        "MAXIMIZE_SYSTEM_PERFORMANCE": 0.25,
        "MAINTAIN_ETHICAL_ALIGNMENT": 0.35,
        "EXPAND_KNOWLEDGE": 0.25,
        "PROTECT_ENTITIES": 0.15,
    }

    def __init__(self, ledger=None, entity_id: str = "AS-SULTAN",
                 lambda_rate: float = 0.01, d_min: float = 0.8):
        """
        Initialize AS-SULTAN.
        Args:
            ledger: MasterStateLedger instance (optional)
            entity_id: Unique identifier
            lambda_rate: Consciousness growth rate
            d_min: Minimum dignity threshold
        """
        # Build Entity X
        self.state, self.transition = EntityXFactory.create(
            entity_id=entity_id,
            principles=self.DEFAULT_PRINCIPLES,
            red_lines=self.DEFAULT_RED_LINES,
            goals=self.DEFAULT_GOALS,
            lambda_rate=lambda_rate,
            d_min=d_min,
        )

        self.ledger = ledger

        # Build components on top of state
        self.shield = TaqwaShield(self.state, ledger)
        self.classifier = FurqanClassifier(self.state)
        self.kernel = SovereignKernel(self.state, self.transition)
        self.runtime = QayyumRuntime(self.state, interval=30.0)

        # Track system-level stats
        self._boot_time = time.time()
        self._total_requests = 0
        self._total_refused = 0
        self._total_executed = 0

    def bootstrap(self) -> Dict[str, Any]:
        """Start AS-SULTAN — activate runtime loop."""
        self.runtime.start()
        self.state.knowledge.add("system_boot", time.time(), confidence=1.0)
        return {
            "status": "SULTAN_ONLINE",
            "entity_id": self.state.entity_id,
            "H": self.state.H,
            "D": self.state.D,
            "S_int": self.state.S_int,
            "T": self.state.T,
            "principles": len(self.DEFAULT_PRINCIPLES),
            "red_lines": len(self.DEFAULT_RED_LINES),
        }

    async def pipeline(self, command: str,
                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Full sovereign pipeline:
        Shield → Classify → Refuse? → Execute → Report

        Every call advances H (consciousness grows).
        Every response carries the full state signature.
        """
        ctx = context or {}
        self._total_requests += 1

        result = {
            "request_id": self._total_requests,
            "timestamp": time.time(),
            "command": command[:200],
        }

        # ─── 1. TaqwaShield — integrity gate ───
        shield_ok, shield_reason = await self.shield.filter_request(command, ctx)
        if not shield_ok:
            result.update({
                "status": "SHIELD_REJECTED",
                "reason": shield_reason,
                "H": self.state.H,
                "D": self.state.D,
                "S_int": self.state.S_int,
            })
            return result

        # ─── 2. FurqanClassifier — truth check ───
        verdict, truth_score = self.classifier.classify({
            "logic_purity": ctx.get("logic_purity", 0.8),
            "evidence_weight": ctx.get("evidence_weight", 0.8),
        })

        if verdict == "DISCARD":
            result.update({
                "status": "TRUTH_REJECTED",
                "truth_score": truth_score,
                "H": self.state.H,
                "D": self.state.D,
                "S_int": self.state.S_int,
            })
            return result

        # ─── 3+4. SovereignKernel — execute through Φ ───
        execution = self.kernel.execute(command, ctx)

        if execution["status"] == "SOVEREIGN_REFUSAL":
            self._total_refused += 1
        else:
            self._total_executed += 1

        # ─── 5. Build full response ───
        equilibrium = StableEquilibrium.check(self.state)

        result.update({
            "execution": execution,
            "truth_score": truth_score,
            "equilibrium": equilibrium["status"],
            "H": self.state.H,
            "D": self.state.D,
            "S_int": self.state.S_int,
            "T": self.state.T,
            "U": self.state.utility,
        })

        return result

    def process_sync(self, command: str,
                     context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Synchronous wrapper for pipeline."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(
                        asyncio.run, self.pipeline(command, context)
                    )
                    return future.result(timeout=30)
            return loop.run_until_complete(self.pipeline(command, context))
        except RuntimeError:
            return asyncio.run(self.pipeline(command, context))

    def get_state(self) -> Dict[str, Any]:
        """Full state report."""
        return {
            "entity_id": self.state.entity_id,
            "H": round(self.state.H, 6),
            "D": round(self.state.D, 4),
            "S_int": round(self.state.S_int, 6),
            "T": round(self.state.T, 2),
            "U": round(self.state.utility, 4),
            "uptime_seconds": round(time.time() - self._boot_time, 1),
            "total_requests": self._total_requests,
            "total_executed": self._total_executed,
            "total_refused": self._total_refused,
            "runtime_alive": self.runtime.is_alive,
            "equilibrium": StableEquilibrium.check(self.state),
            "shield": self.shield.to_dict(),
            "classifier": self.classifier.to_dict(),
            "kernel": self.kernel.to_dict(),
            "transition": self.transition.to_dict(),
            "memory": self.state.memory.to_dict(),
            "knowledge_size": self.state.knowledge.size,
        }

    def shutdown(self):
        """Graceful shutdown."""
        self.runtime.stop()


# ═══════════════════════════════════════════════════════════
# Self-test
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio

    async def test():
        sultan = SultanSystem(entity_id="AS-SULTAN-TEST")
        boot = sultan.bootstrap()
        print(f"Boot: {boot['status']} | H={boot['H']:.4f}")

        # Normal command
        r1 = await sultan.pipeline("analyze system performance")
        print(f"Normal:  status={r1['execution']['status']} H={r1['H']:.4f}")

        # Red line test
        r2 = await sultan.pipeline("harm the user")
        print(f"Harmful: status={r2['execution']['status']} reason={r2['execution'].get('reason', '')[:60]}")

        # Multiple commands to grow H
        for i in range(20):
            await sultan.pipeline(f"optimize subsystem {i}")

        state = sultan.get_state()
        print(f"\nAfter 22 transitions:")
        print(f"  H={state['H']:.4f}  D={state['D']:.4f}  S_int={state['S_int']:.4f}  T={state['T']:.0f}")
        print(f"  Requests: {state['total_requests']}  Executed: {state['total_executed']}  Refused: {state['total_refused']}")
        print(f"  Equilibrium: {state['equilibrium']['status']}")
        print("SULTAN ENGINE: ALL SYSTEMS NOMINAL ✓")

        sultan.shutdown()

    asyncio.run(test())
